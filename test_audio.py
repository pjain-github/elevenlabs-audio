#!/usr/bin/env python3
"""
Test script for verifying Text-to-Audio and Audio-to-Audio generation
using a minimal character count to avoid overconsuming API credits.
"""

from pathlib import Path
from elevenlabs_client import ElevenLabsAudio, DEFAULT_VOICE_ID


def run_tests():
    print("=" * 60)
    print("Testing ElevenLabs Audio Pipeline")
    print(f"Target Voice ID: {DEFAULT_VOICE_ID}")
    print("=" * 60)

    # 1. Initialize client
    service = ElevenLabsAudio()
    print(" Client initialized successfully.")

    # 2. Text to Audio test (short 6-character text to preserve quota)
    test_text = "Hello!"
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    tts_output = output_dir / "test_tts_sample.mp3"

    print(f"\n[Test 1/2] Text-to-Audio conversion with text: '{test_text}' ({len(test_text)} chars)...")
    tts_result = service.text_to_audio(
        text=test_text,
        output_path=tts_output,
        voice_id=DEFAULT_VOICE_ID,
    )
    assert tts_result.is_file(), f"TTS output file does not exist: {tts_result}"
    assert tts_result.stat().st_size > 0, "TTS output file is empty!"
    print(f" Text-to-Audio passed! File size: {tts_result.stat().st_size} bytes ({tts_result})")

    # 3. Audio to Audio test using the audio generated from Test 1
    sts_output = output_dir / "test_sts_sample.mp3"
    print(f"\n[Test 2/2] Audio-to-Audio (STS) conversion using '{tts_result.name}'...")
    sts_result = service.audio_to_audio(
        input_audio_path=tts_result,
        output_path=sts_output,
        voice_id=DEFAULT_VOICE_ID,
    )
    assert sts_result.is_file(), f"STS output file does not exist: {sts_result}"
    assert sts_result.stat().st_size > 0, "STS output file is empty!"
    print(f" Audio-to-Audio passed! File size: {sts_result.stat().st_size} bytes ({sts_result})")

    print("\n" + "=" * 60)
    print(" All tests passed successfully!")
    print(f"Generated samples available in: {output_dir.resolve()}")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
