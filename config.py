import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Configuration with fallbacks and environment variable support
config = {
    # File paths (can be overridden with environment variables)
    'AUDIO_FILE': os.getenv('AUDIO_FILE', 'input/podcast.wav'),
    'TIMESTAMPS_FILE': os.getenv('TIMESTAMPS_FILE', 'input/timestamps.json'),
    'OUTPUT_DIR': os.getenv('OUTPUT_DIR', 'output'),
    
    # Video settings
    'VIDEO_FPS': int(os.getenv('VIDEO_FPS', 30)),
    'VIDEO_CODEC': os.getenv('VIDEO_CODEC', 'libx264'),
    'VIDEO_AUDIO_CODEC': os.getenv('VIDEO_AUDIO_CODEC', 'aac'),
    
    # Advanced encoding settings
    'ENCODING_PRESET': os.getenv('ENCODING_PRESET', 'medium'),  # Options: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
    'CRF_VALUE': os.getenv('CRF_VALUE', '23'),  # Constant Rate Factor (0-51, lower means better quality)
    'THREADS': int(os.getenv('THREADS', 4)),  # Number of threads to use for encoding
    
    # Logging settings
    'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO'),  # DEBUG, INFO, WARNING, ERROR, CRITICAL
}

# Ensure output directory exists
os.makedirs(config['OUTPUT_DIR'], exist_ok=True)