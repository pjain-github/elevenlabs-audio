# ElevenLabs Audio Toolkit

A Python toolkit for generating and transforming audio using the **ElevenLabs API**.

## Features

- **Text to Audio (TTS)**: Convert text strings or `.txt` files into realistic speech audio using ElevenLabs models (default: `eleven_multilingual_v2`).
- **Audio to Audio (STS)**: Convert existing audio speech files into another voice using ElevenLabs Speech-to-Speech models (default: `eleven_multilingual_sts_v2`).
- **Input Folder**: Place any `.txt` file in `input/` to convert into audio, or drop audio files (`.mp3`, `.wav`) for Speech-to-Speech conversion.
- **Default Voice**: Configured to use Voice ID `TX3LPaxmHKxFdv7VOQHJ` (Liam).
- **Quota-conscious testing**: Included testing tools optimized to consume minimal characters.
- **Isolated Conda environment**: Configured with `environment.yml` targeting a local `./.venv` directory to protect global Python packages.

---

## Project Structure

```text
elevenlabs-audio/
├── environment.yml        # Conda environment specification
├── .env                   # API keys and environment configuration (ignored by git)
├── .env.example           # Example environment template
├── input/                 # Place your input files here (.txt files or audio files)
│   ├── .gitkeep
│   ├── sample.txt         # Sample text file
│   ├── part_1.txt         # Part 1 script with emotional audio tags
│   ├── part_2.txt         # Part 2 script with emotional audio tags
│   ├── part_3.txt         # Part 3 script with emotional audio tags
│   ├── part_4.txt         # Part 4 script with emotional audio tags
│   └── part_5.txt         # Part 5 script with emotional audio tags
├── output/                # Generated audio files (part_1.mp3 ... part_5.mp3)
│   └── .gitkeep
├── elevenlabs_client.py   # Core client wrapper for TTS and STS
├── text_to_audio.py       # Standalone Text-to-Audio script
├── audio_to_audio.py      # Standalone Audio-to-Audio (STS) script
├── generate_parts.py      # Batch generator for the 5-part script using eleven_v3
├── main.py                # Unified CLI entrypoint
├── test_audio.py          # Quick verification test (minimal quota usage)
└── README.md
```

---

## Setup & Installation

### 1. Prerequisites
Ensure you have [Conda](https://docs.conda.io/en/latest/) (Miniconda, Miniforge, or Anaconda) installed.

### 2. Create the Local Conda Environment (`./.venv`)
Create the environment directly inside the repository without affecting global Python packages:

```bash
conda env create --prefix ./.venv -f environment.yml
```

### 3. Activate the Environment
```bash
conda activate ./.venv
```

*(Alternatively, run scripts directly using `./.venv/bin/python`)*

### 4. Configure API Key
Create a `.env` file in the root directory (or copy from `.env.example`):

```bash
cp .env.example .env
```

Set your API key in `.env`:
```env
ELEVENLABS_KEY=sk_...
ELEVENLABS_VOICE_ID=TX3LPaxmHKxFdv7VOQHJ
```

> Note: The client automatically checks `ELEVENLABS_KEY`, `ELEVENLABS_API_KEY`, and `ELEVEN_API_KEY`.

---

## Quick Verification Test

To verify your installation and API key without overconsuming your character quota:

```bash
./.venv/bin/python test_audio.py
```

This runs a 6-character test (`Hello!`) and verifies both TTS and STS pipelines.

---

## Usage

### 1. Text to Audio (Text-to-Speech)

You can pass raw text directly or reference a text file from the `input/` folder.

#### Option A: Using an Input File (.txt)
Place any `.txt` file in `input/` (e.g. `input/sample.txt` or `input/article.txt`):

```bash
# Using main.py:
./.venv/bin/python main.py tts input/sample.txt
# Or with explicit flag:
./.venv/bin/python main.py tts -f input/sample.txt -o output/sample_audio.mp3

# Using text_to_audio.py:
./.venv/bin/python text_to_audio.py -f input/sample.txt
```

#### Option B: Passing Direct Text
```bash
# Using main.py:
./.venv/bin/python main.py tts "Hello, welcome to ElevenLabs audio generation." -o output/welcome.mp3

# Using text_to_audio.py:
./.venv/bin/python text_to_audio.py -t "Your text here" -o output/my_speech.mp3
```

**Options:**
- `text` / `-t`: Text string or path to a text file.
- `-f` / `--file`: Path to an input text file (e.g., `input/sample.txt`).
- `-o` / `--output`: Destination path (default: `output/<source_stem>.mp3` or `output/generated_tts.mp3`).
- `-v` / `--voice-id`: ElevenLabs Voice ID (default: `TX3LPaxmHKxFdv7VOQHJ`).
- `-m` / `--model`: Model ID (default: `eleven_multilingual_v2`).

---

### 2. Audio to Audio (Speech-to-Speech)

Convert an existing voice recording into the target voice while preserving tone and pacing:

Place your source audio in `input/` (e.g., `input/my_speech.mp3`) or specify its path:

#### Using `main.py`:
```bash
# Automatically finds audio file in input/ if not specified:
./.venv/bin/python main.py sts

# Or specify source explicitly:
./.venv/bin/python main.py sts input/my_speech.mp3 -o output/converted_speech.mp3
```

#### Using standalone script `audio_to_audio.py`:
```bash
./.venv/bin/python audio_to_audio.py -i input/my_speech.mp3 -o output/converted.mp3
```

**Options:**
- `-i` / `--input`: Path to the source audio file (.mp3, .wav, etc.). If omitted, detects audio in `input/`.
- `-o` / `--output`: Destination path (default: `output/sts_<name>.mp3`).
- `-v` / `--voice-id`: Target Voice ID (default: `TX3LPaxmHKxFdv7VOQHJ`).
- `-m` / `--model`: STS Model ID (default: `eleven_multilingual_sts_v2`).
- `--remove-noise`: Remove background noise before conversion.

---

### 3. Multi-Part Script Generation with Emotions (`eleven_v3`)

The ElevenLabs `eleven_v3` model natively supports expressive inline emotion tags (such as `[urgent]`, `[intense]`, `[skeptical]`, `[serious]`, `[pause]`, `[dramatic pause]`, `[disbelief]`, `[thoughtful]`, `[calm]`, `[confident]`, `[direct]`, and `[friendly]`).

All 5 parts of the YouTube video script are saved with emotional cues in `input/part_1.txt` through `input/part_5.txt`.

#### Generate all parts:
```bash
./.venv/bin/python generate_parts.py
```

#### Generate or re-generate a specific part:
```bash
# Generate only part 1:
./.venv/bin/python generate_parts.py --part 1

# Force re-generation of existing audio:
./.venv/bin/python generate_parts.py --part 2 --force
```

Outputs are automatically saved as `output/part_1.mp3` through `output/part_5.mp3`.

---

### 4. Python SDK Usage in Your Own Code

You can also import and use `ElevenLabsAudio` directly in your Python code:

```python
from elevenlabs_client import ElevenLabsAudio

# Initialize client (automatically loads .env)
service = ElevenLabsAudio()

# 1. Generate audio from a text file in input/
tts_file = service.text_to_audio(
    file_path="input/sample.txt",
    output_path="output/sample_output.mp3",
    voice_id="TX3LPaxmHKxFdv7VOQHJ"
)
print(f"Generated from file: {tts_file}")

# 2. Generate audio from direct text
tts_direct = service.text_to_audio(
    text="Hello, this is generated directly from Python code!",
    output_path="output/python_direct.mp3"
)
print(f"Generated: {tts_direct}")

# 3. Convert audio to audio
sts_file = service.audio_to_audio(
    input_audio_path="output/python_direct.mp3",
    output_path="output/python_converted.mp3",
    voice_id="TX3LPaxmHKxFdv7VOQHJ"
)
print(f"Converted: {sts_file}")
```

---

## License
MIT
