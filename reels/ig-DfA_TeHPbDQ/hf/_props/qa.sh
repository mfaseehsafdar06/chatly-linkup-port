#!/bin/zsh
# qa.sh <assetDir> <refStartFrame> <tag> "<post args>" j1 j2 ...   (j = frame index within the asset)
# renders stills, applies the post look in place, writes ref|ours pair sheets via hf/lib/compare.py (frame-exact).
D=$1; K0=$2; TAG=$3; PA=$4; shift 4
ROOT=/Users/faseeh/Developer/Chatly/reels/ig-DfA_TeHPbDQ; PY=/Users/faseeh/Developer/Chatly/reels/chatly-chatapps/.venv/bin/python
cd $ROOT
FR=$(echo $@ | tr ' ' ',')
node hf/lib/render.mjs $D 1 --frames $FR $EXTRA >/dev/null || exit 1
[ -n "$PA" ] && eval $PY hf/_props/post.py $D --stills $PA >/dev/null
TS=(); for j in $@; do TS+=($(echo "$j/24" | bc -l)); done
T0=$(echo "$K0/24-0.03" | bc -l)
$PY hf/lib/compare.py $D $T0 $TAG $TS
