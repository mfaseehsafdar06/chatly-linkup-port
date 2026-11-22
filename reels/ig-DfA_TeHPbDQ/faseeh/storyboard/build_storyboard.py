# Storyboard of the 1122 rough cut (1122.mov + 1122.WAV) with graphics planned into the black gaps.
# Output: STORYBOARD-1122.jpg (labelled) + frames/NN_*.jpg (plain 1440x1080, 4:3 as the final edit).
import subprocess, os, json
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(ROOT, '..', '..')            # reels/ig-DfA_TeHPbDQ
MOV = os.path.join(ROOT, '..', 'footage', '1122.mov')
TMP = os.path.join(ROOT, 'tmp'); os.makedirs(TMP, exist_ok=True)
FR = os.path.join(ROOT, 'frames'); os.makedirs(FR, exist_ok=True)
HF = os.path.join(P, 'hf')

# kind: L = live shot in the cut, G = built graphic for a black gap, N = needs building / footage missing
# cx = 4:3 crop centre (fraction of 1920 width) for live shots
B = [
 ('L', 0.000, 1.633, 'This is my co-worker Faseeh.', 'L01 both, low angle outside', dict(t=0.8, cx=.5), 'word pops'),
 ('L', 1.633, 3.133, '...We both work at Chatly', 'L02 Faseeh at bench', dict(t=2.4, cx=.48), 'FASEEH name sticker (P-21)'),
 ('L', 3.133, 4.000, '...and I\'m trying to', 'L03 Faseeh in bushes', dict(t=3.55, cx=.5), 'word pops'),
 ('L', 4.000, 4.967, '...save his job.', 'L04 helmet, arms up', dict(t=4.5, cx=.62), 'word pops'),
 ('L', 4.967, 7.100, 'Faseeh, where\'s the 9am post?', 'L05 teammate on Meet', dict(t=6.0, cx=.42), '"where\'s the 9am post??" card (P-24b)'),
 ('L', 7.100, 8.233, 'Is it 9am?', 'L06 Faseeh on Meet', dict(t=7.7, cx=.5), ''),
 ('L', 8.233, 10.033, 'In San Francisco.', 'L07 teammate on Meet', dict(t=9.1, cx=.42), 'sticker -> "in SAN FRANCISCO" (P-24c, was New York)'),
 ('L', 10.033, 12.000, 'What the f***?  (PROFANITY)', 'L08 Faseeh facepalm on Meet', dict(t=11.0, cx=.5), 'bleep or swap audio'),
 ('G', 12.000, 16.250, 'Every morning, Faseeh has to post...', 'globe -> map, NY! (seg1923)', dict(src=f'{P}/seg1923/out/seg1923-real-v2-4x3.mp4', t=3.0), 'black gap 12.0-19.0'),
 ('G', 16.250, 19.000, '...New York, London and SF at the same time', 'map circles (P-25)', dict(src=f'{HF}/P-25-map/out/P-25-map.mp4', t=2.6), ''),
 ('L', 18.967, 20.633, 'Faseeh has an impossible task.', 'L09 FEEDER ACCOUNTS sign, field', dict(t=19.8, cx=.42), '"impossible task" pop'),
 ('L', 20.633, 23.667, 'He runs dozens of feeder accounts.', 'L10 scroll whip -> POSTING TIMES sign', dict(t=22.6, cx=.5), ''),
 ('L', 23.667, 25.200, 'Every one has its own niche,', 'L11 at monitor, "45" note', dict(t=24.4, cx=.55), ''),
 ('L', 25.200, 26.467, '...its own voice', 'L12 bean bag, laptop', dict(t=25.8, cx=.62), ''),
 ('L', 26.467, 28.100, '...and its own time zone.', 'L13 typing, over shoulder', dict(t=27.3, cx=.4), ''),
 ('G', 28.100, 29.600, '3 posts a day...', 'calculator (P-27, must read 360)', dict(src=f'{HF}/P-27-calculator/out/P-27-calculator.mov', t=1.4, alpha=1), 'black gap 28.1-34.0'),
 ('N', 29.600, 34.000, '...hooks, captions, hashtags. 360 posts a week.', 'TO BUILD: hooks/captions/hashtags + "360/week"', dict(), 'code, free'),
 ('L', 34.000, 35.800, 'What the hell?', 'L14 facepalm on laptop Meet', dict(t=34.9, cx=.42), '"what the hell?" word pop'),
 ('N', 35.800, 39.300, 'And he\'s not the only one...', 'P-14 window: NEEDS 3-4 clips of other people', dict(src=f'{HF}/P-14-not-the-only-one/out/P-14-not-the-only-one_preview.mp4', t=1.6), 'black gap 35.8-62.5'),
 ('G', 39.300, 42.000, 'A notes app full of prompts...', 'Notes app (P-12)', dict(src=f'{HF}/P-12-notes-app/out/P-12-notes-app.mp4', t=2.0), ''),
 ('G', 42.000, 45.400, '...copy, paste, rewrite 30 times a day', 'Google Doc (P-13)', dict(src=f'{HF}/P-13-google-doc/out/P-13-google-doc.mp4', t=2.8), ''),
 ('G', 45.400, 47.400, 'Let\'s just say, it doesn\'t scale.', 'Upload failed (P-11)', dict(src=f'{HF}/P-11-upload-failed/out/P-11-upload-failed.mov', t=1.0, alpha=1), ''),
 ('G', 47.400, 52.500, 'So I showed him the prompt library...', 'Prompt Library save (P-01)', dict(src=f'{HF}/P-01-library-save/out/P-01-library-save.mp4', t=3.2), ''),
 ('G', 52.500, 54.900, 'Type @ in any chat...', '@ sticker + @hook menu (P-30, P-02)', dict(src=f'{HF}/P-02-at-mention/out/P-02-at-mention.mp4', t=2.0), ''),
 ('G', 54.900, 59.100, 'Fill in the account, the niche...', 'Fill in the blanks (P-03)', dict(src=f'{HF}/P-03-fill-blanks/out/P-03-fill-blanks.mp4', t=2.6), ''),
 ('G', 59.100, 62.467, '...the whole team gets it.', 'Who can use it -> Everyone (P-04)', dict(src=f'{HF}/P-04-share-team/out/P-04-share-team.mp4', t=2.3), ''),
 ('L', 62.467, 65.533, 'Faseeh doesn\'t rewrite the same prompt...', 'L15 dancing on Meet', dict(t=63.6, cx=.5), ''),
 ('G', 65.533, 68.833, 'So if you\'re running 10 accounts or 50,', 'scroll ticks (P-28) + "10 or 50"', dict(src=f'{HF}/P-28-scroll-ticks/out/P-28-scroll-ticks.mp4', t=1.8), 'black gap 65.5-68.8'),
 ('L', 68.833, 72.100, 'comment PROMPTS and I\'ll send you...', 'L16 both at desk', dict(t=70.0, cx=.55), '"Comment PROMPTS" pops'),
 ('G', 72.100, 73.350, '(end card)', 'a Chatly story (P-05)', dict(src=f'{HF}/P-05-endcard/out/P-05-endcard.mov', t=1.1, alpha=1), ''),
 ('G', 73.350, 78.350, 'Chatly. AI that works 24/7 for you.', 'official outro 4:3', dict(src=f'{HF}/P-05-endcard/out/outro-4x3.mp4', t=3.5), ''),
]

def grab(src, t, out, vf=None, alpha=False):
    cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', src, '-frames:v', '1']
    if vf: cmd += ['-vf', vf]
    if alpha: cmd += ['-pix_fmt', 'rgba', out]
    else: cmd += ['-q:v', '2', out]
    subprocess.run(cmd, check=True)

PAPER = (246, 246, 243)
frames = []
for i, (k, a, b, vo, what, d, note) in enumerate(B, 1):
    out = os.path.join(FR, f'{i:02d}_{k}.jpg')
    if k == 'L':
        x0 = int(round(d['cx'] * 1920 - 720)); x0 = max(0, min(480, x0))
        grab(MOV, d['t'], out, vf=f'crop=1440:1080:{x0}:0')
    elif 'src' in d:
        if d.get('alpha'):
            png = os.path.join(TMP, f'{i:02d}.png'); grab(d['src'], d['t'], png, alpha=True)
            im = Image.open(png).convert('RGBA'); bg = Image.new('RGBA', im.size, PAPER + (255,))
            Image.alpha_composite(bg, im).convert('RGB').save(out, quality=92)
        else:
            grab(d['src'], d['t'], out)
    else:
        im = Image.new('RGB', (1440, 1080), (30, 30, 30)); g = ImageDraw.Draw(im)
        f = ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc', 64, index=1)
        g.multiline_text((720, 540), 'TO BUILD\n' + what.replace('TO BUILD: ', ''), font=f, fill=(235, 90, 90), anchor='mm', align='center', spacing=18)
        im.save(out, quality=92)
    frames.append(out)

# ---- labelled sheet ----
COLS, TW, TH = 5, 480, 360
CAP = 132; PAD = 14
rows = (len(B) + COLS - 1) // COLS
W = COLS * TW + (COLS + 1) * PAD; H = 90 + rows * (TH + CAP + PAD) + PAD
sheet = Image.new('RGB', (W, H), (18, 18, 20)); g = ImageDraw.Draw(sheet)
F = lambda s, bold=False: ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc', s, index=1 if bold else 0)
g.text((PAD, 22), 'This is Faseeh: 1122 rough cut + planned graphics   (4:3, 72.1 s VO + end card/outro)', font=F(34, True), fill='white')
g.text((PAD + 1420, 30), 'green = live in cut    blue = built graphic    red = missing', font=F(24), fill=(170, 170, 170))
COL = {'L': (60, 200, 110), 'G': (80, 140, 255), 'N': (235, 80, 80)}
for i, ((k, a, b, vo, what, d, note), fp) in enumerate(zip(B, frames)):
    r, c = divmod(i, COLS); x = PAD + c * (TW + PAD); y = 90 + r * (TH + CAP + PAD)
    sheet.paste(Image.open(fp).resize((TW, TH), Image.LANCZOS), (x, y))
    g.rectangle([x, y, x + TW - 1, y + TH - 1], outline=COL[k], width=5)
    g.rectangle([x, y, x + 66, y + 34], fill=COL[k]); g.text((x + 8, y + 4), f'{i+1:02d}', font=F(24, True), fill='black')
    ty = y + TH + 8
    g.text((x, ty), f'{a:05.2f}-{b:05.2f}s', font=F(21, True), fill=COL[k])
    g.text((x, ty + 28), vo[:46], font=F(21), fill='white')
    g.text((x, ty + 56), what[:48], font=F(19), fill=(190, 190, 190))
    if note: g.text((x, ty + 82), note[:50], font=F(19), fill=(240, 190, 90))
sheet.save(os.path.join(ROOT, 'STORYBOARD-1122.jpg'), quality=90)
json.dump([dict(n=i + 1, kind=k, start=a, end=b, vo=vo, shot=what, note=note) for i, (k, a, b, vo, what, d, note) in enumerate(B)],
          open(os.path.join(ROOT, 'storyboard-1122.json'), 'w'), indent=1)
print('ok', len(B), W, H)
