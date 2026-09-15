#!/usr/bin/env python3
"""
Batch generation script to synthesize all 5 parts of the script
using ElevenLabs 'eleven_v3' model with emotion tags and Voice ID TX3LPaxmHKxFdv7VOQHJ.
"""

import argparse
import sys
from pathlib import Path
from elevenlabs_client import ElevenLabsAudio, DEFAULT_VOICE_ID

MODEL_V3 = "eleven_v3"
PARTS = [
    ("part_1", "input/part_1.txt", "output/part_1.mp3"),
    ("part_2", "input/part_2.txt", "output/part_2.mp3"),
    ("part_3", "input/part_3.txt", "output/part_3.mp3"),
    ("part_4", "input/part_4.txt", "output/part_4.mp3"),
    ("part_5", "input/part_5.txt", "output/part_5.mp3"),
]


def generate_single_part(service: ElevenLabsAudio, part_name: str, input_file: str, output_file: str, voice_id: str, model_id: str, force: bool = False):
    input_path = Path(input_file)
    if not input_path.is_file():
        raise FileNotFoundError(f"Missing input file: {input_file}")

    output_path = Path(output_file)
    if not force and output_path.is_file() and output_path.stat().st_size > 1024:
        print(f"\n[{part_name.upper()}] Skipping (already exists: {output_path.stat().st_size / 1024:.1f} KB). Pass --force to re-generate.")
        return output_path

    text = input_path.read_text(encoding="utf-8")
    print(f"\n[{part_name.upper()}] Generating audio ({len(text)} characters) using {model_id}...")
    result_path = service.text_to_audio(
        text=text,
        output_path=output_file,
        voice_id=voice_id,
        model_id=model_id,
    )
    return result_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate audio for the 5 parts of the video script using ElevenLabs v3 model."
    )
    parser.add_argument(
        "-p",
        "--part",
        type=int,
        choices=[1, 2, 3, 4, 5],
        default=None,
        help="Specific part number to generate (1 to 5). If omitted, all parts are generated.",
    )
    parser.add_argument(
        "-v",
        "--voice-id",
        type=str,
        default=DEFAULT_VOICE_ID,
        help=f"Voice ID (default: {DEFAULT_VOICE_ID}).",
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default=MODEL_V3,
        help=f"Model ID to use (default: {MODEL_V3}).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-generation even if output file already exists.",
    )

    args = parser.parse_args()

    service = ElevenLabsAudio()
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    parts_to_run = PARTS
    if args.part is not None:
        idx = args.part - 1
        parts_to_run = [PARTS[idx]]

    print("=" * 60)
    print(f"ElevenLabs v3 Script Generator (Voice ID: {args.voice_id})")
    print(f"Model: {args.model}")
    print(f"Parts to process: {[p[0] for p in parts_to_run]}")
    print("=" * 60)

    generated_files = []
    for part_name, in_file, out_file in parts_to_run:
        try:
            res = generate_single_part(
                service=service,
                part_name=part_name,
                input_file=in_file,
                output_file=out_file,
                voice_id=args.voice_id,
                model_id=args.model,
                force=args.force,
            )
            generated_files.append(res)
        except Exception as e:
            print(f"Error generating {part_name}: {e}", file=sys.stderr)
            sys.exit(1)

    print("\n" + "=" * 60)
    print("Generation complete! Output files:")
    for f in generated_files:
        print(f" - {f} ({f.stat().st_size / 1024:.1f} KB)")
    print("=" * 60)


if __name__ == "__main__":
    main()
