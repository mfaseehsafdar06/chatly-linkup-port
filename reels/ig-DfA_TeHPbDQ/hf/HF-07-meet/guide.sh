#!/bin/bash
# extract reference frames (QA guide only) for an asset: guide.sh <assetDir> <shotStart> <dur>
# frame k  <->  ref time shotStart + k/24
D=$1; S=$2; T=$3; R=$(dirname "$0")/../../refs/ref.mp4
mkdir -p "$D/qa/guide"; rm -f "$D/qa/guide/"*.jpg
ffmpeg -v error -y -ss $(python3 -c "print($S+0.5/24)") -i "$R" -t $T -vf "fps=24,scale=1440:1080" -start_number 0 -q:v 3 "$D/qa/guide/g%04d.jpg"
ls "$D/qa/guide" | wc -l
