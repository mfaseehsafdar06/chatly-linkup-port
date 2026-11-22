#!/bin/zsh
# final_alpha.sh <assetDir> <frames> <outName> [paramsJSON]  -> render alpha frames, post look, ProRes 4444 out/<outName>.mov
ROOT=/Users/faseeh/Developer/Chatly/reels/ig-DfA_TeHPbDQ; PY=/Users/faseeh/Developer/Chatly/reels/chatly-chatapps/.venv/bin/python; cd $ROOT
D=$1; N=$2; NAME=$3; PRM=${4:-'{}'}
node hf/lib/render.mjs $D $(echo "$N/24" | bc -l) --alpha --params "$PRM" >/dev/null || exit 1
$PY hf/_props/post.py $D --alpha --vig 0 --tex .004 --edge .8 --soft .6 --grain 1.2 --name $NAME
rm -f $D/out/$(basename $D).mov.tmp
