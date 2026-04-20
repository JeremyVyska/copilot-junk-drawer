#!/usr/bin/env python3
"""
transcribe.py — Run faster-whisper on a talk recording to produce a timestamped JSON.

Usage:
    python transcribe.py <input_audio> [output_json] [--model MODEL] [--device DEVICE]

Examples:
    python transcribe.py my-talk.m4a
    python transcribe.py my-talk.mp3 output.json
    python transcribe.py my-talk.wav --model medium.en --device cpu

Requirements:
    pip install faster-whisper

Output format: JSON with segments + word-level timestamps. Consumed by analyze.py.
"""
import argparse
import json
import sys
from pathlib import Path


def transcribe(input_path: str, output_path: str, model_size: str, device: str, compute_type: str):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit(
            "ERROR: faster-whisper not installed. Run:\n"
            "  pip install faster-whisper"
        )

    print(f"Loading model '{model_size}' on {device} ({compute_type})...")
    model = WhisperModel(model_size, device=device, compute_type=compute_type)

    print(f"Transcribing {input_path}...")
    segments_iter, info = model.transcribe(
        input_path,
        language="en",
        word_timestamps=True,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
    )

    output = {
        "source_file": input_path,
        "duration": info.duration,
        "language": info.language,
        "model": model_size,
        "segments": [],
    }

    seg_count = 0
    for seg in segments_iter:
        output["segments"].append({
            "start": round(seg.start, 2),
            "end": round(seg.end, 2),
            "text": seg.text.strip(),
            "words": [
                {"word": w.word, "start": round(w.start, 2), "end": round(w.end, 2)}
                for w in (seg.words or [])
            ],
        })
        seg_count += 1
        if seg_count % 50 == 0:
            print(f"  ...processed {seg_count} segments ({seg.end:.1f}s / {info.duration:.1f}s)")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    total_words = sum(len(s["words"]) for s in output["segments"])
    print(
        f"\nDone. "
        f"{seg_count} segments, {total_words:,} words, "
        f"{info.duration/60:.1f} min, "
        f"overall {total_words/(info.duration/60):.1f} WPM"
    )
    print(f"Output: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe a talk recording with word-level timestamps."
    )
    parser.add_argument("input", help="Input audio file (m4a, mp3, wav, etc.)")
    parser.add_argument(
        "output",
        nargs="?",
        default=None,
        help="Output JSON path (default: <input>-transcript.json)",
    )
    parser.add_argument(
        "--model",
        default="large-v3",
        help="Whisper model size (tiny, base, small, medium, large-v3). Default: large-v3",
    )
    parser.add_argument(
        "--device",
        default="auto",
        help="Device: cuda, cpu, auto. Default: auto",
    )
    parser.add_argument(
        "--compute-type",
        default=None,
        help="Compute type (float16, int8, int8_float16). Default: float16 for cuda, int8 for cpu",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        sys.exit(f"ERROR: Input file not found: {input_path}")

    output_path = args.output or str(input_path.with_name(input_path.stem + "-transcript.json"))

    # Sensible compute_type defaults
    if args.compute_type is None:
        compute_type = "float16" if args.device == "cuda" else "int8"
    else:
        compute_type = args.compute_type

    transcribe(str(input_path), output_path, args.model, args.device, compute_type)


if __name__ == "__main__":
    main()
