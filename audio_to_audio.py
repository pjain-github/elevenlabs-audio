#!/usr/bin/env python3
"""
Audio-to-Audio (Speech-to-Speech) conversion script using ElevenLabs API.
Voice ID: TX3LPaxmHKxFdv7VOQHJ (Liam) by default.
"""

import argparse
import sys
from pathlib import Path
from elevenlabs_client import ElevenLabsAudio, DEFAULT_VOICE_ID, DEFAULT_STS_MODEL


def main():
    parser = argparse.ArgumentParser(
        description="Convert an existing audio file into a different voice using ElevenLabs Speech-to-Speech."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        default=None,
        help="Path to the source audio file (.mp3, .wav, etc., e.g., input/recording.mp3).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Path to save the converted audio file (default: output/sts_<name>.mp3).",
    )
    parser.add_argument(
        "-v",
        "--voice-id",
        type=str,
        default=DEFAULT_VOICE_ID,
        help=f"ElevenLabs target voice ID (default: {DEFAULT_VOICE_ID}).",
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default=DEFAULT_STS_MODEL,
        help=f"Model ID to use (default: {DEFAULT_STS_MODEL}).",
    )
    parser.add_argument(
        "--remove-noise",
        action="store_true",
        help="Remove background noise before conversion.",
    )

    args = parser.parse_args()

    input_file = args.input
    if not input_file:
        # Search input/ for audio files (.mp3, .wav, .m4a, .ogg)
        input_dir = Path("input")
        audio_files = sorted(
            [f for f in input_dir.glob("*") if f.suffix.lower() in [".mp3", ".wav", ".m4a", ".ogg", ".aac"]]
        )
        if audio_files:
            input_file = str(audio_files[0])
            print(f"No input file specified. Found audio in input/: {input_file}")
        else:
            print("Error: Please specify an input audio file with --input or place an audio file in 'input/'.", file=sys.stderr)
            sys.exit(1)

    try:
        service = ElevenLabsAudio()
        result_path = service.audio_to_audio(
            input_audio_path=input_file,
            output_path=args.output,
            voice_id=args.voice_id,
            model_id=args.model,
            remove_background_noise=args.remove_noise,
        )
        print(f"Done! Converted audio file generated at: {result_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
