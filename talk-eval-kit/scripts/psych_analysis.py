#!/usr/bin/env python3
"""
psych_analysis.py — Detect psychological-design patterns in a talk transcript.

This is Dimension 6 of the evaluation framework: "Psychological Design."
It checks whether the talk deployed the deliberate rhetorical and persuasive
moves that evidence-based research on presentations recommends.

Does NOT replace the core analyze.py metrics. This runs alongside it as a
separate scoring lens. A talk can have great vocal mechanics (covered by
analyze.py) and still fail to land because it ignored the peak-end rule or
skipped every Cialdini principle. This script catches those.

Heavily inspired by a synthesis of evaluation frameworks from Kirkpatrick
(evaluation levels), Cialdini (influence principles), Kahneman (peak-end,
anchoring), Mayer (dual coding via narrative), Bandura (self-efficacy
framing), and Edmondson (psychological safety).

Usage:
    python psych_analysis.py <transcript.json> [--config config.json] [--output out.json]

Notes:
    - Detection is heuristic, not perfect. A "social proof" marker is
      absence/presence of social-proof LANGUAGE — it doesn't evaluate whether
      the evidence was compelling.
    - Config optionally supplies talk-specific thesis phrases and CTA candidates
      for higher-fidelity detection. Without config, falls back to generic checks.
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


# ========== CIALDINI PRINCIPLE SIGNALS ==========
# Each principle has linguistic markers. Presence-of-signal is necessary but
# not sufficient — a human should review whether the deployment actually worked.

CIALDINI_SIGNALS = {
    "reciprocity": [
        r"\bfree\b", r"\bgiving you\b", r"\bhere's a\b.*\b(?:tool|template|repo|gift|handout|script|download)",
        r"\btake this home\b", r"\byou can have\b", r"\bshare with you\b",
        r"\bhere is my\b", r"\bi built this for\b", r"\bi'm giving\b",
    ],
    "commitment_consistency": [
        r"\braise your hand\b", r"\bshow of hands\b", r"\bhow many of you\b",
        r"\bwho here has\b", r"\bnod if\b", r"\bcommit to\b", r"\byou've already\b",
        r"\bif you've ever\b",
    ],
    "social_proof": [
        r"\bmost people\b", r"\bpeople like you\b", r"\bothers have\b",
        r"\bmy customers\b", r"\bpartners are\b", r"\badoption\b",
        r"\beveryone (?:is|has)\b", r"\bcommunity is\b", r"\bthousands of\b",
    ],
    "authority": [
        r"\byears of experience\b", r"\b\d+\+? years\b", r"\bmvp\b", r"\bpublished\b",
        r"\bresearched\b", r"\bi've been doing\b", r"\bi've worked\b",
        r"\bi teach\b", r"\bmy background\b",
    ],
    "liking": [
        r"\bwe all\b", r"\bi've been there\b", r"\bi know how\b.*\bfeels\b",
        r"\bi get it\b", r"\bi used to\b",
    ],
    "scarcity": [
        r"\blimited\b", r"\bonly available\b", r"\bexclusive\b", r"\bwhile it lasts\b",
        r"\bfor a short time\b", r"\bright now\b.*\b(?:free|available|working)",
        r"\bthe window\b", r"\bgolden era\b",
    ],
    "unity_identity": [
        r"\bwe (?:the|all|as)\b", r"\bour community\b", r"\bour (?:industry|field|craft)\b",
        r"\bus (?:developers|folks|people)\b", r"\bfellow\b.*\b(?:developers|devs)",
        r"\bpeople in (?:this|the) room\b", r"\bfolks (?:in|here|like)\b",
    ],
}


# ========== STORYTELLING MARKERS ==========
# Narrative density = past-tense verbs + named characters + dialogue
NARRATIVE_MARKERS = {
    "past_tense_narrative": r"\b(?:said|told|called|asked|showed|realized|found|figured|decided|tried|wondered|noticed)\b",
    "dialogue_intro": r"(?:said|says|goes|asked|told me|yelled|whispered)[ ,]+['\"]",
    "dialogue_quotes": r"['\"][^'\"]{15,}['\"]",
    "named_character_refs": r"\b(?:my (?:customer|colleague|team|buddy|friend|dev|client|manager|boss|partner))\b",
    "time_markers": r"\b(?:yesterday|last (?:week|month|year)|back in|a (?:few|couple) (?:days|weeks|months) ago|one time|once)\b",
    "scene_setters": r"\b(?:imagine|picture this|so there i was|it was a|walking into|sitting at)\b",
}


# ========== PSYCHOLOGICAL SAFETY MARKERS ==========
SAFETY_MARKERS = [
    r"\bno (?:dumb|stupid|bad) questions?\b",
    r"\bany questions?\b.*\bwelcome\b",
    r"\binterrupt me\b", r"\bstop me\b", r"\bcall (?:me )?out\b",
    r"\bit's okay (?:to|if)\b", r"\bdon't worry (?:about|if)\b",
    r"\bmistakes? (?:are|is) (?:fine|okay|part of)\b",
    r"\bi've (?:screwed|messed|gotten) (?:this|it) up\b",
    r"\bi was wrong\b", r"\bi didn't know\b",
]


# ========== SELF-EFFICACY / GROWTH FRAMING ==========
EFFICACY_MARKERS = [
    r"\byou can (?:do|build|make|ship)\b", r"\bin (?:five|ten|fifteen|10|15|30) minutes\b",
    r"\bmonday morning\b", r"\bstart with\b", r"\beasier than\b",
    r"\byou've already\b", r"\byou're ready\b", r"\bi have faith in\b",
    r"\byou've been doing\b", r"\byour (?:expertise|experience|wisdom)\b",
]


# ========== CALL-TO-ACTION MARKERS ==========
CTA_MARKERS = [
    r"\bgo (?:and |to |try )?(?:install|try|download|clone|fork|star|build|read|watch)\b",
    r"\bscan (?:this|the) (?:qr|code)\b",
    r"\bvisit\b.*\b(?:\.com|\.dev|\.io|\.net|github)",
    r"\bsign up (?:for|at)\b", r"\bjoin (?:me|us)\b", r"\bfollow (?:me|the)\b",
    r"\bcome (?:find|talk to|chat) (?:me|with me)\b",
    r"\btell me\b.*\b(?:what|how|if)\b", r"\breach out\b", r"\bemail me\b",
    r"\brate (?:this|the) session\b",
    r"\bnext (?:step|thing)\b", r"\bstart (?:here|with|by)\b",
    r"\btry (?:this|it|them) (?:out |on )?(?:monday|tomorrow|today|this week)\b",
]


def ts(sec: float) -> str:
    return f"{int(sec//60)}:{int(sec%60):02d}"


def find_matches(segments, patterns, case_sensitive=False):
    """Find all segments where any pattern matches. Returns list of hits with timestamps."""
    flags = 0 if case_sensitive else re.IGNORECASE
    hits = []
    for s in segments:
        text = s["text"]
        for pat in patterns:
            if re.search(pat, text, flags):
                hits.append({
                    "timestamp": s["start"],
                    "timestamp_mmss": ts(s["start"]),
                    "text": s["text"].strip(),
                    "pattern": pat,
                })
                break  # one match per segment is enough
    return hits


def analyze_cialdini(segments):
    """Score each Cialdini principle's deployment."""
    results = {}
    for principle, patterns in CIALDINI_SIGNALS.items():
        hits = find_matches(segments, patterns)
        results[principle] = {
            "count": len(hits),
            "deployed": len(hits) > 0,
            "first_hit": hits[0] if hits else None,
            "sample_hits": hits[:3],
        }
    return results


def analyze_peak_end(segments, duration):
    """
    Peak-end rule detection. Three things to look at:
    1. Opening 2 min — is there a strong anchor statement, specific number, or hook?
    2. Closing 2 min — is there a distinct CTA and emotional button?
    3. Middle — is there an identifiable "peak" (longest pause, most emphatic segment)?
    """
    opening_cutoff = 120  # first 2 minutes
    closing_cutoff = duration - 120  # last 2 minutes

    opening = [s for s in segments if s["start"] < opening_cutoff]
    closing = [s for s in segments if s["start"] >= closing_cutoff]

    # Look for specific numbers (anchors) in opening
    opening_text = " ".join(s["text"] for s in opening)
    opening_has_specific_number = bool(re.search(r"\b\d+(?:\.\d+)?\s*(?:percent|%|hours|minutes|times|years|weeks|days)\b", opening_text, re.IGNORECASE))
    opening_has_question = "?" in opening_text
    opening_has_story_opener = bool(re.search(r"\b(?:imagine|picture|so there|let me tell|once|back when)\b", opening_text, re.IGNORECASE))

    closing_text = " ".join(s["text"] for s in closing)
    closing_has_cta = bool(find_matches(closing, CTA_MARKERS))
    closing_has_callback = bool(re.search(r"\b(?:remember|as i said|we started|earlier)\b", closing_text, re.IGNORECASE))
    closing_has_emotional_button = bool(re.search(r"\b(?:thank you|let's|go (?:build|make|do)|the (?:real|whole) (?:point|thing))\b", closing_text, re.IGNORECASE))

    # Detect peak via dramatic pauses in the middle third (approx 30-70% of duration)
    middle_start = duration * 0.3
    middle_end = duration * 0.7
    middle_dramatic_pauses = []
    for i in range(len(segments) - 1):
        gap = segments[i + 1]["start"] - segments[i]["end"]
        if gap > 3.0 and middle_start <= segments[i]["end"] <= middle_end:
            middle_dramatic_pauses.append({
                "timestamp_mmss": ts(segments[i]["end"]),
                "gap_sec": round(gap, 2),
                "text_before": segments[i]["text"].strip()[-150:],
            })

    peak_detected = len(middle_dramatic_pauses) > 0

    return {
        "opening": {
            "text_preview": " ".join(s["text"].strip() for s in opening[:5])[:300],
            "has_specific_number_anchor": opening_has_specific_number,
            "has_engagement_question": opening_has_question,
            "has_story_opener": opening_has_story_opener,
            "assessment": _opening_assessment(opening_has_specific_number, opening_has_question, opening_has_story_opener),
        },
        "closing": {
            "text_preview": " ".join(s["text"].strip() for s in closing[-5:])[:300],
            "has_cta": closing_has_cta,
            "has_callback_to_opening": closing_has_callback,
            "has_emotional_button": closing_has_emotional_button,
            "assessment": _closing_assessment(closing_has_cta, closing_has_callback, closing_has_emotional_button),
        },
        "peak_moments": {
            "detected_peaks": peak_detected,
            "peak_count": len(middle_dramatic_pauses),
            "candidates": middle_dramatic_pauses[:5],
        },
    }


def _opening_assessment(has_num, has_q, has_story):
    score = sum([has_num, has_q, has_story])
    if score >= 2:
        return "strong — opening uses multiple engagement techniques"
    if score == 1:
        return "adequate — one engagement technique used"
    return "weak — opening may not capture attention fast enough"


def _closing_assessment(has_cta, has_callback, has_button):
    score = sum([has_cta, has_callback, has_button])
    if score >= 2:
        return "strong — closing hits CTA, callback, and/or emotional button"
    if score == 1:
        return "adequate — one closing technique used"
    return "weak — closing may fade rather than land"


def analyze_storytelling(segments):
    """Narrative density analysis. High narrative = more story, less lecture."""
    narrative_hits = {}
    total = 0
    for name, pat in NARRATIVE_MARKERS.items():
        matches = 0
        for s in segments:
            matches += len(re.findall(pat, s["text"], re.IGNORECASE))
        narrative_hits[name] = matches
        total += matches

    segment_count = len(segments)
    narrative_per_segment = total / max(segment_count, 1)

    if narrative_per_segment > 0.8:
        assessment = "story-heavy — strong narrative texture throughout"
    elif narrative_per_segment > 0.4:
        assessment = "balanced — mix of narrative and exposition"
    else:
        assessment = "exposition-heavy — may benefit from more story beats"

    return {
        "marker_counts": narrative_hits,
        "total_narrative_markers": total,
        "narrative_per_segment": round(narrative_per_segment, 3),
        "assessment": assessment,
    }


def analyze_psychological_safety(segments):
    hits = find_matches(segments, SAFETY_MARKERS)
    return {
        "count": len(hits),
        "deployed": len(hits) > 0,
        "sample_hits": hits[:3],
        "assessment": "explicit safety markers present" if hits else "no explicit safety invitations — audience may be more hesitant to engage",
    }


def analyze_self_efficacy(segments):
    hits = find_matches(segments, EFFICACY_MARKERS)
    return {
        "count": len(hits),
        "deployed": len(hits) > 0,
        "sample_hits": hits[:5],
        "assessment": "efficacy framing strong" if len(hits) >= 3 else ("some efficacy framing" if hits else "efficacy framing absent — audience may not feel empowered to act"),
    }


def analyze_ctas(segments, duration):
    """Count CTAs and check whether they cluster in the closing."""
    hits = find_matches(segments, CTA_MARKERS)
    closing_threshold = duration - 180  # last 3 min
    closing_ctas = [h for h in hits if h["timestamp"] >= closing_threshold]

    return {
        "total_cta_count": len(hits),
        "closing_cta_count": len(closing_ctas),
        "has_closing_cta": len(closing_ctas) > 0,
        "all_ctas": hits[:10],
        "assessment": _cta_assessment(len(hits), len(closing_ctas)),
    }


def _cta_assessment(total, closing):
    if total == 0:
        return "no CTAs detected — audience has nothing specific to do after the talk"
    if closing == 0:
        return "CTAs present mid-talk but missing at close — call to action may not land as the takeaway"
    if total > 8:
        return "many CTAs — risk of diffusing the primary ask"
    return "CTA deployment looks intentional"


def analyze_repetition(segments, thesis_phrases):
    """Mere exposure effect — did core messages get repeated enough to stick?"""
    if not thesis_phrases:
        return {
            "note": "no thesis phrases provided in config — skipping repetition analysis",
            "counts": {},
        }

    text_lower = " ".join(s["text"].lower() for s in segments)
    counts = {}
    for phrase in thesis_phrases:
        pattern = r"\b" + re.escape(phrase.lower()) + r"\b"
        n = len(re.findall(pattern, text_lower))
        counts[phrase] = n

    # Assessment: a thesis phrase should appear at least 3 times to benefit from mere exposure
    under_exposed = [p for p, c in counts.items() if c < 3]

    return {
        "counts": counts,
        "under_exposed": under_exposed,
        "assessment": (
            f"all thesis phrases repeated adequately"
            if not under_exposed
            else f"under-exposed thesis phrases (< 3 repetitions): {under_exposed}"
        ),
    }


def print_summary(results):
    print("=" * 70)
    print("DIMENSION 6 — PSYCHOLOGICAL DESIGN ANALYSIS")
    print("=" * 70)

    print("\n🏛️ CIALDINI PRINCIPLES DEPLOYMENT")
    for principle, data in results["cialdini"].items():
        status = "✅" if data["deployed"] else "⚠️  MISSING"
        print(f"  {status}  {principle:25s} hits={data['count']}")
        if data["sample_hits"]:
            sample = data["sample_hits"][0]
            print(f"         └ first @ {sample['timestamp_mmss']}: \"{sample['text'][:80]}...\"")

    print("\n🎯 PEAK-END RULE")
    pe = results["peak_end"]
    print(f"  Opening: {pe['opening']['assessment']}")
    print(f"    anchor_num={pe['opening']['has_specific_number_anchor']}  question={pe['opening']['has_engagement_question']}  story={pe['opening']['has_story_opener']}")
    print(f"  Closing: {pe['closing']['assessment']}")
    print(f"    cta={pe['closing']['has_cta']}  callback={pe['closing']['has_callback_to_opening']}  button={pe['closing']['has_emotional_button']}")
    print(f"  Peak moments (dramatic pauses in middle 40%): {pe['peak_moments']['peak_count']} detected")

    print("\n📖 STORYTELLING DENSITY")
    st = results["storytelling"]
    print(f"  Total narrative markers: {st['total_narrative_markers']}")
    print(f"  Per-segment rate: {st['narrative_per_segment']}")
    print(f"  Assessment: {st['assessment']}")

    print("\n🛡️ PSYCHOLOGICAL SAFETY")
    ps = results["psychological_safety"]
    print(f"  Markers detected: {ps['count']}")
    print(f"  {ps['assessment']}")

    print("\n💪 SELF-EFFICACY FRAMING")
    se = results["self_efficacy"]
    print(f"  Markers detected: {se['count']}")
    print(f"  {se['assessment']}")

    print("\n📣 CALLS TO ACTION")
    cta = results["ctas"]
    print(f"  Total CTAs: {cta['total_cta_count']}  |  In closing: {cta['closing_cta_count']}")
    print(f"  Assessment: {cta['assessment']}")

    if "repetition" in results and results["repetition"].get("counts"):
        print("\n🔁 THESIS REPETITION (mere exposure)")
        rep = results["repetition"]
        for phrase, count in sorted(rep["counts"].items(), key=lambda x: -x[1]):
            flag = "🔴" if count < 3 else ("⚠️" if count < 5 else "✅")
            print(f"  {flag}  \"{phrase}\"  ×{count}")
        print(f"  {rep['assessment']}")


def main():
    parser = argparse.ArgumentParser(description="Analyze psychological-design patterns in a talk.")
    parser.add_argument("transcript", help="Transcript JSON (from transcribe.py)")
    parser.add_argument("--config", default=None, help="Talk-specific config JSON for thesis phrases, CTAs, etc.")
    parser.add_argument("--output", default=None, help="Write results to JSON")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    path = Path(args.transcript)
    if not path.exists():
        sys.exit(f"ERROR: Transcript not found: {path}")

    with open(path) as f:
        data = json.load(f)

    segments = data["segments"]
    duration = data["duration"]

    # Load thesis phrases from config if provided
    thesis_phrases = []
    if args.config:
        with open(args.config) as f:
            cfg = json.load(f)
        # Use signature_phrases as thesis candidates, or a dedicated thesis_phrases key if provided
        thesis_phrases = cfg.get("thesis_phrases", cfg.get("signature_phrases", []))

    results = {
        "source_file": data.get("source_file", "unknown"),
        "duration_sec": duration,
        "cialdini": analyze_cialdini(segments),
        "peak_end": analyze_peak_end(segments, duration),
        "storytelling": analyze_storytelling(segments),
        "psychological_safety": analyze_psychological_safety(segments),
        "self_efficacy": analyze_self_efficacy(segments),
        "ctas": analyze_ctas(segments, duration),
        "repetition": analyze_repetition(segments, thesis_phrases),
    }

    output_path = args.output or str(path.with_name(path.stem.replace("-transcript", "") + "-psych.json"))
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    if not args.quiet:
        print_summary(results)
        print(f"\n✅ Psychological analysis written to: {output_path}")


if __name__ == "__main__":
    main()
