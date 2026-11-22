#!/usr/bin/env python3
"""This is Faseeh: final picture compositor (1440x1080, 24 fps, 4:3).
The owner's rough cut (1122.mov) sets the timing; every black gap is filled with our HF graphics; live shots get the
HeyClicky warm grade (reels/chatly-chatapps/comp/grade.py); LinkUp-style word pops + subtitles; whip transitions.
Usage:  python compose.py            -> out/picture.mp4
        python compose.py --stills 0.8,6.2,...   -> tmp/stills/t*.png (QA)"""
import os, sys, json, subprocess, math
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(D, '..', '..')); HF = f'{R}/hf'
sys.path.insert(0, os.path.abspath(f'{R}/../chatly-chatapps/comp')); from grade import grade
W, H, FPS = 1440, 1080, 24
TOTAL = 78.35
HN = '/System/Library/Fonts/HelveticaNeue.ttc'
HAND = f'{D}/fonts/CoveredByYourGrace.ttf'

# ---------------------------------------------------------------- sources
class Seq:  # video file, random access by frame index (cached sequential reads)
    def __init__(s, path): s.cap = cv2.VideoCapture(path); s.n = int(s.cap.get(cv2.CAP_PROP_FRAME_COUNT)); s.pos = -1; s.last = None
    def frame(s, i):
        i = max(0, min(s.n - 1, i))
        if i == s.pos: return s.last
        if i != s.pos + 1: s.cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ok, f = s.cap.read()
        if not ok: return s.last
        s.pos, s.last = i, f; return f
class PNGs:  # alpha overlay as png sequence
    def __init__(s, d): s.d = d; s.files = sorted(os.listdir(d)); s.n = len(s.files); s.cache = {}
    def frame(s, i):
        i = max(0, min(s.n - 1, i))
        if i not in s.cache:
            if len(s.cache) > 90: s.cache.clear()
            s.cache[i] = cv2.imread(f'{s.d}/{s.files[i]}', cv2.IMREAD_UNCHANGED)
        return s.cache[i]
SRC = Seq(f'{D}/tmp/src24.avi'); PLATE = Seq(f'{D}/tmp/src24.avi')
def clip(p): return Seq(p)
G = {k: clip(v) for k, v in {
    'globe': f'{R}/seg1923/out/seg1923-real-v2-nowords-4x3.mp4', 'map': f'{HF}/P-25-map/out/P-25-map.mp4',
    'posts': f'{HF}/P-31-posts-math/out/P-31-posts-math.mp4', 'montage': f'{HF}/P-32-notes-montage/out/P-32-notes-montage.mp4',
    'notes': f'{HF}/P-12-notes-app/out/P-12-notes-app.mp4', 'doc': f'{HF}/P-13-google-doc/out/P-13-google-doc.mp4',
    'card': f'{HF}/P-29-prompt-cards/out/P-29a-blank-card-slide.mp4', 'lib': f'{HF}/P-01-library-save/out/P-01-library-save.mp4',
    'at': f'{HF}/P-02-at-mention/out/P-02-at-mention.mp4', 'fill': f'{HF}/P-03-fill-blanks/out/P-03-fill-blanks.mp4',
    'share': f'{HF}/P-04-share-team/out/P-04-share-team.mp4', 'scroll': f'{HF}/P-28-scroll-ticks/out/P-28-scroll-ticks.mp4',
    'outro': f'{HF}/P-05-endcard/out/outro-4x3.mp4', 'cards': f'{HF}/P-33-account-cards/out/P-33-account-cards.mp4'}.items()}
OV = {n: PNGs(f'{D}/tmp/ov/{n}') for n in os.listdir(f'{D}/tmp/ov')}
HOLE = {k: {e['frame']: np.float32(e['quad']) for e in json.load(open(f'{HF}/{k}/out/{k}-hole.json'))} for k in ('P-22-reportcard-fail', 'P-23-reportcard-pass')}

# ---------------------------------------------------------------- helpers
def live(t, cx=.5, zoom=1.0, cy=.5, src_t=None, seq=None):
    """graded 4:3 crop of the 1122 cut at source time src_t (default = t)"""
    seq = seq or SRC; i0 = int(round((t if src_t is None else src_t) * FPS)); f = seq.frame(i0)
    for d in (-1, 1, -2, 2, -3, 3):  # the rough cut has black gaps: never show a black source frame at a cut
        if f is not None and f.mean() > 10: break
        f = seq.frame(i0 + d)
    cw, ch = 1440 / zoom, 1080 / zoom
    x0 = min(max(0, cx * 1920 - cw / 2), 1920 - cw); y0 = min(max(0, cy * 1080 - ch / 2), 1080 - ch)
    if zoom == 1.0: return f[int(y0):int(y0) + 1080, int(x0):int(x0) + 1440].copy()
    M = np.float32([[zoom, 0, -x0 * zoom], [0, zoom, -y0 * zoom]]); return cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_CUBIC)
def gfx(k, lt, hold=True):
    s = G[k]; i = int(round(lt * FPS)); return s.frame(min(i, s.n - 1)).copy()
def over(base, rgba, dx=0, dy=0, sc=1.0, alpha=1.0):
    if rgba is None: return base
    if dx or dy or sc != 1.0:
        M = np.float32([[sc, 0, dx + W / 2 * (1 - sc)], [0, sc, dy + H / 2 * (1 - sc)]]); rgba = cv2.warpAffine(rgba, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
    a = rgba[..., 3:4].astype(np.float32) / 255 * alpha
    return (base.astype(np.float32) * (1 - a) + rgba[..., :3].astype(np.float32) * a).astype(np.uint8)
def paste_rgba(base, img, cx, cy):  # img RGBA (BGR order) centred at cx,cy
    h, w = img.shape[:2]; x0, y0 = int(round(cx - w / 2)), int(round(cy - h / 2))
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if xa >= xb or ya >= yb: return base
    sub = img[ya - y0:yb - y0, xa - x0:xb - x0]; a = sub[..., 3:4].astype(np.float32) / 255
    base[ya:yb, xa:xb] = (base[ya:yb, xa:xb] * (1 - a) + sub[..., :3] * a).astype(np.uint8); return base
def warp_plate(base, plate, quad):
    h, w = plate.shape[:2]; M = cv2.getPerspectiveTransform(np.float32([[0, 0], [w, 0], [w, h], [0, h]]), quad)
    wp = cv2.warpPerspective(plate, M, (W, H), flags=cv2.INTER_LINEAR); m = cv2.warpPerspective(np.full((h, w), 255, np.uint8), M, (W, H))
    m = (m.astype(np.float32) / 255)[..., None]; return (base * (1 - m) + wp * m).astype(np.uint8)
def meet_tile(t_src):  # Faseeh's Meet tile from the 1122 cut (inc. name label)
    f = PLATE.frame(int(round(t_src * FPS))); return f[196:878, 494:1432].copy()
def whip(img, amt, direction=1):  # horizontal motion streak + shift, amt 0..1
    if amt <= 0: return img
    L = int(10 + 150 * amt); k = np.zeros((1, L), np.float32); k[0, :] = 1 / L
    b = cv2.filter2D(img, -1, k, borderType=cv2.BORDER_REFLECT); sh = int(direction * 90 * amt)
    return np.roll(b, sh, axis=1)
def blur_dark(img, k=0.45, b=0):
    if b: img = cv2.GaussianBlur(img, (0, 0), b)
    return (img.astype(np.float32) * (1 - k)).astype(np.uint8)


# ---- screen treatment after the ref's app section (ref 42-58 s): photographed-screen look, sage-cream whites (L85 a-11 b+15),
# lifted blacks (~L30-45), softness, gentle handheld drift + eased punch-ins on the part that matters
def ease(x, a, b):
    u = min(1, max(0, (x - a) / (b - a))); return u * u * (3 - 2 * u)
_L = np.arange(256, dtype=np.float32)
_LUT_L = (np.clip(30 + .57 * (_L / 2.55), 0, 100) * 2.55).astype(np.uint8)
_yy, _xx = np.mgrid[0:H, 0:W]; _VIG = (1 - .14 * np.clip((np.sqrt(((_xx - W / 2) / (W * .6)) ** 2 + ((_yy - H / 2) / (H * .6)) ** 2) - .45) / .6, 0, 1) ** 1.6).astype(np.float32)[..., None]
def refscreen(img, soft=True):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB); L0 = lab[..., 0].astype(np.float32) / 2.55
    a = (lab[..., 1].astype(np.float32) - 128) * .8 - 3 - 8 * L0 / 100; b = (lab[..., 2].astype(np.float32) - 128) * .8 + 3 + 12 * L0 / 100
    out = cv2.cvtColor(np.dstack([_LUT_L[lab[..., 0]], np.clip(a + 128, 0, 255).astype(np.uint8), np.clip(b + 128, 0, 255).astype(np.uint8)]), cv2.COLOR_LAB2BGR)
    if soft: out = cv2.GaussianBlur(out, (0, 0), .7)
    return np.clip(out.astype(np.float32) * _VIG, 0, 255).astype(np.uint8)
def screen(img, t, z=1.0, cx=.5, cy=.5):
    dx = math.sin(t * 1.9) * 5 + math.sin(t * 4.7) * 1.8; dy = math.cos(t * 1.5) * 4 + math.sin(t * 3.9) * 1.4
    z = z * 1.03  # a hair of overscan so the drift never shows an edge
    tx = W / 2 - cx * W * z + dx; ty = H / 2 - cy * H * z + dy
    tx = min(0, max(W - W * z, tx)); ty = min(0, max(H - H * z, ty))
    img = cv2.warpAffine(img, np.float32([[z, 0, tx], [0, z, ty]]), (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return cv2.GaussianBlur(img, (0, 0), .55)


# ---- FINISH: one soft cinematic grade over the whole film (HeyClicky look, = chat-apps comp/grade.py, user-approved),
# plus a soft gradient: warm light falling from the top, gentle shade toward the bottom and corners.
import grade as _G
_gy, _gx = np.mgrid[0:H, 0:W].astype(np.float32)
_r = np.sqrt(((_gx - W / 2) / (W * .62)) ** 2 + ((_gy - H * .46) / (H * .72)) ** 2)
_FVIG = (1 - .16 * np.clip((_r - .45) / .6, 0, 1) ** 1.7)[..., None]
_top = np.clip(1 - _gy / (H * .75), 0, 1) ** 1.6 * np.clip(1.15 - np.abs(_gx - W * .38) / (W * .9), 0, 1)
_WARM = (_top[..., None] * np.float32([150, 205, 255]))            # BGR amber light
_BOT = (1 - .10 * np.clip((_gy - H * .55) / (H * .45), 0, 1) ** 1.4)[..., None]
# film grain: 24 pre-made fields (fine 35mm-like, ~1.3 px clumps, slight colour), a new one every frame, strongest in the mids
_rg = np.random.default_rng(1122); _GRAIN = []
for _i in range(24):
    n = _rg.normal(0, 1, (H, W)).astype(np.float32); n = cv2.GaussianBlur(n, (0, 0), .75); n /= n.std()
    c = cv2.GaussianBlur(_rg.normal(0, 1, (H // 2, W // 2, 3)).astype(np.float32), (0, 0), 1.0); c = cv2.resize(c, (W, H)); c /= c.std()
    _GRAIN.append((n[..., None] * .85 + c * .15).astype(np.float32))
GRAIN_AMT = 7.5
def grain(out, t):
    g = _GRAIN[int(round(t * FPS)) % 24]; L = out.mean(2, keepdims=True) / 255
    w = .55 + 1.8 * L * (1 - L)                                             # more in the mids, less in clipped whites/blacks
    return out + g * GRAIN_AMT * w
def finish(img, k=1.0, t=0.0):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB); Lc = lab[..., 0]
    a = lab[..., 1].astype(np.float32) - 128; b = lab[..., 2].astype(np.float32) - 128; sat = _G.SAT[Lc]
    a = a * sat + _G.DA[Lc]; b = b * sat + _G.DB[Lc]
    out = cv2.cvtColor(np.dstack([_G.L_LUT[Lc], np.clip(a + 128, 0, 255).astype(np.uint8), np.clip(b + 128, 0, 255).astype(np.uint8)]), cv2.COLOR_LAB2BGR).astype(np.float32)
    hi = np.clip((out.max(2, keepdims=True) - 180) / 75, 0, 1) * out; glow = cv2.GaussianBlur(hi, (0, 0), 22)
    out = 255 - (255 - out) * (1 - .10 * glow / 255)                       # lens bloom
    # soft film: mute skies/blues (HeyClicky never has a punchy blue), gentle Pro-Mist diffusion
    hsv = cv2.cvtColor(np.clip(out, 0, 255).astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
    hue = hsv[..., 0]; blue = np.exp(-((hue - 108) / 16) ** 2); hsv[..., 1] *= (1 - .38 * blue) * .94
    out = cv2.cvtColor(hsv.clip(0, 255).astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
    mist = cv2.GaussianBlur(out, (0, 0), 16); out = out * .86 + mist * .14
    out = 255 - (255 - out) * (1 - .15 * _WARM / 255)                      # warm top light (screen) - the soft gradient
    out = out * _BOT * _FVIG
    out = grain(out, t)
    if k < 1: out = img.astype(np.float32) * (1 - k) + out * k
    return np.clip(out, 0, 255).astype(np.uint8)

# ---------------------------------------------------------------- text + stickers
_tc = {}
def word_img(txt, size, italic=False, ui=False):
    key = (txt, size, italic, ui)
    if key in _tc: return _tc[key]
    F = ImageFont.truetype(HN, size, index=3 if italic else 1)
    bb = F.getbbox(txt); w, h = bb[2] - bb[0] + (64 if ui else 40), bb[3] - bb[1] + 40
    L = Image.new('L', (w, h), 0); ImageDraw.Draw(L).text(((32 if ui else 20) - bb[0], 20 - bb[1]), txt, font=F, fill=255)
    sh = L.filter(ImageFilter.GaussianBlur(4 if not ui else 6)); sh = Image.fromarray((np.array(sh) * (.45 if not ui else .8)).astype(np.uint8))
    out = np.zeros((h, w, 4), np.uint8); s = np.array(sh).astype(np.float32); s = np.roll(s, 2, 0)
    l = np.array(L).astype(np.float32)
    if ui:  # on light UI screens: near-black text on a soft white pill
        P = Image.new('L', (w, h), 0); ImageDraw.Draw(P).rounded_rectangle((4, 6, w - 4, h - 4), radius=(h - 10) // 2, fill=232)
        halo = np.array(P.filter(ImageFilter.GaussianBlur(2))).astype(np.float32)
        a = np.maximum(l, halo); col = np.where(a > 0, 28 * l / np.maximum(a, 1) + 252 * (1 - l / np.maximum(a, 1)), 0)
    else:
        a = np.maximum(l, s); col = np.where(a > 0, 255 * l / np.maximum(a, 1), 0)
    out[..., 0] = out[..., 1] = out[..., 2] = col.clip(0, 255).astype(np.uint8); out[..., 3] = a.clip(0, 255).astype(np.uint8)
    _tc[key] = (out, -bb[0] + 20, -bb[1] + 20, bb); return _tc[key]
def put_word(base, txt, x, y, size, italic=False, centre=False, ui=False):
    img, ox, oy, bb = word_img(txt, size, italic, ui); w = bb[2] - bb[0]; h = bb[3] - bb[1]
    left = x - w / 2 if centre else x; return paste_rgba(base, img, left + w / 2, y)
_sc = {}
def hand_sticker(txt, color, h=150, rot=0, font=None):
    key = (txt, color, h, rot, font)
    if key in _sc: return _sc[key]
    blank = Image.open(f'{D}/stk/blank-{color}.png').convert('RGBA'); F = ImageFont.truetype(font or HAND, int(h * (.62 if font else .78)))
    tw = ImageDraw.Draw(blank).textlength(txt, font=F); w = int(tw + 70)
    s = blank.resize((w, h)); T = Image.new('L', (w, int(h * 1.4)), 0); ImageDraw.Draw(T).text((35, h * .2), txt, font=F, fill=255, stroke_width=2, stroke_fill=255)
    T = T.resize((w, int(h * 1.4 * 1.15))).crop((0, int(h * .17), w, int(h * .17) + h)).filter(ImageFilter.GaussianBlur(.6))
    ink = Image.new('RGBA', (w, h), (36, 38, 44, 255)); s.paste(ink, (0, 0), T)
    pad = 30; c = Image.new('RGBA', (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    shadow = Image.new('RGBA', c.size, (0, 0, 0, 0)); a = s.split()[3].point(lambda v: int(v * .32)); shadow.paste((20, 18, 10, 255), (pad + 3, pad + 7), a)
    c = Image.alpha_composite(c, shadow.filter(ImageFilter.GaussianBlur(7))); c.alpha_composite(s, (pad, pad)); c = c.rotate(rot, Image.BICUBIC, expand=True)
    arr = cv2.cvtColor(np.array(c), cv2.COLOR_RGBA2BGRA); _sc[key] = arr; return arr
def png_sticker(path, w, rot=0):
    key = (path, w, rot)
    if key in _sc: return _sc[key]
    im = Image.open(path).convert('RGBA'); im = im.resize((w, int(w * im.height / im.width)), Image.LANCZOS)
    pad = 30; c = Image.new('RGBA', (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0)); sh = Image.new('RGBA', c.size, (0, 0, 0, 0))
    sh.paste((20, 18, 10, 255), (pad + 3, pad + 7), im.split()[3].point(lambda v: int(v * .32))); c = Image.alpha_composite(c, sh.filter(ImageFilter.GaussianBlur(7)))
    c.alpha_composite(im, (pad, pad)); c = c.rotate(rot, Image.BICUBIC, expand=True); arr = cv2.cvtColor(np.array(c), cv2.COLOR_RGBA2BGRA); _sc[key] = arr; return arr
def pop(base, img, t, t0, cx, cy, seed=1):
    d = (t - t0) * FPS
    if d < -1e-6: return base
    s = 1.18 if d < 1 else 1.06 if d < 2 else 1.0
    st = int(t * FPS) // 2; rng = np.random.default_rng(seed * 1000 + st); jx, jy = rng.uniform(-1.2, 1.2, 2)
    if s != 1.0: img = cv2.resize(img, None, fx=s, fy=s, interpolation=cv2.INTER_LINEAR)
    return paste_rgba(base, img, cx + jx, cy + jy)

# ---------------------------------------------------------------- captions
# W: word pops (t_in, t_out, text, x_left|None, y_centre, size, opts)
W_ = []
def w(t, t_out, txt, x, y, size=72, italic=False, centre=False, dark=False): W_.append((t, t_out, txt, x, y, size, italic, centre, dark))
w(0.00, 1.633, 'This', 470, 120); w(0.32, 1.633, 'is', 670, 210); w(0.46, 1.633, 'my', 790, 120); w(0.64, 1.633, 'co-worker', 900, 230)
w(1.74, 3.133, 'We', 140, 150); w(2.00, 3.133, 'both', 300, 260); w(2.30, 3.133, 'work', 1010, 140); w(2.56, 3.133, 'at', 1080, 250); w(2.70, 3.133, 'Chatly', 1040, 360, 92)
w(4.14, 4.967, 'HIS', 120, 330, 96); w(4.30, 4.967, 'JOB.', 1080, 330, 96)
w(5.66, 7.10, 'Faseeh,', 860, 150, 80)
w(7.22, 8.233, 'Is', 1040, 230); w(7.36, 8.233, 'it', 1135, 330); w(7.48, 8.233, '9am?', 1040, 440, 96)
w(10.24, 12.0, 'What', 160, 300, 90); w(10.72, 12.0, 'the', 230, 410, 90)
w(17.78, 18.967, 'same', 420, 920, 104); w(18.02, 18.967, 'time.', 720, 920, 104)
w(18.97, 20.633, 'Faseeh', 90, 300, 74); w(19.28, 20.633, 'has', 140, 400, 74); w(19.56, 20.633, 'an', 1120, 260, 74)
w(19.74, 20.633, 'impossible', 860, 860, 104); w(20.34, 20.633, 'task.', 1130, 960, 84)
w(21.64, 23.667, 'dozens', 1000, 200, 100)
w(34.16, 35.8, 'What', 140, 230, 96); w(34.54, 35.8, 'the', 160, 345, 96); w(34.80, 35.8, 'hell?', 960, 300, 132)
w(35.92, 37.3, "he's", 300, 470, 68); w(36.16, 37.3, 'not', 680, 330, 68); w(36.36, 37.3, 'the', 960, 560, 68)
w(36.52, 37.3, 'only', 420, 760, 68, True); w(36.74, 37.3, 'one.', 960, 760, 68)
w(45.52, 47.4, "let's", 120, 330, 72); w(45.82, 47.4, 'just', 190, 440, 72); w(45.98, 47.4, 'say…', 290, 560, 72)
w(46.38, 47.4, "it doesn't", 760, 770, 64); w(46.94, 47.4, 'scale.', 760, 880, 112)

w(64.62, 65.533, 'ANYMORE.', None, 960, 100, centre=True)
w(68.72, 69.46, 'Comment', 70, 150, 84)
w(69.46, 72.1, "and I'll send", 880, 760, 64); w(70.02, 72.1, 'you the exact one', 880, 830, 64); w(71.06, 72.1, 'Faseeh uses.', 880, 920, 84)
# S: subtitles (t_in, t_out, text, ui-style)
S_ = [(3.10, 3.90, "and I'm trying to save", 0), (11.90, 13.88, 'Every morning, Faseeh has to post.', 1), (14.02, 15.16, 'Except morning means', 1),
      (15.16, 17.14, 'New York, London and San Francisco', 1), (17.14, 17.78, 'at the', 1),
      (21.16, 23.06, 'He runs dozens of feeder accounts.', 0), (23.52, 25.36, 'Every one has its own niche,', 1), (25.52, 26.30, 'its own voice', 0),
      (26.30, 27.80, 'and its own time zone.', 0), (37.40, 39.28, 'Every social media marketer has this.', 0),
      (39.42, 41.25, 'A notes app full of prompts you copy,', 1), (41.42, 43.32, 'paste and rewrite 30 times a day,', 1), (43.60, 45.10, 'swapping one word each time.', 1),
      (47.52, 49.94, 'So I showed him the Prompt Library in Chatly.', 1), (50.24, 52.40, 'Write the prompt once and leave the blanks.', 1),
      (52.62, 54.86, 'Type @ in any chat and it’s right there.', 1), (54.86, 57.84, 'Fill in the account, the niche, the platform', 1),
      (57.84, 58.98, 'and it’s ready to send.', 1), (59.20, 60.64, 'And when he writes a good one,', 1), (60.82, 62.40, 'the whole team gets it.', 1),
      (62.48, 64.62, 'Faseeh doesn’t rewrite the same prompt 30 times', 0), (65.533, 66.30, "So if you're running", 1)]

# ---------------------------------------------------------------- stickers (code)
PHOTOS = []
PHOTO_SPEC = [  # owner's photos (Downloads 2026-11-23): file, rect on black (x0,y0,x1,y1), handle, sticker colour
    ('img02_15.07.42.jpeg', (330, 90, 1110, 1000), '@pawsdaily', 'pink'),
    ('img04_15.07.44.jpeg', (150, 170, 1290, 900), '@offroad.trails', 'yellow'),
    ('img05_15.07.45_(1).jpeg', (240, 120, 1240, 870), '@nightsout.live', 'blue'),
    ('img09_15.32.36.jpeg', (120, 210, 1320, 885), '@goldenhour.co', 'green'),
    ('img10_20.24.59.jpeg', (420, 70, 1060, 925), '@carspotting', 'yellow'),
    ('img01_15.04.46.jpeg', (200, 140, 1220, 905), '@ridersclub', 'pink')]
def build_photos():
    from PIL import ImageOps
    for f, (x0, y0, x1, y1), hk, col in PHOTO_SPEC:
        im = ImageOps.exif_transpose(Image.open(f'{R}/faseeh/footage/images-1123/{f}').convert('RGB'))
        im = ImageOps.fit(im, (x1 - x0, y1 - y0), Image.LANCZOS, centering=(.5, .45))
        PHOTOS.append((cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR), (x0, y0, x1, y1), 'ph_' + hk))
        STK['ph_' + hk] = hand_sticker(hk, col, 110, [-4, 3, -2, 4, -3, 2][len(PHOTOS) - 1])
STK = {}
def build_stickers():
    STK['sf'] = png_sticker(f'{R}/assets/cut/F-01_02_v1122.png', 640, -3)
    STK['bleep'] = hand_sticker('#@$%!', 'red', 170, 6, f'{D}/fonts/PermanentMarker.ttf')
    STK['acc10'] = hand_sticker('10 ACCOUNTS', 'yellow', 170, -4)
    STK['or50'] = hand_sticker('OR 50', 'pink', 190, 5)
    STK['prompts'] = hand_sticker('"PROMPTS"', 'yellow', 200, -3)
    for k, txt, col, h, r in [('s_rew', 'REWRITE', 'pink', 150, -4), ('s_30', '30x A DAY', 'yellow', 160, 3), ('s_one', 'ONE WORD', 'green', 150, -3),
                              ('s_lib', 'PROMPT LIBRARY', 'blue', 170, -3), ('s_blank', '{{ BLANKS }}', 'green', 160, 4),
                              ('s_acc', 'ACCOUNT', 'yellow', 140, -5), ('s_niche', 'NICHE', 'pink', 140, 4), ('s_plat', 'PLATFORM', 'blue', 140, -3),
                              ('s_send', 'SEND!', 'green', 150, 5), ('s_team', 'WHOLE TEAM', 'pink', 170, -4)]:
        STK[k] = hand_sticker(txt, col, h, r)

# ---------------------------------------------------------------- timeline
SCR_STK = [(41.86, 42.0, 's_rew', 1090, 760), (42.24, 45.4, 's_30', 1110, 230), (44.20, 45.4, 's_one', 380, 820),
           (48.66, 50.20, 's_lib', 880, 175), (51.56, 52.5, 's_blank', 1060, 820),
           (55.82, 57.84, 's_acc', 1170, 260), (56.66, 57.84, 's_niche', 1220, 420), (57.36, 57.84, 's_plat', 1150, 580),
           (58.68, 59.1, 's_send', 1210, 230), (61.26, 62.467, 's_team', 1080, 230)]
CUTS_WHIP = {12.0: 1, 18.967: -1, 28.1: 1, 62.467: -1, 65.533: 1}   # cut time -> direction
def frame_at(t):
    if t < 1.633:  img = live(t, .5)
    elif t < 3.133: img = live(t, .48)
    elif t < 4.0:    img = live(t, .5)
    elif t < 4.967:  img = live(t, .6)   # the owner's jump up from behind the plants
    elif t < 7.100:
        img = live(t, .42); lt = t - 6.04
        if lt >= 0: img = over(img, OV['P-24b-9am-card'].frame(int(lt * FPS)), dy=600, sc=.92)
    elif t < 8.233: img = live(t, .5)
    elif t < 10.033:
        img = live(t, .42); img = pop(img, STK['sf'], t, 9.22, 980, 850, 3)
    elif t < 12.0:
        img = live(t, .5); img = pop(img, STK['bleep'], t, 10.90, 1060, 800, 4)
    elif t < 16.25: img = gfx('globe', t - 12.0)
    elif t < 18.967: img = gfx('map', 15 / FPS + (t - 16.25))
    elif t < 20.633: img = live(t, .42)
    elif t < 23.667: img = live(t, .5)
    elif t < 25.2:   img = gfx('cards', t - 23.667)   # P-33: owner's photos as feeder-account cards on the globe poster
    elif t < 26.467: img = live(t, .62)
    elif t < 28.1:   img = live(t, .40)
    elif t < 34.0:   img = gfx('posts', t - 28.1)
    elif t < 35.8:   img = live(t, .42, zoom=1.0 if t < 34.80 else 1.22, cy=.45)
    elif t < 37.3:  # ref 'she's not the only one': small window on black
        img = np.zeros((H, W, 3), np.uint8); p = cv2.resize(meet_tile(10.25 + (t - 35.8)), (420, 315), interpolation=cv2.INTER_AREA)
        img[383:698, 510:930] = p
    elif t < 39.3:   img = gfx('montage', t - 37.3)
    elif t < 42.0:   img = screen(gfx('notes', t - 39.3), t, 1.0, .5, .5)
    elif t < 45.4:
        lt = t - 42.0; u = ease(lt, 2.3, 3.1); img = screen(gfx('doc', lt), t, 1 + 1.0 * u, .5 + (.47 - .5) * u, .5 + (.42 - .5) * u)
    elif t < 47.4:
        img = blur_dark(screen(gfx('doc', 99), t, 2.0, .47, .42), .58, 3); lt = t - 46.54
        if lt >= 0: img = over(img, OV['P-11-upload-failed'].frame(int(lt * FPS)), dx=40, dy=-40)
    elif t < 48.65:  img = screen(gfx('card', t - 47.4), t, 1.0, .5, .5)
    elif t < 52.5:
        lt = t - 48.65; u1 = ease(lt, 1.9, 2.4); u2 = ease(lt, 2.95, 3.4)
        z = 1 + .35 * u1 + (.55 - .35 * u1) * u2 if u2 > 0 else 1 + .35 * u1
        img = screen(gfx('lib', lt), t, z, .5 + (.47 - .5) * u1 + (.42 - .47) * u2, .5 + (.47 - .5) * u1 + (.36 - .47) * u2)
    elif t < 54.9:
        lt = t - 52.5; u = ease(lt, .5, 1.1); img = screen(gfx('at', lt), t, 1 + .45 * u, .5, .5 + .06 * u)
        if t >= 52.90: img = over(img, OV['P-30-at-sticker'].frame(int((t - 52.90) * FPS)))
    elif t < 59.1:
        lt = .35 + (t - 54.9); u = ease(lt, 3.2, 3.8); img = screen(gfx('fill', lt), t, 1 + .4 * u, .5 + (.36 - .5) * u, .5 + (.34 - .5) * u)
    elif t < 62.467:
        lt = t - 59.1; u = ease(lt, 2.4, 3.0); img = screen(gfx('share', lt), t, 1 + .2 * u, .5 + (.42 - .5) * u, .5 + (.42 - .5) * u)
    elif t < 64.3:   img = live(t, .5)
    elif t < 65.533:  # PASS card, the dance keeps going in the window
        i = 4 + int(round((t - 64.3) * FPS)); plate = live(t, .5)
        img = np.zeros((H, W, 3), np.uint8); img = warp_plate(img, plate, HOLE['P-23-reportcard-pass'][min(i, 76)])
        img = over(img, OV['P-23-reportcard-pass'].frame(i))
    elif t < 68.833:
        sc0 = gfx('scroll', t - 65.533); bg = np.full_like(sc0, sc0[540, 1420]); sm = cv2.resize(sc0, None, fx=.8, fy=.8, interpolation=cv2.INTER_AREA)
        img = bg.copy(); img[108:108 + sm.shape[0], 20:20 + sm.shape[1]] = sm
        img = pop(img, STK['acc10'], t, 66.34, 1130, 380, 5); img = pop(img, STK['or50'], t, 67.08, 1200, 600, 6)
    elif t < 72.1:
        img = live(t, .55); img = pop(img, STK['prompts'], t, 69.04, 800, 150, 7)
    elif t < 73.35:
        img = blur_dark(live(72.05, .55), .4, 6); img = over(img, OV['P-05-endcard'].frame(int((t - 72.1) * FPS)))
    else:            img = gfx('outro', t - 73.35)
    if t < 73.35: img = finish(img, t=t)
    # paper stickers slapped on the screens on the VO word (ref: LOCATION / WORKING ON / PRIORITIES / ANYTIME)
    for (t0, t1, k, cx, cy) in SCR_STK:
        if t0 - 1e-6 <= t < t1 - 1e-6: img = pop(img, STK[k], t, t0, cx, cy, hash(k) % 97)
    # whip transitions: 2 frames each side of listed cuts
    for tc, dr in CUTS_WHIP.items():
        d = (t - tc) * FPS
        if -2.5 < d < 2.5: img = whip(img, max(0, 1 - abs(d + .5) / 2.5), dr)
    # captions
    if t < 72.1:
        for (t0, t1, txt, x, y, size, it, ce, dk) in W_:
            if t0 - 1e-6 <= t < t1 - 1e-6: img = put_word(img, txt, x if x is not None else 720, y, size, it, ce or x is None, ui=dk)
        for (t0, t1, txt, ui) in S_:
            if t0 - 1e-6 <= t < t1 - 1e-6: img = put_word(img, txt, 720, 1000, 50, centre=True, ui=bool(ui))
    return img

if __name__ == '__main__':
    build_stickers()
    if '--stills' in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index('--stills') + 1].split(',')]; os.makedirs(f'{D}/tmp/stills', exist_ok=True)
        for t in ts: cv2.imwrite(f'{D}/tmp/stills/t{t:06.2f}.png', frame_at(t)); print('still', t)
        sys.exit()
    n = int(round(TOTAL * FPS)); out = f'{D}/out/picture.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-crf', '14', '-preset', 'medium', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for k in range(n):
        p.stdin.write(frame_at(k / FPS).tobytes())
        if k % 240 == 0: print(f'{k / FPS:.1f}s', flush=True)
    p.stdin.close(); p.wait(); print('wrote', out, n)
