# Pixel fixes on the hand-drawn sticker cutouts so they match the 1122 VO (no paid regeneration).
#   =630 -> =360 (swap the real 6 and 3 glyphs), in NEW YORK -> in SAN FRANCISCO, +5 -> -8 (map sticker for SF),
#   scroll: @STUDYHACKS.PK [PK] -> @STUDYHACKS [UK]  (no South Asian markers).  Writes assets/cut/*_v1122.png
import numpy as np, cv2, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = os.path.dirname(os.path.abspath(__file__)); C = os.path.join(D, '..', '..', 'assets', 'cut')
FONT = os.path.join(D, 'fonts', 'CoveredByYourGrace.ttf')
rd = lambda n: np.array(Image.open(f'{C}/{n}.png').convert('RGBA'))
def ink_mask(a):  # dark marker ink inside the sticker
    rgb = a[..., :3].astype(int); return ((rgb.max(2) < 110) & (a[..., 3] > 128)).astype(np.uint8)
def erase(a, m, grow=5):
    m = cv2.dilate(m, np.ones((grow, grow), np.uint8)); bgr = cv2.cvtColor(a[..., :3], cv2.COLOR_RGB2BGR)
    out = cv2.inpaint(bgr, m * 255, 7, cv2.INPAINT_TELEA); a = a.copy(); a[..., :3] = cv2.cvtColor(out, cv2.COLOR_BGR2RGB); return a
def cols(m):  # x-runs of ink columns -> glyph spans
    c = m.sum(0) > 0; spans = []; x = 0
    while x < len(c):
        if c[x]:
            s = x
            while x < len(c) and c[x]: x += 1
            spans.append([s, x])
        x += 1
    return spans
def hand_text(a, txt, box, size, sy=1.22, ink=(38, 40, 46), seed=1):
    """draw txt in a hand font into box (x0,y0,x1,y1), letters slightly jittered, stretched vertically by sy"""
    x0, y0, x1, y1 = box; W, H = x1 - x0, y1 - y0; rng = np.random.default_rng(seed)
    F = ImageFont.truetype(FONT, size); L = Image.new('L', (W * 2, H * 2), 0); g = ImageDraw.Draw(L)
    x = 10
    for ch in txt:
        if ch == ' ': x += size * .28; continue
        g.text((x, H * .5 + rng.uniform(-3, 3)), ch, font=F, fill=255); x += g.textlength(ch, font=F) * .96
    bb = L.getbbox(); L = L.crop(bb); L = L.resize((L.width, int(L.height * sy)), Image.LANCZOS)
    k = min(W / L.width, H / L.height); L = L.resize((int(L.width * k), int(L.height * k)), Image.LANCZOS)
    L = L.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(.7))
    ox, oy = x0 + (W - L.width) // 2, y0 + (H - L.height) // 2
    m = np.array(L).astype(np.float32)[..., None] / 255; reg = a[oy:oy + L.height, ox:ox + L.width, :3].astype(np.float32)
    a[oy:oy + L.height, ox:ox + L.width, :3] = (reg * (1 - m) + np.array(ink) * m).astype(np.uint8); return a

# 1) =630 -> =360
a = rd('F-01_07'); m = ink_mask(a)
n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.dilate(m, np.ones((3, 3), np.uint8)))
big = sorted([i for i in range(1, n) if st[i, 4] > 800 and st[i, 0] > 200], key=lambda i: st[i, 0])  # skip the '=' bars
print('630 glyphs', [tuple(st[i, :4]) for i in big])
i6, i3 = big[0], big[1]
def glyph(i):
    x, y, w, h = st[i, :4]; mk = ((lab == i) & (m > 0)).astype(np.float32)[y:y + h, x:x + w]
    return a[y:y + h, x:x + w].copy(), cv2.GaussianBlur(mk, (3, 3), 0)[..., None], x, y, w, h
G6, G3 = glyph(i6), glyph(i3)
b = erase(a, (((lab == i6) | (lab == i3)) & (m > 0)).astype(np.uint8), 7)
def paste(b, G, x, y):
    reg, mk, _, _, w, h = G; b[y:y + h, x:x + w, :3] = (b[y:y + h, x:x + w, :3] * (1 - mk) + reg[..., :3] * mk).astype(np.uint8)
x6, x3 = G6[2], G3[2]; gap = x3 - (x6 + G6[4])
paste(b, G3, x6, G3[3]); paste(b, G6, x6 + G3[4] + gap, G6[3])
Image.fromarray(b).save(f'{C}/F-01_07_v1122.png')

# 2) in NEW YORK -> in SAN FRANCISCO (widen the blue sticker by stretching its middle)
a = rd('F-01_02'); m = ink_mask(a); sp = [s for s in cols(m) if s[1] - s[0] > 4]
print('NY spans', sp)
in_end = sp[1][1] if sp[1][0] - sp[0][1] < 25 else sp[0][1]       # 'i' + 'n'
ys, xs = np.where(m[:, in_end + 10:]); ty0, ty1 = ys.min(), ys.max()
b = erase(a, np.pad(m[:, in_end + 6:], ((0, 0), (in_end + 6, 0))))
H, W = b.shape[:2]; xa, xb = int(W * .45), int(W * .75); add = int(W * .55)
mid = cv2.resize(b[:, xa:xb], (xb - xa + add, H), interpolation=cv2.INTER_LINEAR)
b = np.concatenate([b[:, :xa], mid, b[:, xb:]], 1)
b = hand_text(b, 'SAN FRANCISCO', (in_end + 22, ty0 - 4, b.shape[1] - 40, ty1 + 6), 150, seed=3)
Image.fromarray(b).save(f'{C}/F-01_02_v1122.png')

# 3) +5 -> -8 on the red sticker; the '-' comes from the real '-5' sticker
a = rd('F-01_05'); m = ink_mask(a); b = erase(a, m, 9)
d = rd('F-01_03'); dm = ink_mask(d); dsp = [s for s in cols(dm) if s[1] - s[0] > 15]
mx0, mx1 = dsp[0]; ys, _ = np.where(dm[:, mx0:mx1]); my0, my1 = ys.min() - 3, ys.max() + 4
minus = (d[my0:my1, mx0:mx1].copy(), dm[my0:my1, mx0:mx1].copy())
ys, xs = np.where(m); bx0, bx1, by0, by1 = xs.min(), xs.max(), ys.min(), ys.max()
reg, mk = minus; mk = cv2.GaussianBlur(mk.astype(np.float32), (3, 3), 0)[..., None]
s = (bx1 - bx0) * .36 / reg.shape[1]; reg = cv2.resize(reg, None, fx=s, fy=s); mk = cv2.resize(mk, None, fx=s, fy=s)[..., None]
cy = (by0 + by1) // 2; py = cy - reg.shape[0] // 2; px = bx0
b[py:py + reg.shape[0], px:px + reg.shape[1], :3] = (b[py:py + reg.shape[0], px:px + reg.shape[1], :3] * (1 - mk) + reg[..., :3] * mk).astype(np.uint8)
b = hand_text(b, '8', (bx0 + int((bx1 - bx0) * .46), by0, bx1, by1), 260, sy=1.0, seed=5)
Image.fromarray(b).save(f'{C}/F-01_05_v1122.png')

# 4) scroll: drop '.PK' and swap the green PK box for a copy of the magenta UK box
a = np.array(Image.open(f'{C}/F-04_00.png').convert('RGB'))
S = a.shape[1] / 1500  # coords measured on the 1500-wide preview
r = lambda *v: [int(round(x * S)) for x in v]
pk_dot = r(1078, 912, 1240, 1102); pk_box = r(1230, 905, 1432, 1110); uk_box = r(1186, 1146, 1392, 1342)
mask = np.zeros(a.shape[:2], np.uint8)
for x0, y0, x1, y1 in (pk_dot, pk_box): mask[y0:y1, x0:x1] = 1
dark = (a.max(2) < 200) | (np.abs(a.astype(int) - a.mean(2, keepdims=True)).max(2) > 25)
bgr = cv2.inpaint(cv2.cvtColor(a, cv2.COLOR_RGB2BGR), (mask * 255).astype(np.uint8), 15, cv2.INPAINT_TELEA)
bgr = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB); pap = np.median(a[int(1105*S):int(1140*S), int(900*S):int(1100*S)].reshape(-1, 3), 0)
rng = np.random.default_rng(2); fill = (pap + rng.normal(0, 1.2, a.shape)).clip(0, 255).astype(np.uint8)
bgr = np.where(mask[..., None] > 0, fill, bgr); bgr = cv2.cvtColor(bgr, cv2.COLOR_RGB2BGR)
a2 = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
ux0, uy0, ux1, uy1 = uk_box; box = a2[uy0:uy1, ux0:ux1]; bm = (box.min(2) < 215).astype(np.float32)
bm = cv2.GaussianBlur(bm, (3, 3), 0)[..., None]
tx, ty = r(1100)[0], r(919)[0]
reg = a2[ty:ty + box.shape[0], tx:tx + box.shape[1]].astype(np.float32)
a2[ty:ty + box.shape[0], tx:tx + box.shape[1]] = (reg * (1 - bm) + box * bm).astype(np.uint8)
Image.fromarray(a2).save(f'{C}/F-04_00_v1122.png')
print('ok')
