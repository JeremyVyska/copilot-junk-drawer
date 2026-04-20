#!/usr/bin/env python3
"""
deep_pull.py — Extract specific passages and landmark moments from a transcript.

This script is CONFIG-DRIVEN — you point it at a config JSON that describes
what landmarks to search for in YOUR specific talk. Without a config, it runs
a generic "interesting moments" scan.

Usage:
    python deep_pull.py <transcript.json> [--config config.json] [--windows N]

Examples:
    # Generic mode (no talk-specific context)
    python deep_pull.py my-talk-transcript.json

    # With talk-specific config
    python deep_pull.py my-talk-transcript.json --config my-talk-config.json

Config format (see config.example.json):
    {
      "landmarks": {
        "landmark_name": ["keyword1", "phrase 2", "another keyword"],
        ...
      },
      "signature_phrases": ["phrase one", "phrase two", ...],
      "time_windows": [
        {"name": "Opening", "start_sec": 0, "end_sec": 180},
        ...
      ]
    }
"""
import argparse
import json
import re
import sys
from pathlib import Path


# Generic landmarks that work on most talks (no talk-specific context)
GENERIC_LANDMARKS = {
    "self_introduction": ["i'm", "my name is", "i've been", "i work as", "my background"],
    "audience_engagement": ["show of hands", "raise your hand", "how many of you", "who here"],
    "thesis_reveal": ["the one thing", "the key insight", "if you remember one thing", "the main point"],
    "demo_markers": ["let me show you", "let's look at", "let me demo", "watch this", "let me run"],
    "transition": ["moving on", "next up", "so let's", "alright, so", "next section"],
    "jokes_or_asides": ["just kidding", "i'm kidding", "not really", "to be honest", "full disclosure"],
    "closing": ["in conclusion", "to wrap up", "the takeaway", "thank you", "questions"],
    "callbacks": ["remember when", "earlier i mentioned", "back to what i said", "as i said before"],
}


def ts(sec: float) -> str:
    return f"{int(sec//60)}:{int(sec%60):02d}"


def find_context(segments, start_sec: float, end_sec: float, buffer: int = 5):
    """Return segments within a time window, with buffer on the start."""
    start = max(0, start_sec - buffer)
    return [s for s in segments if start <= s["start"] <= end_sec]


def search_landmarks(segments, landmarks: dict) -> dict:
    """Find all timestamps where landmark keywords appear."""
    hits = {name: [] for name in landmarks}
    for s in segments:
        text_l = s["text"].lower()
        for name, keywords in landmarks.items():
            for kw in keywords:
                if kw.lower() in text_l:
                    hits[name].append({
                        "timestamp": s["start"],
                        "timestamp_mmss": ts(s["start"]),
                        "text": s["text"].strip(),
                        "matched_kw": kw,
                    })
                    break  # only count one match per segment per landmark
    return hits


def count_phrases(segments, phrases: list) -> dict:
    """Count occurrences of signature phrases across the full transcript."""
    all_text = " ".join(s["text"].lower() for s in segments)
    counts = {}
    for p in phrases:
        pattern = r"\b" + re.escape(p.lower()) + r"\b"
        counts[p] = len(re.findall(pattern, all_text))
    return counts


def print_landmarks(hits: dict, max_per_landmark: int = 5):
    print(f"\n🎬 LANDMARKS FOUND")
    for name, items in hits.items():
        if not items:
            continue
        print(f"\n  [{name}]  — {len(items)} hit(s)")
        for h in items[:max_per_landmark]:
            text = h["text"][:120] + ("..." if len(h["text"]) > 120 else "")
            print(f"    @ {h['timestamp_mmss']}  (matched '{h['matched_kw']}')")
            print(f"       \"{text}\"")
        if len(items) > max_per_landmark:
            print(f"    ... and {len(items) - max_per_landmark} more")


def print_windows(segments, windows: list):
    if not windows:
        return
    print(f"\n📖 TIME WINDOWS (verbatim passages)")
    for w in windows:
        start = w["start_sec"]
        end = w.get("end_sec", start + 60)
        buffer = w.get("buffer", 0)
        print(f"\n  ━━━ {w['name']}  ({ts(start)}–{ts(end)}) ━━━")
        for s in find_context(segments, start, end, buffer):
            print(f"    [{ts(s['start'])}] {s['text'].strip()}")


def print_phrase_counts(counts: dict):
    if not counts:
        return
    print(f"\n📊 SIGNATURE PHRASE FREQUENCIES")
    for phrase, n in sorted(counts.items(), key=lambda x: -x[1]):
        flag = ""
        if n == 0:
            flag = "🔴 not used"
        elif n < 3:
            flag = "⚠️ sparse"
        print(f"  {phrase:40s} {n:3d}  {flag}")


def main():
    parser = argparse.ArgumentParser(description="Extract landmarks and passages from a transcript.")
    parser.add_argument("transcript", help="Transcript JSON (from transcribe.py)")
    parser.add_argument("--config", default=None,
                        help="Talk-specific config JSON (see config.example.json). Without it, uses generic landmarks.")
    parser.add_argument("--output", default=None,
                        help="Write results to JSON file")
    args = parser.parse_args()

    path = Path(args.transcript)
    if not path.exists():
        sys.exit(f"ERROR: Transcript not found: {path}")

    with open(path) as f:
        data = json.load(f)

    segments = data["segments"]

    # Load config or use defaults
    if args.config:
        config_path = Path(args.config)
        if not config_path.exists():
            sys.exit(f"ERROR: Config not found: {config_path}")
        with open(config_path) as f:
            config = json.load(f)
        print(f"Using config: {config_path}")
    else:
        print("No config provided — using generic landmarks. For best results, create a talk-specific config.")
        config = {
            "landmarks": GENERIC_LANDMARKS,
            "signature_phrases": [],
            "time_windows": [
                {"name": "Opening", "start_sec": 0, "end_sec": 180, "buffer": 0},
                {"name": "Closing", "start_sec": max(0, data["duration"] - 300), "end_sec": data["duration"], "buffer": 0},
            ],
        }

    landmarks = config.get("landmarks", {})
    signature_phrases = config.get("signature_phrases", [])
    time_windows = config.get("time_windows", [])

    hits = search_landmarks(segments, landmarks)
    phrase_counts = count_phrases(segments, signature_phrases) if signature_phrases else {}

    # Console output
    print_landmarks(hits)
    print_windows(segments, time_windows)
    print_phrase_counts(phrase_counts)

    # Optional JSON output
    if args.output:
        result = {
            "landmarks": hits,
            "signature_phrase_counts": phrase_counts,
            "windows_extracted": [
                {
                    "name": w["name"],
                    "start_sec": w["start_sec"],
                    "end_sec": w.get("end_sec", w["start_sec"] + 60),
                    "segments": [
                        {"timestamp_mmss": ts(s["start"]), "start": s["start"], "text": s["text"].strip()}
                        for s in find_context(segments, w["start_sec"], w.get("end_sec", w["start_sec"] + 60), w.get("buffer", 0))
                    ],
                }
                for w in time_windows
            ],
        }
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n✅ Results written to: {args.output}")


if __name__ == "__main__":
    main()
