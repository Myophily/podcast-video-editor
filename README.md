# Podcast Video Automation Tool

This tool automates the creation of podcast videos by synchronizing an audio track with specific video loops based on timestamps. It is designed to easily generate "visual podcast" style videos where different characters or avatars appear on screen corresponding to who is speaking.

## Example Videos

To see videos created using this tool, please visit: **[https://www.youtube.com/@pomato_potcast](https://www.youtube.com/@pomato_potcast)**

## Features

- **Automatic Synchronization**: Syncs audio segments with specific character videos.
- **Smart Looping**: Automatically loops short video clips to match the duration of the specific audio segment.
- **Multiple Input Formats**: Supports both structured JSON and simple TXT script files for defining timestamps.
- **Flexible Configuration**: Configure via command-line arguments or environment variables (`.env`).
- **Character Mapping**: Automatically maps character names from text scripts to video files.

## Installation

1.  **Clone the repository**

    ```bash
    git clone https://github.com/Myophily/podcast-video-editor.git
    cd podcast-video-editor
    ```

2.  **Install dependencies**
    Make sure you have Python installed (3.8+ recommended), then run:
    ```bash
    pip install -r requirements.txt
    ```
    _Note: This project uses `moviepy` which requires FFMPEG to be installed on your system._

## Usage

### Basic Command

Run the tool using `main.py`:

```bash
python main.py --audio input/podcast.wav --timestamps input/timestamps.txt --output output/final_video.mp4
```

### Command Line Arguments

- `--audio`: Path to the source audio file (e.g., `.wav`, `.mp3`).
- `--timestamps`: Path to the timestamps file (supports `.json` or `.txt`).
- `--output`: (Optional) Name of the output video file.
- `--output-dir`: (Optional) Directory to save the output files.

### Running with Defaults

If you configure your paths in `config.py` or use a `.env` file, you can simply run:

```bash
python main.py
```

## Input File Formats

### 1\. Text Format (`.txt`)

This format is useful for simple scripts. It parses standard script formats to determine timestamps and the active character.

**Format:**

```text
MM:SS Character Name
Dialogue or description...

MM:SS Another Character
Response dialogue...
```

**Example:**

```text
00:00 Speaking Potato
Hello everyone, welcome to the show.

00:15 Speaking Tomato
Thanks for having me!
```

**Character Mapping:**
By default, the tool looks for video files in the `input/` folder matching the character name (e.g., "Speaking Potato" -\> `input/Speaking Potato.mov`). You can customize this mapping in `video_editor.py` or rely on filename matching.

### 2\. JSON Format (`.json`)

Use this for precise control over video paths and exact start/end times.

**Format:**

```json
[
  {
    "video": "input/character_a.mov",
    "start": 0,
    "end": 15.5
  },
  {
    "video": "input/character_b.mov",
    "start": 15.5,
    "end": "end"
  }
]
```

- `start`/`end`: Can be in seconds (float) or "MM:SS" format.
- `"end"`: Use the string "end" to indicate the end of the audio file.

## Configuration

You can modify settings in `config.py` or create a `.env` file in the root directory to override defaults without changing the code.

**Available Environment Variables:**

| Variable          | Description                    | Default                 |
| :---------------- | :----------------------------- | :---------------------- |
| `AUDIO_FILE`      | Default input audio path       | `input/podcast.wav`     |
| `TIMESTAMPS_FILE` | Default timestamps file path   | `input/timestamps.json` |
| `OUTPUT_DIR`      | Output directory               | `output`                |
| `VIDEO_FPS`       | Frames per second for output   | `30`                    |
| `VIDEO_CODEC`     | Video codec                    | `libx264`               |
| `THREADS`         | Number of threads for encoding | `4`                     |
| `LOG_LEVEL`       | Logging verbosity              | `INFO`                  |

## Project Structure

- `main.py`: Entry point. Handles argument parsing, input validation, and orchestration.
- `video_editor.py`: Core logic. Handles video loading, segment processing, looping, and concatenation via `moviepy`.
- `config.py`: Configuration settings and environment variable loading.
- `requirements.txt`: Python package dependencies.

## Logging

Logs are generated in the output directory with the timestamp of the run (e.g., `podcast_automation_YYYYMMDD_HHMMSS.log`) and are also printed to the console.

---

Made by Myophily, Assisted by Claude sonnet 3.7, 2025
