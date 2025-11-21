# Podcast Video Editor

A command-line tool that automates the creation of podcast videos with talking character animations. This tool intelligently combines character video clips with audio based on a timestamp file, handling looping and cutting to match each segment's exact duration.

## Features

- **Talking Character Animation**: Synchronizes character animations with podcast audio.
- **Intelligent Looping**: Automatically loops animations for segments longer than the original video.
- **Flexible Timestamp Formats**: Supports both JSON and TXT timestamp files.
- **Customizable Output**: Configure video resolution, FPS, codec, and more.
- **Robust Error Handling**: Detailed logging and error reporting.

## Getting Started

### Prerequisites

- Python 3.7+
- FFmpeg (must be installed and accessible in your system's PATH)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/podcast-video-editor.git
   cd podcast-video-editor
   ```

2. **Install the required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

### Directory Structure

- **`input/`**: Place your audio files, video clips, and timestamp files here.
- **`output/`**: The generated videos and logs will be saved in this directory.

### Usage

Run the tool from the command line. You can specify the audio, timestamps, and output file paths.

**Basic command:**

```bash
python main.py --audio input/podcast.wav --timestamps input/timestamps.json --output my-podcast.mp4
```

**Using a TXT timestamp file:**

```bash
python main.py --audio input/podcast.wav --timestamps input/transcript.txt --output my-podcast.mp4
```

## Configuration

You can configure the video editor using command-line arguments or environment variables.

### Command-Line Arguments

| Argument       | Description                                | Default  |
| -------------- | ------------------------------------------ | -------- |
| `--audio`      | Path to the audio file.                    | `None`   |
| `--timestamps` | Path to the timestamps file (JSON or TXT). | `None`   |
| `--output`     | Name of the output video file.             | `None`   |
| `--output-dir` | Directory for output files.                | `output` |

### Environment Variables

| Variable            | Description                             | Default   |
| ------------------- | --------------------------------------- | --------- |
| `AUDIO_FILE`        | Path to the audio file.                 | `None`    |
| `TIMESTAMPS_FILE`   | Path to the timestamps file.            | `None`    |
| `OUTPUT_DIR`        | Directory for output files.             | `output`  |
| `VIDEO_FPS`         | Frames per second for the output video. | `24`      |
| `VIDEO_CODEC`       | Video codec.                            | `libx264` |
| `VIDEO_AUDIO_CODEC` | Audio codec.                            | `aac`     |
| `ENCODING_PRESET`   | Encoding preset.                        | `medium`  |
| `CRF_VALUE`         | Constant Rate Factor for quality.       | `23`      |
| `THREADS`           | Number of threads for encoding.         | `4`       |
| `LOG_LEVEL`         | Logging level.                          | `INFO`    |

## Timestamp File Formats

The tool supports two formats for timestamps: a JSON file and a TXT file.

### JSON Format

The JSON file can be a list of segments or a dictionary mapping videos to time ranges.

**1. List of Segments:**

```json
[
  {
    "video": "input/character1.mov",
    "start": 0,
    "end": 21
  },
  {
    "video": "input/character2.mov",
    "start": 22,
    "end": 23
  }
]
```

**2. Dictionary Mapping:**

Time values can be in seconds (integer or float) or in `"MM:SS"` format.

```json
{
  "input/character1.mov": {
    "start_time": "00:00",
    "end_time": "00:21"
  },
  "input/character2.mov": {
    "start_time": "00:22",
    "end_time": "00:23"
  }
}
```

### TXT Format

The TXT file should contain one segment per line, with the video file path, start time, and end time separated by spaces.

```
input/character1.mov 0 21
input/character2.mov 22 23
```

## How It Works

The video editor processes each segment from the timestamp file to create a video clip with the correct duration.

1. **Calculate Duration**: The tool calculates the exact duration needed for each segment.
2. **Loop or Trim Video**:
   - If the segment is shorter than the animation, the animation is trimmed to the required length.
   - If the segment is longer, the animation is looped to match the segment's duration.
3. **Synchronize Audio**: The podcast audio is cut to match the segment's duration.
4. **Combine and Concatenate**: The audio and video are combined for each segment, and all segments are concatenated to create the final video.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

---

Made by Myophily, Assisted by Claude 3.7 sonnet, 2025
