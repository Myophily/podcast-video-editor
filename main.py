import os
import argparse
import logging
import json
import sys
from datetime import datetime

from video_editor import VideoEditor
from config import config

def validate_json_file(file_path):
    """
    Validate that the JSON file is properly formatted.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        bool: True if valid, raises exception if invalid
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check if it's a list of segments or a dictionary of timestamps
        if isinstance(data, list):
            # Validate each segment has required fields
            for i, segment in enumerate(data):
                if not all(k in segment for k in ['video', 'start', 'end']):
                    raise ValueError(f"Segment {i} is missing required fields (video, start, end)")
        elif isinstance(data, dict):
            # Validate each timestamp entry
            for video_path, times in data.items():
                if not all(k in times for k in ['start_time', 'end_time']):
                    raise ValueError(f"Entry for {video_path} is missing required fields (start_time, end_time)")
        else:
            raise ValueError("JSON must be either a list of segments or a dictionary of timestamps")
            
        return True
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {str(e)}")

def check_file_exists(file_path, description):
    """Check if a file exists and raise an error if it doesn't."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{description} not found: {file_path}")
    return True

def main():
    """Main function to run the podcast video automation tool."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Podcast Video Automation Tool')
    parser.add_argument('--audio', help='Path to the audio file')
    parser.add_argument('--timestamps', help='Path to the timestamps JSON file')
    parser.add_argument('--output', help='Name of the output video file')
    parser.add_argument('--output-dir', help='Directory for output files')
    args = parser.parse_args()
    
    # Update config with command line arguments if provided
    if args.audio:
        config['AUDIO_FILE'] = args.audio
    if args.timestamps:
        config['TIMESTAMPS_FILE'] = args.timestamps
    if args.output_dir:
        config['OUTPUT_DIR'] = args.output_dir
    
    # Set up logging
    log_file = os.path.join(config['OUTPUT_DIR'], f"podcast_automation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    logging.basicConfig(
        level=getattr(logging, config['LOG_LEVEL']),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger(__name__)
    
    # Output file name (default or from args)
    output_filename = args.output or f"podcast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    
    try:
        # Validate inputs
        logger.info("Validating input files...")
        check_file_exists(config['AUDIO_FILE'], "Audio file")
        check_file_exists(config['TIMESTAMPS_FILE'], "Timestamps file")
        validate_json_file(config['TIMESTAMPS_FILE'])
        
        # Create video editor and generate video
        logger.info("Initializing video editor...")
        video_editor = VideoEditor(config)
        
        logger.info(f"Generating podcast video: {output_filename}")
        output_path = video_editor.create_final_video(output_filename)
        
        logger.info(f"Video created successfully! Output: {output_path}")
        print(f"\nSuccess! Your podcast video has been created at: {output_path}")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        print(f"\nError: {str(e)}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())