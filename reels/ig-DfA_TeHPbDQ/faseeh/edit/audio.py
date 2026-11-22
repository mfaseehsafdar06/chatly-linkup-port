#!/usr/bin/env python3
"""This is Faseeh: sound mix, HeyClicky / chat-apps style (reels/chatly-chatapps/mix/audio_v5.py):
teammate VO (1122.WAV) + bleep on the f-word + messwave 'Lost in the Right Direction' (86 bpm) ~16 dB under the voice,
its drop (track 47.80) on 'So I showed him the prompt library' (47.52) + ~70 SFX, each = the object on screen + Chatly outro audio.
-> out/audio.wav (78.35 s)"""
import os, re, subprocess
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(f'{D}/../..')
P = os.path.abspath(f'{R}/../chatly-chatapps/audio-ref/picks'); S = os.path.abspath(f'{R}/../chatly-chatapps/mix/sfx')
VO = f'{R}/faseeh/footage/1122.WAV'; OUTRO = f'{R}/hf/P-05-endcard/out/outro-4x3.mp4'
MUS = f'{D}/music/ref_music.wav'   # ref reel's music stem (demucs no_vocals) - LICENCE CHECK before publishing
TOTAL = 78.35; OUT0 = 73.35; MLUFS = -21.0
BLEEP = (10.89, 11.31)
# (ref_start, ref_end, our_start, fade_in, fade_out): ref structure = intro | silence on the call | hits | 103 bpm cue | silence | quiet 136 | drop
BAR1, BAR2 = 4 * .580, 4 * .440
SEG = [(0.0, 5.0, 0.0, .02, .4),
       (12.5, 18.0, 18.967 - 5.5, .3, .02),
       (18.0, 18.0 + 3 * BAR1, 18.967, .02, .03), (18.0 + 2 * BAR1, 30.5, 18.967 + 3 * BAR1, .03, .35),
       (33.42, 33.42 + 4 * BAR2, 47.52 - 7 * BAR2, .25, .03), (33.42 + BAR2, 33.42 + 4 * BAR2, 47.52 - 3 * BAR2, .03, .03),
       (40.46, 40.46 + (OUT0 + .9 - 47.52), 47.52, .01, 1.2)]

C = [  # (time, file, dB after peak-normalising to -1 dBFS, [trim])
 (1.12, 'pop-box', -15), (1.60, 'swish-air-quick', -19),
 (3.633, 'card-slap-paper', -10), (4.22, 'stamp-rubber-thunk', -15), (4.36, 'stamp-rubber-thunk', -13),
 (4.95, 'phone-vibrate-on-table', -17, 1.0), (6.02, 'swish-ui-soft', -14), (6.10, 'notif-ding-phone-bright', -12),
 (7.48, 'pop-glassy-select', -18), (9.22, 'card-slap-paper', -12),
 (10.90, 'stamp-text-slam-heavy', -15),
 (11.93, 'whoosh-whip-fast', -11), (12.05, 'whoosh-heavy-rumble', -16), (12.2, 'paper-rustle-newspaper', -22, 1.2),
 (16.22, 'whip-snap-zoom-a', -15), (17.60, 'whoosh-zoom-mid', -15),
 (17.75, 'pop-glassy-select', -14), (17.92, 'pop-tiny-heart', -14), (18.08, 'pop-glassy-select', -14),
 (18.93, 'whip-swish-tight', -12), (19.74, 'orch-hit-dramatic', -15), (20.60, 'whoosh-whip-fast', -14), (21.64, 'pop-box', -16),
 (26.50, 'typing-keys-b', -20, 1.5),
 (28.06, 'whoosh-rising-bright', -15), (28.10, 'pop-box', -13), (28.22, 'pop-bubbly-ui', -13), (28.34, 'pop-tiny-heart', -13), (28.12, 'card-slap-paper', -14),
 (29.86, 'card-slap-paper', -12), (30.48, 'card-slap-paper', -12), (31.22, 'card-slap-paper', -11),
 (31.40, 'ticker-rapid-count', -15, 1.15), (31.45, 'rev-cymbal-into-drop', -13),
 (32.56, 'stamp-text-slam-heavy', -6), (32.58, 'punch-hit-whoosh', -11), (32.88, 'card-slap-paper', -12),
 (34.00, 'swish-air-quick', -16), (34.80, 'punch-hit-whoosh', -10), (34.82, 'meme-crowd-gasp-ooh', -17, 1.2),
 (35.80, 'thud-soft-object', -12),
 (37.30, 'whip-swish-tight', -17), (37.633, 'pop-box', -17), (37.967, 'whip-swish-tight', -18), (38.30, 'pop-bubbly-ui', -17), (38.633, 'whip-swish-tight', -18), (38.967, 'pop-box', -17),
 (39.35, 'typing-phone-fast', -19, 2.2), (42.05, 'typing-keys-b', -20, 2.6),
 (45.40, 'whoosh-zoom-mid', -18), (46.54, 'S:buzz', -13), (46.94, 'thud-soft-object', -13),
 (47.05, 'whoosh-rising-bright', -14), (47.40, 'paper-slide-desk', -13), (47.52, 'ui-burst-sparkle', -11),
 (48.65, 'swish-ui-soft', -16), (49.70, 'ui-click-crisp', -16), (50.10, 'typing-keys-b', -20, 1.3), (51.95, 'done-chime', -13),
 (52.50, 'swish-ui-soft', -16), (52.90, 'pop-box', -10), (53.30, 'typing-keys-b', -20, .6), (53.95, 'swish-ui-soft', -15), (54.40, 'ui-click-crisp', -16),
 (54.90, 'swish-ui-soft', -16), (55.30, 'typing-keys-b', -20, 2.6), (58.60, 'send-whoop', -10),
 (59.10, 'swish-ui-soft', -16), (59.90, 'ui-click-crisp', -15), (60.55, 'toggle-switch-on', -11, .45), (61.30, 'done-chime', -12),
 (62.43, 'whoosh-whip-fast', -12), (62.60, 'sparkle-glitter', -15),
 (64.30, 'card-slap-paper', -9), (64.62, 'notif-ding-positive', -11),
 (65.50, 'whoosh-zoom-mid', -14), (65.75, 'S:tick', -17), (66.05, 'S:tick', -17), (66.34, 'card-slap-paper', -16), (66.65, 'S:tick', -17), (67.08, 'card-slap-paper', -17), (67.30, 'S:tick', -17),
 (68.80, 'swish-air-quick', -15), (69.04, 'stamp-rubber-thunk', -10),
 (72.10, 'glass-shimmer-flash', -13)]

def fpath(n):
    if n.startswith('S:'): n = n[2:]; d = S
    else: d = P
    return next(f'{d}/{f}' for f in os.listdir(d) if f.rsplit('.', 1)[0] == n)
PEAK = {}
for c in C:
    if c[1] in PEAK: continue
    o = subprocess.run(['ffmpeg', '-hide_banner', '-i', fpath(c[1]), '-af', 'volumedetect', '-f', 'null', '-'], capture_output=True, text=True).stderr
    PEAK[c[1]] = float(re.search(r'max_volume: (\S+) dB', o).group(1))
def expr(keys):
    return '+'.join(f"between(t,{t0},{t1})*pow(10,({v0}+({v1}-({v0}))*(t-{t0})/{max(t1 - t0, 1e-3)})/20)" for (t0, v0), (t1, v1) in zip(keys, keys[1:]))
b0, b1 = BLEEP
bg = [f"[0:a]aresample=48000,aformat=channel_layouts=stereo,asplit={len(SEG)}" + ''.join(f'[m{i}]' for i in range(len(SEG)))]
bg += [f"[m{i}]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d={fi},afade=t=out:st={b - a - fo:.3f}:d={fo},adelay={int(o * 1000)}|{int(o * 1000)}[mm{i}]" for i, (a, b, o, fi, fo) in enumerate(SEG)]
bg += [''.join(f'[mm{i}]' for i in range(len(SEG))) + f"amix=inputs={len(SEG)}:normalize=0,apad=whole_dur={TOTAL:.3f},atrim=0:{TOTAL:.3f}[bed]"]
BED = f'{D}/tmp/music_bed.wav'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', MUS, '-filter_complex', ';'.join(bg), '-map', '[bed]', BED], check=True)
o = subprocess.run(['ffmpeg', '-hide_banner', '-i', BED, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', o)[-1]); MG = MLUFS - I; print('music bed', I, 'LUFS -> gain', round(MG, 2))
inputs = ['-i', VO, '-i', BED, '-i', OUTRO, '-f', 'lavfi', '-i', f'sine=frequency=1000:sample_rate=48000:duration={b1 - b0:.3f}'] + sum((['-i', fpath(c[1])] for c in C), [])
g = [f"[0:a]aresample=48000,aformat=channel_layouts=stereo,highpass=f=80,asplit=2[v1][v2]", f"[v1]atrim=0:{b0},afade=t=out:st={b0 - .03:.3f}:d=0.03[va]",
     f"[v2]atrim=start={b1},asetpts=PTS-STARTPTS,afade=t=in:d=0.02[vb]", f"aevalsrc=0|0:d={b1 - b0:.3f}:s=48000[vz]",
     f"[va][vz][vb]concat=n=3:v=0:a=1,loudnorm=I=-16:TP=-2:LRA=9,aresample=48000,apad=whole_dur={TOTAL:.3f},atrim=0:{TOTAL:.3f},asplit=3[vo][sc1][sc2]",
     f"[3:a]volume=-15dB,afade=t=in:d=0.01,afade=t=out:st={b1 - b0 - .02:.3f}:d=0.02,adelay={int(b0 * 1000)}|{int(b0 * 1000)},aformat=channel_layouts=stereo[bl]",
     f"[1:a]volume={MG:.2f}dB[mus0]",
     "[mus0][sc1]sidechaincompress=threshold=0.08:ratio=2.2:attack=30:release=450[mus]",
     f"[2:a]aresample=48000,aformat=channel_layouts=stereo,volume=-3dB,adelay={int(OUT0 * 1000)}|{int(OUT0 * 1000)}[out0]"]
for i, c in enumerate(C):
    t, n, db = c[:3]; trim = c[3] if len(c) > 3 else None; ms = int(round(t * 1000)); gain = db + (-1 - PEAK[n])
    tr = f"atrim=0:{trim},afade=t=out:st={max(0, trim - .25):.2f}:d=0.25," if trim else ''
    g.append(f"[{i + 4}:a]{tr}aresample=48000,aformat=channel_layouts=stereo,volume={gain:.2f}dB,adelay={ms}|{ms}[s{i}]")
g.append(''.join(f'[s{i}]' for i in range(len(C))) + f"[bl]amix=inputs={len(C) + 1}:normalize=0,apad=whole_dur={TOTAL:.3f}[sfx0]")
g.append("[sfx0][sc2]sidechaincompress=threshold=0.06:ratio=2:attack=10:release=250[sfx]")
g.append(f"[vo][mus][sfx][out0]amix=inputs=4:normalize=0,atrim=0:{TOTAL:.3f},afade=t=out:st={TOTAL - .4:.2f}:d=0.4,alimiter=limit=0.89,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[out]")
OUT = f'{D}/out/audio.wav'
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', ';'.join(g), '-map', '[out]', '-ac', '2', OUT], check=True)
print(OUT, len(C), 'cues')
