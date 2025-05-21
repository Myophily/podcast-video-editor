from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import os
import json
import logging
from datetime import datetime
import time

class VideoEditor:
    def __init__(self, config):
        """
        Initialize the VideoEditor with the provided configuration.
        
        Args:
            config: Dictionary containing configuration parameters
        """
        self.config = config
        self.audio_file = config.get('AUDIO_FILE')
        self.timestamps_file = config.get('TIMESTAMPS_FILE')
        self.output_dir = config.get('OUTPUT_DIR')
        self.video_fps = config.get('VIDEO_FPS', 30)
        self.video_codec = config.get('VIDEO_CODEC', 'libx264')
        self.video_audio_codec = config.get('VIDEO_AUDIO_CODEC', 'aac')
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(self.output_dir, 'video_editor.log')),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize audio clip
        if not os.path.exists(self.audio_file):
            raise FileNotFoundError(f"Audio file not found: {self.audio_file}")
        
        self.audio_clip = AudioFileClip(self.audio_file)
        self.logger.info(f"Loaded audio file: {self.audio_file} (duration: {self.audio_clip.duration:.2f}s)")
        
        # Cache for video clips to avoid reloading
        self.video_cache = {}

    def load_segments(self):
        """
        Load and parse the timestamps file.
        
        Returns:
            list: List of segment dictionaries with video path, start and end times
        """
        if not os.path.exists(self.timestamps_file):
            raise FileNotFoundError(f"Timestamps file not found: {self.timestamps_file}")
            
        with open(self.timestamps_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check if the JSON format matches the specification format
        if isinstance(data, dict):
            # Convert specification format to internal format
            segments = []
            for video_path, times in data.items():
                # Handle time format (either "00:00" or numeric seconds)
                start = self._parse_time(times.get('start_time', times.get('start', 0)))
                end = self._parse_time(times.get('end_time', times.get('end', 0)))
                
                segments.append({
                    'video': video_path,
                    'start': start,
                    'end': end
                })
            # Sort segments by start time
            segments.sort(key=lambda x: x['start'])
            return segments
        elif isinstance(data, list):
            # Already in the expected format
            # Convert any time strings to seconds
            for segment in data:
                segment['start'] = self._parse_time(segment.get('start', 0))
                segment['end'] = self._parse_time(segment.get('end', 0))
            return data
        else:
            raise ValueError("Invalid timestamp format. Expected a list of segments or a dictionary mapping videos to timestamps.")

    def _parse_time(self, time_value):
        """
        Parse time values in various formats to seconds.
        
        Args:
            time_value: Time value in seconds (float/int) or string format "MM:SS"
            
        Returns:
            float: Time in seconds
        """
        if isinstance(time_value, (int, float)):
            return float(time_value)
        elif isinstance(time_value, str):
            # Handle "MM:SS" format
            if ':' in time_value:
                parts = time_value.split(':')
                if len(parts) == 2:
                    return int(parts[0]) * 60 + float(parts[1])
                elif len(parts) == 3:
                    return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
            # Try direct conversion
            return float(time_value)
        else:
            raise ValueError(f"Invalid time format: {time_value}")

    def get_video_clip(self, video_path):
        """
        Get a video clip, using cache if available.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            VideoFileClip: The loaded video clip
        """
        if video_path not in self.video_cache:
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Video file not found: {video_path}")
                
            self.video_cache[video_path] = VideoFileClip(video_path)
            self.logger.info(f"Loaded video: {video_path} (duration: {self.video_cache[video_path].duration:.2f}s)")
            
        return self.video_cache[video_path].copy()

    def process_segment(self, segment):
        """
        Process a single segment by cutting and looping video as needed.
        
        Args:
            segment: Dictionary with video path, start and end times
            
        Returns:
            VideoFileClip: Processed video clip with audio
        """
        video_path = segment['video']
        start_time = segment['start']
        end_time = segment['end']
        segment_duration = end_time - start_time
        
        # Skip invalid segments
        if segment_duration <= 0:
            self.logger.warning(f"Skipping segment with invalid duration: {segment}")
            return None
            
        # Get the base video clip
        try:
            video_clip = self.get_video_clip(video_path)
            video_duration = video_clip.duration
            
            # Process the video based on needed duration
            if segment_duration <= video_duration:
                # Use just a portion of the video
                processed_video = video_clip.subclip(0, min(segment_duration, video_duration))
                self.logger.info(f"Using {segment_duration:.2f}s portion of {video_path}")
            else:
                # Need to loop the video
                loops_needed = int(segment_duration // video_duration)
                remainder = segment_duration % video_duration
                
                self.logger.info(
                    f"Looping {video_path} {loops_needed} times with {remainder:.2f}s remainder "
                    f"for {segment_duration:.2f}s segment"
                )
                
                # Create loops plus remainder
                clips = [video_clip.copy() for _ in range(loops_needed)]
                if remainder > 0:
                    remainder_clip = video_clip.subclip(0, remainder)
                    clips.append(remainder_clip)
                
                processed_video = concatenate_videoclips(clips, method="compose")
            
            # Cut the audio segment
            audio_segment = self.audio_clip.subclip(start_time, end_time)
            
            # Set audio to video
            processed_video = processed_video.set_audio(audio_segment)
            
            return processed_video
            
        except Exception as e:
            self.logger.error(f"Error processing segment {segment}: {str(e)}")
            raise

    def create_final_video(self, output_filename):
        """
        Create the final video by processing all segments and concatenating them.
        
        Args:
            output_filename: Name of the output file
            
        Returns:
            str: Path to the created video
        """
        start_time = time.time()
        self.logger.info(f"Starting to create final video: {output_filename}")
        
        try:
            # Load segments
            segments = self.load_segments()
            self.logger.info(f"Loaded {len(segments)} segments from {self.timestamps_file}")
            
            # Process each segment
            processed_clips = []
            for i, segment in enumerate(segments):
                self.logger.info(f"Processing segment {i+1}/{len(segments)}: {segment}")
                processed_clip = self.process_segment(segment)
                if processed_clip is not None:
                    processed_clips.append(processed_clip)
            
            if not processed_clips:
                raise ValueError("No valid segments to process")
                
            # Concatenate all processed segments
            self.logger.info(f"Concatenating {len(processed_clips)} processed clips")
            final_clip = concatenate_videoclips(processed_clips, method="compose")
            
            # Write the final video
            output_path = os.path.join(self.output_dir, output_filename)
            self.logger.info(f"Writing final video to {output_path}")
            
            final_clip.write_videofile(
                output_path,
                fps=self.video_fps,
                codec=self.video_codec,
                audio_codec=self.video_audio_codec,
                threads=4,
                preset='medium',  # Better balance between speed and quality
                ffmpeg_params=['-crf', '23']  # Constant rate factor for quality
            )
            
            # Calculate and log total duration
            total_duration = sum(clip.duration for clip in processed_clips)
            self.logger.info(
                f"Video created successfully! Duration: {total_duration:.2f}s, "
                f"Processing time: {time.time() - start_time:.2f}s"
            )
            
            # Cleanup
            self.logger.info("Cleaning up resources")
            final_clip.close()
            for clip in processed_clips:
                clip.close()
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error creating final video: {str(e)}")
            raise
        finally:
            # Cleanup video cache
            self.close()

    def close(self):
        """Clean up all resources."""
        try:
            if hasattr(self, 'audio_clip') and self.audio_clip is not None:
                self.audio_clip.close()
                
            # Close all cached video clips
            for path, clip in self.video_cache.items():
                if clip is not None:
                    clip.close()
            self.video_cache.clear()
            
        except Exception as e:
            self.logger.error(f"Error closing resources: {str(e)}")