#!/usr/bin/env bash
# Re-download the reference reel and rebuild the frames the scripts read.
# Run from reels/ig-DfA_TeHPbDQ. Needs yt-dlp and ffmpeg.
set -e
cd "$(dirname "$0")"
yt-dlp -o "refs/ref.%(ext)s" "https://www.instagram.com/p/DfA_TeHPbDQ/"
mkdir -p refs/f10 seg1923/ref24
ffmpeg -v error -i refs/ref.mp4 -vf fps=10 -q:v 3 refs/f10/%04d.jpg              # 10 fps study frames
ffmpeg -v error -ss 19.0 -t 4.5 -i refs/ref.mp4 -vf fps=24 -start_number 0 seg1923/ref24/r%03d.png   # native frames for 19-23.5 s (compare.py, post2.py)
echo done
