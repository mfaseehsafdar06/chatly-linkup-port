// Shared LinkUp helpers (HF-19..26). Plain script; needs ../lib/kit.js (window.HF) and, for the globe, vendor/d3 + topojson.
// window.LU = { PEOPLE, PH, people photos, globe(), cursor svg, plane svg, sticker(), lerpKeys(), loadLand() }
(function () {
  const B = new URL('.', document.currentScript.src).href; // .../hf/_linkup/
  const CUT = new URL('../../assets/cut/', B).href;

  // ---- people (names swapped per ASSETS §1; Ying's surname is a placeholder until the user picks one) ----
  const YING = 'Ying Tan'; // PLACEHOLDER surname (reference used a real person's full name)
  // photos are PLACEHOLDERS (headshot pack not generated yet): reels/chatly-chatapps/mg/assets/av
  const PH = {
    duo: [B + 'img/m3-white-40s.jpg', B + 'img/f4-white-40s.jpg'],
    izy: B + 'img/f3-southasian-early30s.jpg',
    luke: B + 'img/m2-black-mid30s.jpg',
    ying: B + 'img/f2-eastasian-mid30s.jpg',
    fin: B + 'img/m1-latino-mid20s.jpg',
  };
  const PEOPLE = {
    ying: { name: YING, city: 'Singapore', lat: 1.35, lon: 103.82, c: 'g', off: 8, status: 'Working on the next banger' },
    fin: { name: 'Fin', city: 'Brisbane', lat: -27.47, lon: 153.03, c: 'y', off: 10, status: 'Being the next ice cream delivery man' },
    izy: { name: 'Izy', city: 'Edmonton', lat: 53.55, lon: -113.49, c: 'r', off: -6, status: 'Late for class in Uni' },
    leo: { name: 'Leo and Max', city: 'Zurich', lat: 47.37, lon: 8.54, c: 'r', off: 2, status: 'Frolicking in the Swiss Alps' },
    luke: { name: 'Luke', city: 'New York', lat: 40.71, lon: -74.0, c: 'y', off: -4, status: 'Couch surfing for the month' },
  };
  // local time string for a base Singapore time (h,m) -> person's time
  function timeFor(p, sgH, sgM) { let h = (sgH + (p.off - 8) + 48) % 24; const ap = h >= 12 ? 'PM' : 'AM'; let hh = h % 12; if (!hh) hh = 12; return `${hh}:${String(sgM).padStart(2, '0')} ${ap}`; }

  // ---- keyframe interpolation: keys [[t, v], ...] (v number or array) ----
  function lerpKeys(keys, t, ease) {
    if (t <= keys[0][0]) return keys[0][1];
    for (let i = 0; i < keys.length - 1; i++) {
      const [t0, a] = keys[i], [t1, b] = keys[i + 1];
      if (t <= t1) { let u = (t - t0) / (t1 - t0); if (ease) u = ease(u); return Array.isArray(a) ? a.map((x, k) => x + (b[k] - x) * u) : a + (b - a) * u; }
    }
    return keys[keys.length - 1][1];
  }
  const smooth = u => u * u * (3 - 2 * u);

  // ---- cursors (macOS look) ----
  const ARROW = `<svg width="34" height="48" viewBox="0 0 17 24"><path d="M1 1 L1 18.5 L5.2 14.6 L8 21.3 L10.9 20.1 L8.1 13.5 L13.8 13.5 Z" fill="#111" stroke="#fff" stroke-width="1.3" stroke-linejoin="round"/></svg>`;
  const HAND = `<svg width="40" height="46" viewBox="0 0 20 23" style="left:-12px;top:-2px"><path d="M7.2 1.2c.9 0 1.6.7 1.6 1.6v6.3l.4-.1V7.6c0-.9.7-1.5 1.5-1.5s1.5.6 1.5 1.5v1.5l.4-.1c0-.8.7-1.4 1.5-1.4s1.5.6 1.5 1.5v1.3l.3-.1c.1-.7.7-1.1 1.4-1.1.8 0 1.4.6 1.4 1.4v5.6c0 3.4-2.4 6-5.8 6h-1.6c-2 0-3.4-.8-4.6-2.4L2 13.8c-.5-.7-.3-1.6.4-2 .6-.4 1.4-.3 1.9.2l1.3 1.4V2.8c0-.9.7-1.6 1.6-1.6z" fill="#fff" stroke="#111" stroke-width="1.1" stroke-linejoin="round"/><path d="M8.8 9v4.6M11.7 9.2v4.4M14.6 10.2v3.6" stroke="#111" stroke-width=".9" stroke-linecap="round"/></svg>`;
  function cursorEl(parent) { const d = document.createElement('div'); d.className = 'lu-cursor'; parent.appendChild(d); let k = ''; return { el: d, set(x, y, kind = 'arrow', s = 1, show = true) { d.style.display = show ? '' : 'none'; d.style.left = x + 'px'; d.style.top = y + 'px'; d.style.transform = `scale(${s})`; if (k !== kind) { d.innerHTML = kind === 'hand' ? HAND : ARROW; k = kind; } } }; }

  // ---- cartoon plane (red + white, felt-tip look), nose pointing right ----
  const PLANE = `<svg viewBox="0 0 120 80" width="120" height="80"><g stroke="#2a1a1a" stroke-width="2.8" stroke-linejoin="round" stroke-linecap="round">
    <path d="M56 32 L36 4 Q44 1 50 5 L74 32 Z" fill="#D7263D"/>
    <path d="M58 50 L40 76 Q48 79 54 75 L78 50 Z" fill="#D7263D"/>
    <path d="M20 32 L8 12 Q14 9 19 13 L34 32 Z" fill="#D7263D"/>
    <path d="M8 41 C8 31 22 28 44 28 L90 28 C106 28 116 34 116 41 C116 48 106 54 90 54 L44 54 C22 54 8 51 8 41 Z" fill="#fff"/>
    <path d="M98 31 C106 32 112 36 113 40 L100 40 C97 37 96 34 98 31 Z" fill="#7FD1E8"/>
    <circle cx="84" cy="40" r="4.2" fill="#7FD1E8"/><circle cx="70" cy="40" r="4.2" fill="#7FD1E8"/><circle cx="56" cy="40" r="4.2" fill="#7FD1E8"/>
    <path d="M12 46 L104 48" stroke="#D7263D" stroke-width="3.2"/></g></svg>`;

  // ---- stickers: crayon cutouts sized by target box (fit inside, centred), popped with the HF kit ----
  const STK = { location: 'GPT-05_01.png', time: 'GPT-05_02.png', working: 'GPT-05_03.png', priorities: 'GPT-05_04.png' };
  // trims transparent padding at load so the box is the paper itself (the cutouts get regenerated with different padding)
  function sticker(parent, key, box, t0, seed, t1 = 1e9) {
    const im = new Image(); im.className = 'lu-stk'; im.style.display = 'none'; parent.appendChild(im);
    const [x0, y0, x1, y1] = box;
    const ready = (async () => {
      const src = new Image(); src.src = CUT + STK[key]; await src.decode();
      const c = document.createElement('canvas'); c.width = src.naturalWidth; c.height = src.naturalHeight; const g = c.getContext('2d'); g.drawImage(src, 0, 0);
      const d = g.getImageData(0, 0, c.width, c.height).data; let a = c.width, b = c.height, e = 0, f = 0;
      for (let y = 0; y < c.height; y++) for (let x = 0; x < c.width; x++) if (d[(y * c.width + x) * 4 + 3] > 40) { if (x < a) a = x; if (x > e) e = x; if (y < b) b = y; if (y > f) f = y; }
      const o = document.createElement('canvas'); o.width = e - a + 1; o.height = f - b + 1; o.getContext('2d').drawImage(c, -a, -b);
      im.src = o.toDataURL(); await im.decode();
    })();
    return {
      ready,
      set(t) {
        const m = HF.motion.pop(t, t0, seed); if (!m || t >= t1 - 1e-6) { im.style.display = 'none'; return; }
        const bw = x1 - x0, bh = y1 - y0, ar = im.naturalWidth / im.naturalHeight; let w = bw, h = bw / ar; if (h > bh * 1.6) { h = bh * 1.6; w = h * ar; } // width-fit (new art is less elongated than the ref)
        const j = HF.jitter(t, seed, 0.8, 0.25);
        im.style.display = ''; im.style.width = w + 'px'; im.style.height = h + 'px';
        im.style.left = (x0 + (bw - w) / 2) + 'px'; im.style.top = (y0 + (bh - h) / 2) + 'px';
        im.style.transform = `translate(${j.dx}px,${j.dy}px) rotate(${(m.rot * 0.15 + j.rot)}rad) scale(${m.scale})`;
      },
    };
  }

  // ---- globe (d3 orthographic on canvas) ----
  let LAND = null;
  async function loadLand(res = '50m') { // needs <script src="../_linkup/vendor/land-50m.js">
    if (LAND) return LAND; const topo = window['LAND_TOPO_' + res]; LAND = topojson.feature(topo, topo.objects.land); return LAND; }
  // draw globe; returns projector p(lon,lat) -> {x,y,vis(cos c)}
  function drawGlobe(g, { cx, cy, r, lon0, lat0, ocean = '#5FA7B5', land = '#8FE3A7', dots = true, rim = '#7B7FA6' }) {
    const proj = d3.geoOrthographic().translate([cx, cy]).scale(r).rotate([-lon0, -lat0]).clipAngle(90).precision(0.3);
    const path = d3.geoPath(proj, g);
    g.save();
    g.beginPath(); g.arc(cx, cy, r, 0, Math.PI * 2); g.closePath();
    const og = g.createRadialGradient(cx - r * .25, cy - r * .3, r * .1, cx, cy, r * 1.02);
    og.addColorStop(0, '#78BCC6'); og.addColorStop(.65, ocean); og.addColorStop(1, '#4A8D9F'); g.fillStyle = og; g.fill();
    g.clip();
    if (dots) { // fine halftone dot grid on the ocean
      g.fillStyle = 'rgba(255,255,255,.10)'; const s = Math.max(3, r / 90);
      for (let y = cy - r; y < cy + r; y += s) for (let x = cx - r + ((Math.round((y - cy) / s) & 1) ? s / 2 : 0); x < cx + r; x += s) g.fillRect(x, y, s * .38, s * .38);
    }
    g.beginPath(); path(LAND); const lg = g.createRadialGradient(cx - r * .3, cy - r * .35, r * .1, cx, cy, r);
    lg.addColorStop(0, '#A6EEB8'); lg.addColorStop(.7, land); lg.addColorStop(1, '#6CC98E'); g.fillStyle = lg; g.fill();
    // limb shading
    const sh = g.createRadialGradient(cx, cy, r * .55, cx, cy, r); sh.addColorStop(0, 'rgba(20,40,60,0)'); sh.addColorStop(1, 'rgba(20,40,70,.14)');
    g.fillStyle = sh; g.fillRect(cx - r, cy - r, 2 * r, 2 * r);
    g.restore();
    g.beginPath(); g.arc(cx, cy, r, 0, Math.PI * 2); g.lineWidth = Math.max(1.5, r / 220); g.strokeStyle = rim; g.stroke();
    const rad = Math.PI / 180, sφ0 = Math.sin(lat0 * rad), cφ0 = Math.cos(lat0 * rad);
    return (lon, lat) => {
      const φ = lat * rad, Δ = (lon - lon0) * rad;
      const vis = sφ0 * Math.sin(φ) + cφ0 * Math.cos(φ) * Math.cos(Δ);
      const x = Math.cos(φ) * Math.sin(Δ), y = cφ0 * Math.sin(φ) - sφ0 * Math.cos(φ) * Math.cos(Δ);
      return { x: cx + r * x, y: cy - r * y, vis };
    };
  }

  window.LU = { B, CUT, YING, PH, PEOPLE, timeFor, lerpKeys, smooth, ARROW, HAND, cursorEl, PLANE, sticker, loadLand, drawGlobe };
})();
