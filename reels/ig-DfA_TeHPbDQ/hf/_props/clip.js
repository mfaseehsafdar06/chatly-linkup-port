// Sticker clip engine for the "This is Faseeh" overlays (P-21/24/27/30). window.CLIP(cfg) sets window.ready / window.render.
// cfg = { items:[ITEM...] }  (frames are clip frames at 24 fps, positions in output px 1440x1080)
// ITEM = { src, cx, cy, w, h?, rot(deg), on(frame), anim:'pop'|'slap'|'slide', boil(true), off(frame, optional),
//          slide:{from:[dx,dy], frames:4}, slap:{from:[dx,dy], hand:{w, rot, at:[dx,dy]}}, buzz:{on, frames, amp}, inset:[l,t,r,b], filter }
// Look follows the reference stickers: hard 1-frame appear (scale 1.06 -> 1.025 -> 1), then a stop-motion hold that boils
// between 3 nearby poses every 4 frames (like the LEO chip in ref shot 4).
(function () {
  window.CLIP = function (cfg) {
    const g = document.getElementById('c').getContext('2d'); let IM;
    const srcs = { H0: '../_props/hands/H0L.png' }; cfg.items.forEach((it, i) => srcs['i' + i] = it.src);
    window.ready = (async () => { IM = await X.load(srcs); cfg.items.forEach((it, i) => { if (it.curl) IM['i' + i] = curl(IM['i' + i], it.curl); }); })();
    // bake a paper curl into a sticky note: bottom edge lifts (darker band + light rim), slight top-corner highlight
    function curl(img, k) { const c = document.createElement('canvas'); c.width = img.width; c.height = img.height; const q = c.getContext('2d'); q.drawImage(img, 0, 0);
      q.globalCompositeOperation = 'source-atop'; const h = img.height;
      let gr = q.createLinearGradient(0, h * .62, 0, h); gr.addColorStop(0, 'rgba(0,0,0,0)'); gr.addColorStop(.75, `rgba(60,40,0,${.16 * k})`); gr.addColorStop(.93, `rgba(255,255,230,${.22 * k})`); gr.addColorStop(1, `rgba(40,30,0,${.25 * k})`);
      q.fillStyle = gr; q.fillRect(0, 0, img.width, h);
      gr = q.createLinearGradient(0, 0, img.width * .5, h * .4); gr.addColorStop(0, `rgba(255,255,255,${.12 * k})`); gr.addColorStop(1, 'rgba(255,255,255,0)'); q.fillStyle = gr; q.fillRect(0, 0, img.width, h); return c; }
    const HANCH = [738, 521], HW0 = 757; // knuckle anchor in H0L px (H0 padded 250 px each side); HW0 = palm image width before padding
    function pose(it, i, f) { if (it.boil === false) return [0, 0, 0, 1]; const k = Math.floor(Math.max(0, f - it.on) / 4) % 3; const R = HF.rng(HF.hash(i * 17 + 3, k));
      const a = it.boilAmp ?? 1; return [(R() - .5) * 9 * a, (R() - .5) * 6 * a, (R() - .5) * .5 * a, 1 + (R() - .5) * .03 * a]; }
    function sticker(G, it, i, f, ox, oy, orot, osc) { const img = IM['i' + i]; const p = pose(it, i, f);
      X.draw(G, img, { cx: it.cx + p[0] + ox, cy: it.cy + p[1] + oy, w: it.w, h: it.h, rot: (it.rot || 0) + p[2] + orot, scale: p[3] * osc, inset: it.inset, filter: it.filter, shadow: it.curl ? { op: .34, blur: 12, dx: 2, dy: 8 } : { op: .22, blur: 7, dy: 3 } }); }
    function hand(G, it, f, ox, oy) { const h = it.slap.hand; const s = h.w / HW0; G.save(); G.translate(it.cx + h.at[0] + ox, it.cy + h.at[1] + oy); G.rotate(h.rot * Math.PI / 180);
      G.shadowColor = 'rgba(0,0,0,.35)'; G.shadowBlur = 14; G.shadowOffsetY = 8; G.drawImage(IM.H0, -HANCH[0] * s, -HANCH[1] * s, IM.H0.width * s, IM.H0.height * s); G.restore(); }
    window.render = t => { const f = Math.round(t * 24); g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, 1440, 1080);
      cfg.items.forEach((it, i) => { if (f < it.on - (it.anim === 'slap' ? 2 : 0) || (it.off != null && f >= it.off)) return; const d = f - it.on;
        let ox = 0, oy = 0, orot = 0, osc = 1, blur = null;
        if (it.anim === 'pop') osc = d < 1 ? 1.06 : d < 2 ? 1.025 : 1;
        if (it.anim === 'slide') { const n = it.slide.frames || 4, fr = it.slide.from; let u; if (d < n) u = HF.easeOut((d + 1) / (n + 1)) * 1.04; else if (d < n + 2) u = 1.04 - .04 * (d - n + 1) / 2; else u = 1;
          ox = fr[0] * (1 - u); oy = fr[1] * (1 - u); if (d < n) blur = [fr[0] * .22 * (1 - d / n), fr[1] * .22 * (1 - d / n)]; }
        if (it.anim === 'slap') { const fr = it.slap.from; if (d === -2) { ox = fr[0]; oy = fr[1]; orot = 8; osc = 1.12; blur = [-fr[0] * .5, -fr[1] * .5]; }
          else if (d === -1) { ox = fr[0] * .3; oy = fr[1] * .3; orot = 3; osc = 1.05; blur = [-fr[0] * .35, -fr[1] * .35]; } }
        if (it.buzz && f >= it.buzz.on && f < it.buzz.on + it.buzz.frames) { const k = f - it.buzz.on; const a = it.buzz.amp * (1 - k / it.buzz.frames * .5); ox += (k % 2 ? -a : a); orot += (k % 2 ? -1 : 1) * .9; }
        const draw = (G, dx, dy) => sticker(G, it, i, f, ox + dx, oy + dy, orot, osc);
        if (blur) X.mblur(g, blur, 12, draw); else draw(g, 0, 0);
        if (it.anim === 'slap') { const fr = it.slap.from; let hx = null, hb = null;
          if (d === -2) { hx = [fr[0], fr[1]]; hb = [-fr[0] * .5, -fr[1] * .5]; } else if (d === -1) { hx = [fr[0] * .3, fr[1] * .3]; hb = [-fr[0] * .35, -fr[1] * .35]; }
          else if (d >= 0 && d <= 2) hx = [0, 0]; else if (d === 3) { hx = [fr[0] * .45, fr[1] * .45]; hb = [fr[0] * .4, fr[1] * .4]; } else if (d === 4) { hx = [fr[0] * 1.1, fr[1] * 1.1]; hb = [fr[0] * .5, fr[1] * .5]; }
          if (hx) { const dh = (G, dx, dy) => hand(G, it, f, hx[0] + dx, hx[1] + dy); if (hb) X.mblur(g, hb, 12, dh); else dh(g, 0, 0); } }
      }); };
  };
})();
