// HF-07 · Google Meet chrome component (shared by HF-08, HF-10, HF-11, HF-28, HF-29, HF-30).
// Classic script -> window.MEET. Also usable as a module side-effect import.
// Everything is laid out in "Meet CSS px" (measured from the reference: button pitch 48, reaction pitch 28.3)
// inside a page box of size W x H; the asset scales/positions the page with a CSS transform.
// The video tile is a TRANSPARENT HOLE (the page background is drawn as the tile's box-shadow), so the live-action
// plate goes underneath. The PIP interior is transparent too; its border/label are drawn.
// Brand swaps: no "Ask Gemini" cluster (left of toolbar is blank), meeting title is neutral.
(function () {
  const ICON = {
    more_horiz: 'M6 10c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm12 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm-6 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z',
    mic: 'M12 14c1.66 0 2.99-1.34 2.99-3L15 5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.3-3c0 3-2.54 5.1-5.3 5.1S6.7 14 6.7 11H5c0 3.41 2.72 6.23 6 6.72V21h2v-3.28c3.28-.48 6-3.3 6-6.72h-1.7z',
    expand_less: 'M12 8l-6 6 1.41 1.41L12 10.83l4.59 4.58L18 14z',
    videocam: 'M15 8v8H5V8h10m1-2H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4V7c0-.55-.45-1-1-1z',
    present: 'M21 3H3c-1.11 0-2 .89-2 2v12c0 1.1.89 2 2 2h5v2h8v-2h5c1.1 0 1.99-.9 1.99-2L23 5c0-1.11-.9-2-2-2zm0 14H3V5h18v12zM12 6.5l-4 4h3V15h2v-4.5h3z',
    mood: 'M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z',
    cc: 'M19 4H5c-1.11 0-2 .9-2 2v12c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 14H5V6h14v12zM7 15h3c.55 0 1-.45 1-1v-1H9.5v.5h-2v-3h2v.5H11v-1c0-.55-.45-1-1-1H7c-.55 0-1 .45-1 1v4c0 .55.45 1 1 1zm7 0h3c.55 0 1-.45 1-1v-1h-1.5v.5h-2v-3h2v.5H18v-1c0-.55-.45-1-1-1h-3c-.55 0-1 .45-1 1v4c0 .55.45 1 1 1z',
    hand: 'M13 24c-3.26 0-6.19-1.99-7.4-5.02l-3.03-7.61C2.26 10.58 3 9.79 3.81 10.05l.79.26c.56.18 1.02.61 1.24 1.16L7.25 15H8V3.25C8 2.56 8.56 2 9.25 2s1.25.56 1.25 1.25V12h1V1.25c0-.69.56-1.25 1.25-1.25S14 .56 14 1.25V12h1V2.75c0-.69.56-1.25 1.25-1.25s1.25.56 1.25 1.25V12h1V5.75c0-.69.56-1.25 1.25-1.25S21 5.06 21 5.75V16c0 4.42-3.58 8-8 8zm0-2c3.31 0 6-2.69 6-6V7h-.5v6h-4.5V3h-.5v9H9V5h-.5v12.5H5.86l-.84-2.13-.67-1.71 3.11 7.83C8.23 20.5 10.5 22 13 22z',
    more_vert: 'M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z',
    call_end: 'M12 9c-1.6 0-3.15.25-4.6.72v3.1c0 .39-.23.74-.56.9-.98.49-1.87 1.12-2.66 1.85-.18.18-.43.28-.7.28-.28 0-.53-.11-.71-.29L.29 13.08c-.18-.17-.29-.42-.29-.7 0-.28.11-.53.29-.71C3.34 8.78 7.46 7 12 7s8.66 1.78 11.71 4.67c.18.18.29.43.29.71 0 .28-.11.53-.29.71l-2.48 2.48c-.18.18-.43.29-.71.29-.27 0-.52-.11-.7-.28-.79-.74-1.69-1.36-2.67-1.85-.33-.16-.56-.5-.56-.9v-3.1C15.15 9.25 13.6 9 12 9z',
    chat: 'M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H5.17L4 17.17V4h16v12zM6 12h8v2H6zm0-3h12v2H6zm0-3h12v2H6z',
    apps: 'M4 8h4V4H4v4zm6 12h4v-4h-4v4zm-6 0h4v-4H4v4zm0-6h4v-4H4v4zm6 0h4v-4h-4v4zm6-10v4h4V4h-4zm-6 4h4V4h-4v4zm6 6h4v-4h-4v4zm0 6h4v-4h-4v4z',
    info: 'M11 7h2v2h-2zm0 4h2v6h-2zm1-9C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z',
    add_reaction: 'M18 9V7h-2V2.84C14.77 2.3 13.42 2 11.99 2 6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12c0-1.05-.17-2.05-.47-3H18zm-2.5-1c.83 0 1.5.67 1.5 1.5s-.67 1.5-1.5 1.5-1.5-.67-1.5-1.5.67-1.5 1.5-1.5zm-7 0c.83 0 1.5.67 1.5 1.5S9.33 11 8.5 11 7 10.33 7 9.5 7.67 8 8.5 8zm3.5 9.5c-2.33 0-4.32-1.45-5.12-3.5h1.67c.7 1.19 1.97 2 3.45 2s2.76-.81 3.45-2h1.67c-.8 2.05-2.79 3.5-5.12 3.5zM22 3h2v2h-2v2h-2V5h-2V3h2V1h2v2z',
    keep: 'M16 9V4h1c.55 0 1-.45 1-1s-.45-1-1-1H7c-.55 0-1 .45-1 1s.45 1 1 1h1v5c0 1.66-1.34 3-3 3v2h5.97v7l1 1 1-1v-7H19v-2c-1.66 0-3-1.34-3-3z',
  };
  const svg = (name, size, color, extra = '') => `<svg width="${size}" height="${size}" viewBox="0 0 24 24" style="display:block;${extra}"><path fill="${color}" d="${ICON[name]}"/></svg>`;

  // Reaction row emoji (Meet order). Last one is the red "+" tile.
  const REACT = ['💖', '👍', '🎉', '👏', '😂', '😮', '😥', '🤔', '👎', '+'];
  // control offsets from the toolbar centre (Meet CSS px), averaged over shots 8 / 51 / 54
  const CTRL = [
    ['more_horiz', -194, 'plain'], ['mic', -165, 'circ'], ['expand_less', -123, 'plain'], ['videocam', -94, 'circ'],
    ['present', -48, 'circ'], ['mood', 0, 'active'], ['cc', 49, 'circ'], ['hand', 97, 'circ'], ['more_vert', 139, 'plain'], ['call_end', 186, 'hang'],
  ];
  const C = { bg: '#131314', btn: '#2e2f33', pill: '#1e1f22', icon: '#e3e3e3', active: '#c6d3ec', activeIcon: '#0e2350', hang: '#dc362e', label: '#ffffff' };

  const css = `
  .mt-page{position:absolute;left:0;top:0;overflow:hidden;transform-origin:0 0;font-family:GS,'Google Sans',Roboto,Arial,sans-serif;color:#e3e3e3}
  .mt-hole{position:absolute;box-sizing:border-box}
  .mt-c{position:absolute;display:flex;align-items:center;justify-content:center;transform:translate(-50%,-50%)}
  .mt-lbl{position:absolute;white-space:nowrap;font-family:GS,'Google Sans',Roboto,Arial,sans-serif;color:#f1f1f1;font-weight:450;text-shadow:0 1px 2px rgba(0,0,0,.55),0 0 1px rgba(0,0,0,.4);letter-spacing:.1px}
  .mt-emo{position:absolute;transform:translate(-50%,-50%);font-family:'Apple Color Emoji';line-height:1}
  .mt-plus{position:absolute;transform:translate(-50%,-50%);border-radius:3px;background:#e2231a;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900}
  .mt-pipring{position:absolute;box-sizing:border-box;border:2px solid rgba(190,206,242,.92)}
  `;
  function injectCSS() { if (document.getElementById('mt-css')) return; const s = document.createElement('style'); s.id = 'mt-css'; s.textContent = css; document.head.appendChild(s); }

  // toolbar: cx,cy = centre of the emoji (active) button. opts.right = [{icon,x}] absolute x (page px)
  function toolbar({ cx, cy, emojiActive = true, iconSize = 20, hover = null } = {}) {
    let h = '';
    // grouped pills behind [... mic] and [^ cam]
    h += `<div class="mt-c" style="left:${cx - 178}px;top:${cy}px;width:66px;height:36px;border-radius:18px;background:${C.pill}"></div>`;
    h += `<div class="mt-c" style="left:${cx - 107}px;top:${cy}px;width:62px;height:36px;border-radius:18px;background:${C.pill}"></div>`;
    for (const [name, dx, kind] of CTRL) {
      const x = cx + dx; let bg = '', w = 36, hh = 36, r = 18, col = C.icon;
      if (kind === 'circ') bg = C.btn;
      if (kind === 'plain') { w = 28; hh = 36; }
      if (kind === 'active') { if (emojiActive) { bg = C.active; w = 40; hh = 34; r = 10; col = C.activeIcon; } else bg = C.btn; }
      if (kind === 'hang') { bg = C.hang; w = 50; hh = 34; r = 17; col = '#fff'; }
      const sz = name === 'more_horiz' || name === 'expand_less' ? iconSize * .8 : name === 'call_end' ? iconSize * 1.05 : iconSize;
      const op = name === 'expand_less' ? .75 : 1;
      h += `<div class="mt-c" style="left:${x}px;top:${cy}px;width:${w}px;height:${hh}px;border-radius:${r}px;background:${bg || 'transparent'};opacity:${op}">${svg(name, sz, col)}</div>`;
    }
    return h;
  }
  // reaction row: centre of the toolbar's emoji button = cx; row y = cy. hide = index set to hide; scale per emoji
  function reactions({ cx, cy, size = 16, pitch = 28.3, start = -194, addX = 190, hoverIdx = -1 } = {}) {
    let h = '';
    REACT.forEach((e, i) => {
      const x = cx + start + i * pitch;
      if (i === hoverIdx) h += `<div class="mt-c" style="left:${x}px;top:${cy}px;width:${size * 1.65}px;height:${size * 1.65}px;border-radius:50%;background:rgba(255,255,255,.12)"></div>`;
      if (e === '+') h += `<div class="mt-plus" style="left:${x}px;top:${cy}px;width:${size * .82}px;height:${size * .82}px;font-size:${size * .8}px"><svg width="${size * .6}" height="${size * .6}" viewBox="0 0 10 10"><path d="M4 1h2v3h3v2H6v3H4V6H1V4h3z" fill="#fff"/></svg></div>`;
      else h += `<div class="mt-emo" style="left:${x}px;top:${cy}px;font-size:${size}px">${e}</div>`;
    });
    h += `<div class="mt-c" style="left:${cx + addX}px;top:${cy}px">${svg('add_reaction', size * 1.05, C.icon)}</div>`;
    return h;
  }
  function speaking(x, y, d = 20) {
    return `<div class="mt-c" style="left:${x}px;top:${y}px;width:${d}px;height:${d}px;border-radius:50%;background:rgba(190,205,250,.9)">
      <svg width="${d * .6}" height="${d * .6}" viewBox="0 0 12 12"><rect x="1.5" y="3.5" width="2" height="5" rx="1" fill="#1d3a9a"/><rect x="5" y="1.5" width="2" height="9" rx="1" fill="#1d3a9a"/><rect x="8.5" y="3.5" width="2" height="5" rx="1" fill="#1d3a9a"/></svg></div>`;
  }
  // A whole Meet page. All geometry in page px.
  // o = {W,H, bg, tile:{x,y,w,h,r}, pip:{x,y,w,h,r,label,labelSize}, name:{text,x,y,size}, speak:{x,y,d}|null,
  //      bar:{cx,cy,emojiActive}, react:{cy,size,hoverIdx}|null, header:{time,title,x,y,size}|null, right:[{icon,x,y,size}]}
  function page(o) {
    injectCSS();
    const bg = o.bg || C.bg; let h = '';
    if (o.tile) { const t = o.tile; h += `<div class="mt-hole" style="left:${t.x}px;top:${t.y}px;width:${t.w}px;height:${t.h}px;border-radius:${t.r}px;box-shadow:0 0 0 ${o.W + o.H}px ${bg}${o.tileFill ? ';background:' + o.tileFill : ''}"></div>`; }
    else h += `<div class="mt-hole" style="left:0;top:0;width:${o.W}px;height:${o.H}px;background:${bg}"></div>`;
    if (o.pip) {
      const p = o.pip; h += `<div class="mt-pipring" style="left:${p.x}px;top:${p.y}px;width:${p.w}px;height:${p.h}px;border-radius:${p.r}px"></div>`;
      if (p.label) h += `<div class="mt-lbl" style="left:${p.x + (p.lx ?? 8)}px;top:${p.y + p.h - (p.ly ?? 6)}px;transform:translateY(-100%);font-size:${p.labelSize || 9}px">${p.label}</div>`;
    }
    if (o.name) h += `<div class="mt-lbl" style="left:${o.name.x}px;top:${o.name.y}px;transform:translateY(-50%);font-size:${o.name.size || 12}px">${o.name.text}</div>`;
    if (o.speak) h += speaking(o.speak.x, o.speak.y, o.speak.d);
    if (o.header) { const hd = o.header; h += `<div class="abs" style="left:${hd.x}px;top:${hd.y}px;transform:translateY(-50%);display:flex;align-items:center;gap:${hd.size * .55}px;font-size:${hd.size}px;font-weight:500;color:#e3e3e3;white-space:nowrap">${hd.time ? `<span>${hd.time}</span><span style="width:1px;height:${hd.size * 1.1}px;background:#8e918f"></span>` : ''}<span>${hd.title}</span>${svg('info', hd.size * 1.15, '#c4c7c5')}</div>`; }
    if (o.react) h += reactions({ cx: o.bar.cx, cy: o.react.cy, size: o.react.size || 16, hoverIdx: o.react.hoverIdx ?? -1 });
    if (o.bar) h += toolbar({ cx: o.bar.cx, cy: o.bar.cy, emojiActive: o.bar.emojiActive !== false });
    for (const r of (o.right || [])) h += `<div class="mt-c" style="left:${r.x}px;top:${r.y}px">${svg(r.icon, r.size || 20, C.icon)}</div>`;
    return `<div class="mt-page" style="width:${o.W}px;height:${o.H}px">${h}</div>`;
  }
  // floating reaction bubble (emoji + "You" pill) used by HF-28 / HF-30
  function bubble(emoji, size = 22, you = true) {
    return `<div style="position:relative;width:${size}px;height:${size}px"><div class="mt-emo" style="left:50%;top:50%;font-size:${size}px">${emoji}</div>${you ? `<div style="position:absolute;left:50%;top:${size * 1.05}px;transform:translateX(-50%);font:600 ${size * .36}px GS,Arial;color:#0b1d4a;background:rgba(200,215,250,.92);border-radius:${size}px;padding:${size * .04}px ${size * .22}px;white-space:nowrap">You</div>` : ''}</div>`;
  }
  window.MEET = { ICON, svg, REACT, CTRL, C, page, toolbar, reactions, speaking, bubble, injectCSS };
})();
