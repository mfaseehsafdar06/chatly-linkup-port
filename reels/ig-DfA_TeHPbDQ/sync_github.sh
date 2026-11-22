#!/usr/bin/env bash
# Mirror this project into the public repo and push.  Usage: ./sync_github.sh "commit message"
set -e
SRC="$(cd "$(dirname "$0")" && pwd)"; REPO=/Users/faseeh/Developer/chatly-linkup-port
rsync -a --delete --exclude 'frames_*' --exclude 'ref24' --exclude 'f10' --exclude 'ref.mp4' --exclude '*.wav' \
  --exclude 'src/hi-1.png' --exclude 'src/crop.png' --exclude 'src/prev-1.png' --exclude '*.npy' --exclude '.DS_Store' \
  --exclude 'tmp/' --exclude 'node_modules/' "$SRC/" "$REPO/reels/ig-DfA_TeHPbDQ/"
cd "$REPO"; git add -A
if git diff --cached --quiet; then echo "nothing to push"; exit 0; fi
git -c user.name=Faseeh -c user.email=283697232+mfaseehsafdar06@users.noreply.github.com commit -q -m "${1:-Update}

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
T=$(gh auth token -u mfaseehsafdar06)
git -c credential.helper= -c credential.helper="!f(){ echo username=x-access-token; echo password=$T; };f" push -q origin main
git log --oneline -1
