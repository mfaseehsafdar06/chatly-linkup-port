// HF shared kit (HF-03 sticker motion + HF-04 line-boil crayon strokes). Canvas 2D, 1440x1080, 24 fps.
// Load with <script src="../lib/kit.js"></script>; everything hangs off window.HF.
(function () {
  const FPS = 24, W = 1440, H = 1080;
  const rng = s => () => { s |= 0; s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
  const lerp = (a, b, t) => a + (b - a) * t;
  const easeOut = t => 1 - Math.pow(1 - t, 3);
  const frame = t => Math.floor(t * FPS + 1e-6);
  const on2s = t => Math.floor(frame(t) / 2);                       // stop-motion step index (12 fps)
  const hash = (...n) => { let h = 2166136261; for (const x of n) { h ^= Math.floor(x * 1000) | 0; h = Math.imul(h, 16777619); } return h >>> 0; };

  const loadImg = src => new Promise((res, rej) => { const i = new Image(); i.onload = () => res(i); i.onerror = () => rej(new Error('img ' + src)); i.src = src; });
  async function loadAll(map) { const o = {}; await Promise.all(Object.entries(map).map(async ([k, v]) => { o[k] = await loadImg(v); })); return o; }

  // stop-motion jitter: +-px and +-deg, new value every 2 frames
  function jitter(t, seed, px = 1.5, deg = 0.5) { const R = rng(hash(seed, on2s(t))); return { dx: (R() - .5) * 2 * px, dy: (R() - .5) * 2 * px, rot: (R() - .5) * 2 * deg * Math.PI / 180 }; }

  // Draw an image (sticker) centred at (x,y) with width w, rotation rot (rad), alpha, optional paper shadow.
  function drawSticker(g, img, x, y, w, { rot = 0, alpha = 1, scale = 1, shadow = true, blur = 0, flipY = false } = {}) {
    const h = w * img.height / img.width; g.save(); g.globalAlpha = alpha; g.translate(x, y); g.rotate(rot); g.scale(scale, flipY ? -scale : scale);
    if (shadow) { g.shadowColor = 'rgba(0,0,0,.25)'; g.shadowOffsetY = 2; g.shadowBlur = 3; }
    if (blur) g.filter = `blur(${blur}px)`;
    g.drawImage(img, -w / 2, -h / 2, w, h); g.restore();
  }

  // Motion envelopes. Each returns transform params for time t given appear time t0 (seconds).
  const motion = {
    // pop: 1-frame appear, scale 1.06 -> 1.0 over 2 frames, fixed +-2deg rotation per seed
    pop(t, t0, seed = 1) { if (t < t0 - 1e-6) return null; const f = (t - t0) * FPS; const R = rng(hash(seed)); return { scale: f < 1 ? 1.06 : f < 2 ? 1.03 : 1, rot: (R() - .5) * 4 * Math.PI / 180, dx: 0, dy: 0, blur: 0 }; },
    // slide-in from an edge over `frames` frames with blur, 2-frame overshoot. dir = [dx,dy] unit of entry direction (from where it comes)
    slide(t, t0, dir = [1, 0], dist = 900, frames = 4, seed = 1) {
      if (t < t0 - 1e-6) return null; const f = (t - t0) * FPS; const R = rng(hash(seed)); const rot = (R() - .5) * 4 * Math.PI / 180;
      let u; if (f < frames) u = easeOut(f / frames) * 1.04; else if (f < frames + 2) u = lerp(1.04, 1, (f - frames) / 2); else u = 1;
      const off = (1 - u) * dist; return { scale: 1, rot, dx: dir[0] * off, dy: dir[1] * off, blur: f < frames ? 6 * (1 - f / frames) : 0 };
    },
    // wipe progress 0..1 over dur seconds (left->right mask); use with clipRect
    wipe(t, t0, dur = 0.25) { return clamp((t - t0) / dur); },
  };
  function drawMoved(g, img, x, y, w, m, extra = {}) { if (!m) return; drawSticker(g, img, x + m.dx, y + m.dy, w, { ...extra, rot: (extra.rot || 0) + m.rot, scale: m.scale, blur: m.blur }); }

  // slap: hand image enters (2 blur frames), presses 2-3 frames, exits (2 blur frames). Returns {x,y,blur,scale,show}
  // from: [x,y] offscreen start; at: [x,y] press point (hand anchor, i.e. where the palm centre lands)
  function slap(t, t0, from, at, to = from) {
    const f = (t - t0) * FPS; if (f < -2 || f > 7) return { show: false };
    if (f < 0) { const u = (f + 2) / 2; return { show: true, x: lerp(from[0], at[0], u), y: lerp(from[1], at[1], u), blur: 10, scale: 1 }; }
    if (f < 3) return { show: true, x: at[0], y: at[1], blur: 0, scale: .98 };
    const u = clamp((f - 3) / 2); return { show: u < 1, x: lerp(at[0], to[0], u), y: lerp(at[1], to[1], u), blur: 10, scale: 1 };
  }

  // ---------- HF-04 line-boil crayon strokes ----------
  // A crayon stroke along a polyline: many thin jittered passes + grain gaps. Redraws every 2 frames (pass t so it boils).
  function crayonPath(g, pts, { color = '#E4338A', width = 10, t = 0, seed = 1, boil = true, passes = 5, alpha = .9 } = {}) {
    const R = rng(hash(seed, boil ? on2s(t) : 0)); g.save(); g.lineCap = 'round'; g.lineJoin = 'round'; g.strokeStyle = color;
    for (let p = 0; p < passes; p++) {
      g.globalAlpha = alpha * (.35 + R() * .45); g.lineWidth = width * (.35 + R() * .5); const o = (R() - .5) * width * .6;
      g.beginPath(); pts.forEach((q, i) => { const jx = (R() - .5) * width * .35 + o, jy = (R() - .5) * width * .35 + o; i ? g.lineTo(q[0] + jx, q[1] + jy) : g.moveTo(q[0] + jx, q[1] + jy); }); g.stroke();
    }
    // grain: punch tiny gaps
    g.globalCompositeOperation = 'destination-out'; g.globalAlpha = .5;
    for (let i = 0; i < pts.length * 3; i++) { const q = pts[(R() * pts.length) | 0]; g.fillRect(q[0] + (R() - .5) * width, q[1] + (R() - .5) * width, 1 + R() * 2, 1 + R() * 2); }
    g.restore();
  }
  const densify = (pts, step = 12) => { const o = []; for (let i = 0; i < pts.length - 1; i++) { const a = pts[i], b = pts[i + 1], n = Math.max(1, Math.ceil(Math.hypot(b[0] - a[0], b[1] - a[1]) / step)); for (let s = 0; s < n; s++) o.push([lerp(a[0], b[0], s / n), lerp(a[1], b[1], s / n)]); } o.push(pts[pts.length - 1]); return o; };
  const wobble = (pts, amp, seed) => { const R = rng(seed); return pts.map(p => [p[0] + (R() - .5) * amp, p[1] + (R() - .5) * amp]); };
  const prims = {
    box(g, x, y, w, h, o = {}) { const R = rng(hash(o.seed || 1, on2s(o.t || 0))); const j = () => (R() - .5) * 10; const pts = [[x + j(), y + j()], [x + w + j(), y + j()], [x + w + j(), y + h + j()], [x + j(), y + h + j()], [x + j() + 8, y + j() - 4]]; crayonPath(g, densify(pts), o); },
    ring(g, cx, cy, rx, ry, o = {}) { const R = rng(hash(o.seed || 1, on2s(o.t || 0))); const pts = []; const a0 = R() * 6; for (let i = 0; i <= 64; i++) { const a = a0 + i / 60 * Math.PI * 2, k = 1 + (R() - .5) * .05; pts.push([cx + Math.cos(a) * rx * k, cy + Math.sin(a) * ry * k]); } crayonPath(g, pts, o); },
    burst(g, cx, cy, r0, r1, n = 8, o = {}) { const R = rng(hash(o.seed || 1, on2s(o.t || 0))); for (let i = 0; i < n; i++) { const a = i / n * Math.PI * 2 + (R() - .5) * .25; const a1 = r0 * (1 + (R() - .5) * .15), b1 = r1 * (1 + (R() - .5) * .15); crayonPath(g, [[cx + Math.cos(a) * a1, cy + Math.sin(a) * a1], [cx + Math.cos(a) * b1, cy + Math.sin(a) * b1]], { ...o, seed: (o.seed || 1) + i * 7 }); } },
    star(g, cx, cy, r, o = {}) { prims.burst(g, cx, cy, r * .2, r, 6, o); },
    coil(g, x0, y0, x1, y1, loops = 5, r = 30, o = {}) { const R = rng(hash(o.seed || 1, on2s(o.t || 0))); const pts = []; const n = loops * 24; for (let i = 0; i <= n; i++) { const u = i / n, a = u * loops * Math.PI * 2; pts.push([lerp(x0, x1, u) + Math.cos(a) * r * (1 + (R() - .5) * .1), lerp(y0, y1, u) + Math.sin(a) * r * .8]); } crayonPath(g, pts, o); },
  };
  const PAL = { pink: '#E4338A', green: '#22D07A', cyan: '#34B8E8', orange: '#F2A23A', blue: '#5468E8', red: '#E0263F' };

  // Paper background with faint fibres (stable per seed)
  function paper(g, color = 'rgb(246,246,243)', seed = 3) { g.fillStyle = color; g.fillRect(0, 0, W, H); const R = rng(seed); for (let i = 0; i < 900; i++) { g.fillStyle = `rgba(0,0,0,${R() * .035})`; g.fillRect(R() * W, R() * H, 1 + R() * 3, 1); } }

  window.HF = { FPS, W, H, rng, clamp, lerp, easeOut, frame, on2s, hash, loadImg, loadAll, jitter, drawSticker, motion, drawMoved, slap, crayonPath, densify, wobble, prims, PAL, paper };
})();
