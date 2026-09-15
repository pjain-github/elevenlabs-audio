#!/usr/bin/env python3
"""
ElevenLabs Audio CLI:
Provides easy command-line access to:
  1. text to audio (tts)
  2. audio to audio (sts)
  3. test (quick verification with minimal character consumption)
"""

import argparse
import sys
from pathlib import Path
from elevenlabs_client import (
    ElevenLabsAudio,
    DEFAULT_VOICE_ID,
    DEFAULT_TTS_MODEL,
    DEFAULT_STS_MODEL,
)


def handle_tts(args):
    service = ElevenLabsAudio()
    input_text = args.text
    input_file = args.file

    if not input_text and not input_file:
        default_file = Path("input/sample.txt")
        if default_file.is_file():
            input_file = str(default_file)
            print(f"No text specified. Using file: {default_file}")
        else:
            print("Error: Please provide text or an input file using --file or positional argument.", file=sys.stderr)
            sys.exit(1)

    result = service.text_to_audio(
        text=input_text,
        file_path=input_file,
        output_path=args.output,
        voice_id=args.voice_id,
        model_id=args.model,
    )
    print(f"Success! Generated: {result}")


def handle_sts(args):
    service = ElevenLabsAudio()
    input_file = args.input

    if not input_file:
        input_dir = Path("input")
        audio_files = sorted(
            [f for f in input_dir.glob("*") if f.suffix.lower() in [".mp3", ".wav", ".m4a", ".ogg", ".aac"]]
        )
        if audio_files:
            input_file = str(audio_files[0])
            print(f"No input audio specified. Found audio in input/: {input_file}")
        else:
            print("Error: Please specify source audio path or place an audio file in 'input/'.", file=sys.stderr)
            sys.exit(1)

    result = service.audio_to_audio(
        input_audio_path=input_file,
        output_path=args.output,
        voice_id=args.voice_id,
        model_id=args.model,
        remove_background_noise=args.remove_noise,
    )
    print(f"Success! Generated: {result}")


def handle_test(args):
    sample_text = args.text or "Hello from ElevenLabs!"
    print(f"Running quick test with text: '{sample_text}' ({len(sample_text)} chars)...")
    service = ElevenLabsAudio()
    output_tts = service.text_to_audio(
        text=sample_text,
        output_path="output/sample_tts.mp3",
        voice_id=args.voice_id,
    )
    print(f"[1/2] TTS test passed: {output_tts}")

    if not args.skip_sts:
        print("[2/2] Running STS test using generated TTS audio as input...")
        output_sts = service.audio_to_audio(
            input_audio_path=output_tts,
            output_path="output/sample_sts.mp3",
            voice_id=args.voice_id,
        )
        print(f"[2/2] STS test passed: {output_sts}")

    print("\nAll tests completed successfully!")


def main():
    parser = argparse.ArgumentParser(
        description="ElevenLabs Audio Toolkit: Text-to-Audio and Audio-to-Audio conversion."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # TTS Subcommand
    tts_parser = subparsers.add_parser("tts", help="Convert text or a text file into audio")
    tts_parser.add_argument(
        "text",
        type=str,
        nargs="?",
        default=None,
        help="Text string or path to a text file (.txt).",
    )
    tts_parser.add_argument(
        "-f",
        "--file",
        type=str,
        default=None,
        help="Path to an input text file (e.g., input/sample.txt).",
    )
    tts_parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Path for output audio file (e.g., output/speech.mp3).",
    )
    tts_parser.add_argument(
        "-v",
        "--voice-id",
        type=str,
        default=DEFAULT_VOICE_ID,
        help=f"Voice ID (default: {DEFAULT_VOICE_ID}).",
    )
    tts_parser.add_argument(
        "-m",
        "--model",
        type=str,
        default=DEFAULT_TTS_MODEL,
        help=f"Model ID (default: {DEFAULT_TTS_MODEL}).",
    )

    # STS Subcommand
    sts_parser = subparsers.add_parser("sts", help="Convert audio into another voice (Speech-to-Speech)")
    sts_parser.add_argument(
        "input",
        type=str,
        nargs="?",
        default=None,
        help="Path to source audio file (.mp3, .wav, etc., e.g., input/recording.mp3).",
    )
    sts_parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Path for output audio file (e.g., output/converted.mp3).",
    )
    sts_parser.add_argument(
        "-v",
        "--voice-id",
        type=str,
        default=DEFAULT_VOICE_ID,
        help=f"Voice ID (default: {DEFAULT_VOICE_ID}).",
    )
    sts_parser.add_argument(
        "-m",
        "--model",
        type=str,
        default=DEFAULT_STS_MODEL,
        help=f"Model ID (default: {DEFAULT_STS_MODEL}).",
    )
    sts_parser.add_argument(
        "--remove-noise",
        action="store_true",
        help="Remove background noise before conversion.",
    )

    # Test Subcommand
    test_parser = subparsers.add_parser("test", help="Run a quick test with minimal character usage")
    test_parser.add_argument(
        "--text",
        type=str,
        default="Hello from ElevenLabs!",
        help="Custom short text for test.",
    )
    test_parser.add_argument(
        "-v",
        "--voice-id",
        type=str,
        default=DEFAULT_VOICE_ID,
        help=f"Voice ID (default: {DEFAULT_VOICE_ID}).",
    )
    test_parser.add_argument(
        "--skip-sts",
        action="store_true",
        help="Skip speech-to-speech test and only run text-to-speech.",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "tts":
            handle_tts(args)
        elif args.command == "sts":
            handle_sts(args)
        elif args.command == "test":
            handle_test(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
