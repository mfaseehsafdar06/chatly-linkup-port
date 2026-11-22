// Paper/props helpers for HF-05/06/09/12/13/24/27 (on top of ../lib/kit.js). window.X
// Every cutout is alpha-trimmed on load and drawn into a TARGET BOX in output pixels (never native size),
// so the gpt-image cutouts can be swapped without touching layouts.
(function () {
  const W = 1440, H = 1080;
  function trim(img) {
    const c = document.createElement('canvas'); c.width = img.width; c.height = img.height; const g = c.getContext('2d'); g.drawImage(img, 0, 0);
    const d = g.getImageData(0, 0, c.width, c.height).data; let x0 = c.width, y0 = c.height, x1 = 0, y1 = 0;
    for (let y = 0; y < c.height; y += 2) for (let x = 0; x < c.width; x += 2) if (d[(y * c.width + x) * 4 + 3] > 128) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
    if (x1 <= x0) return c; const o = document.createElement('canvas'); o.width = x1 - x0 + 2; o.height = y1 - y0 + 2; const og = o.getContext('2d'); og.drawImage(c, -x0, -y0);
    const id = og.getImageData(0, 0, o.width, o.height), q = id.data; for (let i = 3; i < q.length; i += 4) q[i] = Math.max(0, Math.min(255, (q[i] - 100) * 2.4)); og.putImageData(id, 0, 0); return o;
  }
  async function load(map) { const o = {}; await Promise.all(Object.entries(map).map(async ([k, v]) => { const im = await HF.loadImg(v); o[k] = v.includes('/cut/') ? trim(im) : im; })); return o; }
  const box = (x0, y0, x1, y1) => ({ cx: (x0 + x1) / 2, cy: (y0 + y1) / 2, w: x1 - x0, h: y1 - y0 });
  // draw img stretched into w x h centred at cx,cy, rotated rot (deg). h omitted -> keep aspect.
  function draw(g, img, o) {
    const w = o.w, h = o.h || o.w * img.height / img.width; g.save(); g.globalAlpha = o.alpha ?? 1; if (o.blend) g.globalCompositeOperation = o.blend;
    g.translate(o.cx, o.cy); g.rotate((o.rot || 0) * Math.PI / 180); if (o.scale) g.scale(o.scale, o.scale); if (o.flipX) g.scale(-1, 1);
    if (o.shadow !== false && !o.blend) { const s = o.shadow || {}; g.shadowColor = `rgba(20,20,10,${s.op ?? .16})`; g.shadowBlur = s.blur ?? 5; g.shadowOffsetX = s.dx ?? 1; g.shadowOffsetY = s.dy ?? 3; }
    if (o.clipFrac != null) { g.beginPath(); g.rect(-w / 2 - 4, -h / 2 - 4, w * o.clipFrac + 4, h + 8); g.clip(); }
    if (o.filter) g.filter = o.filter;
    if (o.inset) { const [l, t, r, b] = o.inset; g.drawImage(img, img.width * l, img.height * t, img.width * (1 - l - r), img.height * (1 - t - b), -w / 2, -h / 2, w, h); } else g.drawImage(img, -w / 2, -h / 2, w, h); g.restore();
  }
  // motion blur: average n renders of fn(ctx, dx, dy) along vec [vx,vy] (pixels, full streak length)
  let L1, L2;
  function mblur(g, vec, n, fn) {
    if (!vec || Math.hypot(vec[0], vec[1]) < 1.5) { fn(g, 0, 0); return; }
    if (!L1) { L1 = document.createElement('canvas'); L1.width = W; L1.height = H; L2 = document.createElement('canvas'); L2.width = W; L2.height = H; }
    const a = L1.getContext('2d'), b = L2.getContext('2d'); a.setTransform(1, 0, 0, 1, 0, 0); a.clearRect(0, 0, W, H);
    for (let i = 0; i < n; i++) { const u = n > 1 ? i / (n - 1) - .5 : 0; b.setTransform(1, 0, 0, 1, 0, 0); b.clearRect(0, 0, W, H); fn(b, vec[0] * u, vec[1] * u);
      a.globalCompositeOperation = 'lighter'; a.globalAlpha = 1 / n; a.drawImage(L2, 0, 0); }
    a.globalCompositeOperation = 'source-over'; a.globalAlpha = 1; g.drawImage(L1, 0, 0);
  }
  // white scanned paper with sparse grey specks (stable), faint fibres
  function scanPaper(g, seed = 11, base = [251, 251, 249], specks = 70) {
    g.fillStyle = `rgb(${base})`; g.fillRect(0, 0, W, H); const R = HF.rng(seed);
    for (let i = 0; i < 1400; i++) { g.fillStyle = `rgba(90,90,80,${R() * .03})`; g.fillRect(R() * W, R() * H, 1 + R() * 4, 1); }
    for (let i = 0; i < specks; i++) { const x = R() * W, y = R() * H, r = .7 + R() * 1.6; g.fillStyle = `rgba(40,40,40,${.35 + R() * .5})`; g.beginPath(); g.ellipse(x, y, r, r * (.6 + R() * .8), R() * 3, 0, 7); g.fill(); }
    for (let i = 0; i < 6; i++) { const x = R() * W, y = R() * H; g.strokeStyle = `rgba(60,60,60,${.25 + R() * .3})`; g.lineWidth = 1; g.beginPath(); g.moveTo(x, y); g.lineTo(x + (R() - .5) * 4, y + 4 + R() * 8); g.stroke(); }
  }
  const lerp = (a, b, t) => a + (b - a) * t, cl = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
  // keyframe track: [[frame, value(s)], ...] -> linear interp at frame f
  function track(keys, f) { if (f <= keys[0][0]) return keys[0][1]; for (let i = 1; i < keys.length; i++) if (f <= keys[i][0]) { const [fa, va] = keys[i - 1], [fb, vb] = keys[i]; const u = (f - fa) / (fb - fa); return Array.isArray(va) ? va.map((v, j) => lerp(v, vb[j], u)) : lerp(va, vb, u); } return keys[keys.length - 1][1]; }
  window.X = { W, H, trim, load, box, draw, mblur, scanPaper, lerp, cl, track };
})();
