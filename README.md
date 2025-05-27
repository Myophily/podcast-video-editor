# Podcast Video Automation Tool

A command-line tool that automates the creation of podcasts featuring talking character animations. The tool intelligently combines character video clips with audio based on a timestamp JSON file, properly handling looping and cutting to match each segment's exact duration.

## Key Features

- Synchronizes character animations with podcast audio
- Intelligently loops animations for segments longer than the original video
- Supports both timestamp formats:
  - List of segments with video path, start, and end
  - Dictionary mapping videos to timestamp ranges
- Robust error handling and logging
- Command-line interface with configurable options

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/podcast-automation.git
   cd podcast-automation
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```bash
python main.py
```

This will use the default configuration from `config.py`.

### Command-line Options

```bash
# TXT 파일 사용
python main.py --audio input/podcast.wav --timestamps input/transcript.txt --output podcast-video.mp4

# 기존 JSON 파일도 그대로 사용 가능
python main.py --audio input/podcast.wav --timestamps input/timestamps.json --output podcast-video.mp4
```

Available options:
- `--audio`: Path to the audio file
- `--timestamps`: Path to the timestamps JSON file
- `--output`: Name of the output video file
- `--output-dir`: Directory for output files

### Environment Variables

You can also set configuration options using environment variables:
- `AUDIO_FILE`: Path to the audio file
- `TIMESTAMPS_FILE`: Path to the timestamps JSON file
- `OUTPUT_DIR`: Directory for output files
- `VIDEO_FPS`: Frames per second for output video
- `VIDEO_CODEC`: Video codec (default: libx264)
- `VIDEO_AUDIO_CODEC`: Audio codec (default: aac)
- `ENCODING_PRESET`: Encoding preset (default: medium)
- `CRF_VALUE`: Constant Rate Factor for quality (default: 23)
- `THREADS`: Number of threads for encoding (default: 4)
- `LOG_LEVEL`: Logging level (default: INFO)

## Timestamp JSON Formats

The tool supports two formats for the timestamps.json file:

### Format 1: List of Segments

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

### Format 2: Dictionary Mapping

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

Time values can be in seconds (integer/float) or in "MM:SS" format.

## How It Works

For each segment in the timestamps file:

1. Calculate the exact duration needed
2. Check if the original animation is long enough:
   - If segment <= animation duration: Use just the required portion
   - If segment > animation duration:
     - Calculate full loops needed and remainder time
     - Create the necessary loops plus remainder
3. Cut the podcast audio to match the segment
4. Combine audio with the processed video
5. Concatenate all segments into the final output

## Logging

The tool creates detailed logs in the output directory, including:
- Information about loaded files
- Details on segment processing
- Warnings about potential issues
- Error messages with troubleshooting details

## Requirements

- Python 3.7+
- MoviePy 1.0.3+
- FFmpeg (installed and in PATH)
- Other dependencies in requirements.txt

## License

[MIT License](LICENSE)