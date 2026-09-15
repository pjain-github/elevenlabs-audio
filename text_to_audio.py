#!/usr/bin/env python3
"""
Text-to-Audio generation script using ElevenLabs API.
Voice ID: TX3LPaxmHKxFdv7VOQHJ (Liam) by default.
"""

import argparse
import sys
from pathlib import Path
from elevenlabs_client import ElevenLabsAudio, DEFAULT_VOICE_ID, DEFAULT_TTS_MODEL


def main():
    parser = argparse.ArgumentParser(
        description="Generate speech audio from text using ElevenLabs API."
    )
    parser.add_argument(
        "-t",
        "--text",
        type=str,
        default=None,
        help="The text to convert to audio (or path to a .txt file).",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default=None,
        help="Path to an input text file (e.g., input/sample.txt).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Path to save the generated audio file (default: output/<filename>.mp3 or output/generated_tts.mp3).",
    )
    parser.add_argument(
        "-v",
        "--voice-id",
        type=str,
        default=DEFAULT_VOICE_ID,
        help=f"ElevenLabs voice ID (default: {DEFAULT_VOICE_ID}).",
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default=DEFAULT_TTS_MODEL,
        help=f"Model ID to use (default: {DEFAULT_TTS_MODEL}).",
    )

    args = parser.parse_args()

    # Determine input text / file
    input_file = args.file
    input_text = args.text

    if not input_file and not input_text:
        # Check if default input/sample.txt exists
        default_file = Path("input/sample.txt")
        if default_file.is_file():
            input_file = str(default_file)
            print(f"No text or file specified. Using default: {default_file}")
        else:
            input_text = "Hello! This is a test from ElevenLabs."

    try:
        service = ElevenLabsAudio()
        result_path = service.text_to_audio(
            text=input_text,
            file_path=input_file,
            output_path=args.output,
            voice_id=args.voice_id,
            model_id=args.model,
        )
        print(f"Done! Audio file generated at: {result_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
