# Create output directory if it doesn't exist
New-Item -ItemType Directory -Force -Path "output"

# First clip: 말하는 토마토.mov (0-21 seconds)
# This requires concatenating two full videos and one 1-second clip
ffmpeg -i "input/말하는 토마토.mov" -t 1 -c copy "output/clip1.mov"
ffmpeg -i "input/말하는 토마토.mov" -t 1 -c copy "output/clip2.mov"
ffmpeg -i "input/말하는 토마토.mov" -t 1 -c copy "output/clip3.mov"

# Create a file list for concatenation
@"
file 'clip1.mov'
file 'clip2.mov'
file 'clip3.mov'
"@ | Out-File -FilePath "output/filelist.txt" -Encoding utf8

# Concatenate the first three clips
ffmpeg -f concat -safe 0 -i "output/filelist.txt" -c copy "output/part1.mov"

# Second clip: 말하는 감자.mov (22-23 seconds)
ffmpeg -i "input/말하는 감자.mov" -t 1 -c copy "output/part2.mov"

# Third clip: 말하는 토마토.mov (24-32 seconds)
ffmpeg -i "input/말하는 토마토.mov" -t 1 -c copy "output/part3.mov"

# Create final file list
@"
file 'part1.mov'
file 'part2.mov'
file 'part3.mov'
"@ | Out-File -FilePath "output/final_list.txt" -Encoding utf8

# Concatenate all parts
ffmpeg -f concat -safe 0 -i "output/final_list.txt" -c copy "output/final_output.mov"

# Clean up temporary files
Remove-Item "output/clip*.mov", "output/part*.mov", "output/filelist.txt", "output/final_list.txt" 