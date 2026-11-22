// Shared helpers for the screens/UI assets (HF-07..HF-30, builder 1). Classic script -> window.CM.
// - fonts (Google Sans Flex as 'GS'), full-frame stage, QA guide underlay (PARAMS.guide=true draws qa/guide/gNNNN.jpg,
//   pre-extracted reference frames at 24 fps; never on in final renders).
(function () {
  const P = window.PARAMS || {};
  const st = document.createElement('style');
  st.textContent = `
  @font-face{font-family:GS;src:url('file:///Users/faseeh/Developer/Chatly/reels/chatly-smb/brand/fonts/GoogleSansFlex.woff2') format('woff2');font-weight:1 1000;font-stretch:25% 151%}
  html,body{margin:0;width:1440px;height:1080px;overflow:hidden;background:transparent}
  #guide{position:absolute;left:0;top:0;width:1440px;height:1080px;display:none;z-index:0}
  #stage{position:absolute;left:0;top:0;width:1440px;height:1080px;overflow:hidden;z-index:1}
  .abs{position:absolute}`;
  document.head.appendChild(st);
  let img = null;
  const CM = {
    P,
    pad: (k, n = 4) => String(k).padStart(n, '0'),
    clamp: (v, a = 0, b = 1) => Math.max(a, Math.min(b, v)),
    lerp: (a, b, u) => a + (b - a) * u,
    ease: u => 1 - Math.pow(1 - u, 3),
    easeIO: u => u < .5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2,
    rng(s) { return () => { s |= 0; s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; },
    frame: t => Math.round(t * 24),
    async fonts() { try { await document.fonts.load('500 20px GS'); await document.fonts.load('700 20px GS'); await document.fonts.load('400 20px GS'); } catch (e) { } await document.fonts.ready; },
    // Call once after body exists.
    initGuide() {
      img = document.createElement('img'); img.id = 'guide'; document.body.insertBefore(img, document.body.firstChild);
      if (P.guide) { img.style.display = 'block'; document.body.style.background = '#000'; }
    },
    async guideAt(t) {
      if (!P.guide || !img) return;
      img.src = `${P.guideDir || 'qa/guide'}/g${CM.pad(Math.round(t * 24))}.jpg`;
      try { await img.decode(); } catch (e) { }
    },
    // in guide mode, punch holes at reduced opacity so the ref shows through the UI too (alignment check)
    guideOpacity() { return P.guide ? (P.gop ?? 0.55) : 1; },
  };
  window.CM = CM;
})();
