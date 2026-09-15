"""
ElevenLabs Audio Service Client.
Supports:
1. Text to Audio (Text-to-Speech / TTS)
2. Audio to Audio (Speech-to-Speech / STS)
"""

import os
from pathlib import Path
from typing import Optional, Union, Iterator
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

# Load environment variables from .env
load_dotenv()

DEFAULT_VOICE_ID = "TX3LPaxmHKxFdv7VOQHJ"  # Liam
DEFAULT_TTS_MODEL = "eleven_multilingual_v2"
DEFAULT_STS_MODEL = "eleven_multilingual_sts_v2"
DEFAULT_OUTPUT_FORMAT = "mp3_44100_128"


class ElevenLabsAudio:
    """Wrapper around ElevenLabs SDK for Text-to-Audio and Audio-to-Audio conversion."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        default_voice_id: Optional[str] = None,
    ):
        self.api_key = (
            api_key
            or os.getenv("ELEVENLABS_KEY")
            or os.getenv("ELEVENLABS_API_KEY")
            or os.getenv("ELEVEN_API_KEY")
        )

        if not self.api_key:
            raise ValueError(
                "ElevenLabs API key not found. Please set ELEVENLABS_KEY, "
                "ELEVENLABS_API_KEY, or ELEVEN_API_KEY in your .env file or environment."
            )

        self.client = ElevenLabs(api_key=self.api_key, timeout=600.0)
        self.default_voice_id = (
            default_voice_id
            or os.getenv("ELEVENLABS_VOICE_ID")
            or DEFAULT_VOICE_ID
        )

    def text_to_audio(
        self,
        text: Optional[str] = None,
        file_path: Optional[Union[str, Path]] = None,
        output_path: Optional[Union[str, Path]] = None,
        voice_id: Optional[str] = None,
        model_id: str = DEFAULT_TTS_MODEL,
        output_format: str = DEFAULT_OUTPUT_FORMAT,
    ) -> Path:
        """
        Convert text or a text file into speech audio.

        :param text: Text string to synthesize (or file path if file exists).
        :param file_path: Path to a text file (.txt, .md) to read text from.
        :param output_path: File path where audio will be saved.
        :param voice_id: Voice ID (default: TX3LPaxmHKxFdv7VOQHJ).
        :param model_id: TTS model ID (default: eleven_multilingual_v2).
        :param output_format: Audio format (default: mp3_44100_128).
        :return: Path to saved audio file.
        """
        source_stem = None
        if file_path:
            fp = Path(file_path)
            if not fp.is_file():
                raise FileNotFoundError(f"Input text file not found: {file_path}")
            text = fp.read_text(encoding="utf-8")
            source_stem = fp.stem
        elif text:
            # If text string looks like a path (< 255 chars and no newlines) and matches an existing file, read from it
            if len(text) < 255 and "\n" not in text:
                try:
                    possible_path = Path(text)
                    if possible_path.is_file() and possible_path.suffix.lower() in [".txt", ".md", ".json", ".csv"]:
                        print(f"[TTS] Reading text from file: {possible_path}")
                        text = possible_path.read_text(encoding="utf-8")
                        source_stem = possible_path.stem
                except OSError:
                    pass

        if not text or not text.strip():
            raise ValueError("Input text cannot be empty.")

        target_voice_id = voice_id or self.default_voice_id

        if output_path is None:
            output_dir = Path("output")
            output_dir.mkdir(parents=True, exist_ok=True)
            if source_stem:
                output_path = output_dir / f"{source_stem}.mp3"
            else:
                output_path = output_dir / f"tts_{target_voice_id[:6]}_{abs(hash(text)) % 10000}.mp3"
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"[TTS] Synthesizing text ({len(text)} characters) with voice ID '{target_voice_id}' using model '{model_id}'...")
        audio_stream: Iterator[bytes] = self.client.text_to_speech.convert(
            voice_id=target_voice_id,
            text=text,
            model_id=model_id,
            output_format=output_format,
            request_options={"timeout_in_seconds": 600, "max_retries": 3},
        )

        temp_path = output_path.with_suffix(".tmp")
        try:
            with open(temp_path, "wb") as f:
                for chunk in audio_stream:
                    f.write(chunk)
            temp_path.replace(output_path)
        except Exception:
            if temp_path.exists():
                temp_path.unlink()
            raise

        file_size_kb = output_path.stat().st_size / 1024
        print(f"[TTS] Audio saved to: {output_path} ({file_size_kb:.1f} KB)")
        return output_path

    def audio_to_audio(
        self,
        input_audio_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
        voice_id: Optional[str] = None,
        model_id: str = DEFAULT_STS_MODEL,
        output_format: str = DEFAULT_OUTPUT_FORMAT,
        remove_background_noise: bool = False,
    ) -> Path:
        """
        Convert existing audio into another voice (Speech-to-Speech).

        :param input_audio_path: Path to source audio file (.mp3, .wav, etc.).
        :param output_path: File path where converted audio will be saved.
        :param voice_id: Target voice ID (default: TX3LPaxmHKxFdv7VOQHJ).
        :param model_id: STS model ID (default: eleven_multilingual_sts_v2).
        :param output_format: Audio format (default: mp3_44100_128).
        :param remove_background_noise: Whether to remove background noise before conversion.
        :return: Path to saved audio file.
        """
        input_path = Path(input_audio_path)
        if not input_path.is_file():
            raise FileNotFoundError(f"Input audio file not found: {input_audio_path}")

        target_voice_id = voice_id or self.default_voice_id

        if output_path is None:
            output_dir = Path("output")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"sts_{target_voice_id[:6]}_{input_path.stem}.mp3"
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"[STS] Converting '{input_path.name}' to voice ID '{target_voice_id}'...")
        with open(input_path, "rb") as audio_file:
            audio_stream: Iterator[bytes] = self.client.speech_to_speech.convert(
                voice_id=target_voice_id,
                audio=audio_file,
                model_id=model_id,
                output_format=output_format,
                remove_background_noise=remove_background_noise,
            )

            with open(output_path, "wb") as f:
                for chunk in audio_stream:
                    f.write(chunk)

        file_size_kb = output_path.stat().st_size / 1024
        print(f"[STS] Audio saved to: {output_path} ({file_size_kb:.1f} KB)")
        return output_path
