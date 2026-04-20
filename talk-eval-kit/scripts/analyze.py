#!/usr/bin/env python3
"""
analyze.py — Compute the generic metrics layer for a transcribed talk.

Usage:
    python analyze.py <transcript.json> [--bucket-sec N] [--output metrics.json]

Examples:
    python analyze.py my-talk-transcript.json
    python analyze.py my-talk-transcript.json --bucket-sec 60 --output my-metrics.json

What it produces:
    - Baseline stats (duration, word count, overall WPM)
    - Filler word counts & rates per 10 min
    - Speaking pace by time-bucket (default 2-min windows)
    - Pause detection (significant: 1.5-3s, dramatic: >3s)
    - Engagement markers (questions asked, you/we/I ratios)

What it does NOT produce (requires human/LLM interpretation):
    - Actual audience response (laughter, gasps — filtered by Whisper VAD)
    - Vocal tone or energy modulation
    - Whether a pause was "dramatic good" or "dead air bad"
    - Structural quality vs. an intended outline

Use this output alongside AGENT_INSTRUCTIONS.md to generate the full evaluation.
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


FILLER_PATTERNS = {
    "um":       r"\b(?:um|umm|ummm)\b",
    "uh":       r"\b(?:uh|uhh|uhhh)\b",
    "like":     r"\blike\b",
    "you_know": r"\byou know\b",
    "kind_of":  r"\bkind of\b",
    "sort_of":  r"\bsort of\b",
    "actually": r"\bactually\b",
    "basically": r"\bbasically\b",
    "literally": r"\bliterally\b",
    "right_q":  r"\bright\?",
    "okay_filler": r"\bokay,",
    "so_start": r"(?:^|\. )so[ ,]",
}


def compute_metrics(data: dict, bucket_sec: int = 120) -> dict:
    segments = data["segments"]
    duration = data["duration"]

    all_text = " ".join(s["text"] for s in segments)
    text_lower = all_text.lower()
    total_words = sum(len(s.get("words", [])) for s in segments)

    # Filler word counts
    filler_counts = {}
    for name, pat in FILLER_PATTERNS.items():
        matches = re.findall(pat, text_lower, re.MULTILINE)
        filler_counts[name] = {
            "count": len(matches),
            "per_10min": round(len(matches) / (duration / 600), 2),
        }

    # Speaking pace by bucket
    buckets = defaultdict(lambda: {"words": 0, "duration": 0.0})
    for s in segments:
        b = int(s["start"] // bucket_sec)
        buckets[b]["words"] += len(s.get("words", []))
        buckets[b]["duration"] += s["end"] - s["start"]

    pace_by_bucket = []
    for b, v in sorted(buckets.items()):
        if v["duration"] > 0:
            wpm = v["words"] / (v["duration"] / 60)
            pace_by_bucket.append({
                "bucket": b,
                "time_start_sec": b * bucket_sec,
                "time_range": f"{b*bucket_sec//60}:{b*bucket_sec%60:02d}-"
                              f"{((b+1)*bucket_sec)//60}:{((b+1)*bucket_sec)%60:02d}",
                "wpm": round(wpm, 1),
                "word_count": v["words"],
                "tag": ("fast" if wpm > 200 else "slow" if wpm < 140 else "normal"),
            })

    # Pause detection
    significant_pauses = []
    dramatic_pauses = []
    for i in range(len(segments) - 1):
        gap = segments[i + 1]["start"] - segments[i]["end"]
        if gap > 3.0:
            dramatic_pauses.append({
                "gap_sec": round(gap, 2),
                "timestamp": segments[i]["end"],
                "timestamp_mmss": f"{int(segments[i]['end']//60)}:{int(segments[i]['end']%60):02d}",
                "text_before": segments[i]["text"].strip()[-150:],
                "text_after": segments[i + 1]["text"].strip()[:150],
            })
        elif gap > 1.5:
            significant_pauses.append({
                "gap_sec": round(gap, 2),
                "timestamp": segments[i]["end"],
                "timestamp_mmss": f"{int(segments[i]['end']//60)}:{int(segments[i]['end']%60):02d}",
            })

    # Engagement markers
    question_count = len(re.findall(r"\?", all_text))
    # Word-boundary checks for pronoun use
    you_count = len(re.findall(r"\byou\b", text_lower))
    we_count = len(re.findall(r"\bwe\b", text_lower))
    i_count = len(re.findall(r"\bI\b", all_text))  # case-sensitive to avoid false positives
    you_i_ratio = round(you_count / max(i_count, 1), 2)

    # Overall baseline
    overall_wpm = round(total_words / (duration / 60), 1)

    return {
        "source_file": data.get("source_file", "unknown"),
        "baseline": {
            "duration_sec": round(duration, 1),
            "duration_min": round(duration / 60, 1),
            "total_words": total_words,
            "segment_count": len(segments),
            "overall_wpm": overall_wpm,
            "overall_wpm_assessment": _wpm_assessment(overall_wpm),
        },
        "filler_words": filler_counts,
        "pace_by_bucket": pace_by_bucket,
        "pauses": {
            "dramatic_count": len(dramatic_pauses),
            "significant_count": len(significant_pauses),
            "dramatic": dramatic_pauses,
            "significant": significant_pauses[:40],  # cap for file size
        },
        "engagement": {
            "questions_asked": question_count,
            "you_count": you_count,
            "we_count": we_count,
            "i_count": i_count,
            "you_to_i_ratio": you_i_ratio,
            "assessment": _engagement_assessment(you_i_ratio, question_count, duration),
        },
    }


def _wpm_assessment(wpm: float) -> str:
    if wpm < 130:
        return "slow — may feel plodding or overly formal"
    if wpm < 150:
        return "measured — conversational, easy to follow"
    if wpm < 170:
        return "energetic — good conference-speaker range"
    if wpm < 185:
        return "brisk — confident but may challenge non-native listeners"
    return "fast — risks losing audience on complex material"


def _engagement_assessment(ratio: float, questions: int, duration_sec: float) -> str:
    q_per_10min = questions / (duration_sec / 600)
    if ratio < 0.5:
        tone = "monologue-heavy (I-focused)"
    elif ratio < 0.9:
        tone = "balanced between self-reference and audience"
    else:
        tone = "audience-focused (you-heavy)"

    if q_per_10min < 2:
        rhetorical = "few rhetorical questions"
    elif q_per_10min < 8:
        rhetorical = "regular rhetorical engagement"
    else:
        rhetorical = "highly conversational with frequent audience questions"

    return f"{tone}; {rhetorical} ({q_per_10min:.1f} questions / 10 min)"


def print_summary(metrics: dict):
    b = metrics["baseline"]
    print("=" * 70)
    print("TALK METRICS — GENERIC ANALYSIS")
    print("=" * 70)
    print(f"\nSource: {metrics['source_file']}")
    print(f"Duration: {b['duration_min']:.1f} min  ({b['total_words']:,} words)")
    print(f"Overall WPM: {b['overall_wpm']}  — {b['overall_wpm_assessment']}")

    print(f"\n🎤 FILLER WORDS")
    for name, v in sorted(metrics["filler_words"].items(), key=lambda x: -x[1]["count"]):
        flag = ""
        if v["per_10min"] > 5:
            flag = "⚠️ coaching target"
        elif v["per_10min"] > 3:
            flag = "👀 watch"
        print(f"  {name:12s} {v['count']:4d} total ({v['per_10min']:>4.1f}/10min) {flag}")

    print(f"\n🏃 SPEAKING PACE BY BUCKET")
    for p in metrics["pace_by_bucket"]:
        marker = {"fast": "⚡", "slow": "🐢", "normal": "  "}[p["tag"]]
        print(f"  {marker} {p['time_range']:12s} {p['wpm']:6.1f} WPM  ({p['word_count']} words)")

    print(f"\n🔇 PAUSES")
    print(f"  Dramatic (>3s):    {metrics['pauses']['dramatic_count']}")
    print(f"  Significant (1.5-3s): {metrics['pauses']['significant_count']}")
    print(f"\n  Dramatic pause details:")
    for p in metrics["pauses"]["dramatic"][:15]:
        print(f"    @ {p['timestamp_mmss']}  gap={p['gap_sec']}s")
        print(f"      ← \"...{p['text_before'][-80:]}\"")
        print(f"      → \"{p['text_after'][:80]}...\"")

    print(f"\n💬 ENGAGEMENT")
    e = metrics["engagement"]
    print(f"  Questions asked: {e['questions_asked']}")
    print(f"  You: {e['you_count']}  We: {e['we_count']}  I: {e['i_count']}")
    print(f"  You:I ratio: {e['you_to_i_ratio']}")
    print(f"  Assessment: {e['assessment']}")


def main():
    parser = argparse.ArgumentParser(description="Analyze a transcribed talk.")
    parser.add_argument("transcript", help="Transcript JSON (from transcribe.py)")
    parser.add_argument("--bucket-sec", type=int, default=120,
                        help="Time bucket size in seconds (default: 120)")
    parser.add_argument("--output", default=None,
                        help="Write metrics to JSON file (default: <transcript>-metrics.json)")
    parser.add_argument("--quiet", action="store_true",
                        help="Suppress the console summary")
    args = parser.parse_args()

    path = Path(args.transcript)
    if not path.exists():
        sys.exit(f"ERROR: Transcript not found: {path}")

    with open(path) as f:
        data = json.load(f)

    metrics = compute_metrics(data, bucket_sec=args.bucket_sec)

    output_path = args.output or str(path.with_name(path.stem.replace("-transcript", "") + "-metrics.json"))
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    if not args.quiet:
        print_summary(metrics)
        print(f"\n✅ Metrics written to: {output_path}")


if __name__ == "__main__":
    main()
