// Prompt Library builders for the P-XX clips. Mirrors reference/chatly-web @ 079919718c:
//   modules/prompt-library/**, core/components/{fill-prompt-variables-modal,mentions-menu,prompt-variable-chip,prompt-visibility-*,used-prompt-pill},
//   core/utils/prompt-library/*, core/constants/{prompt-library,mentions}. Labels are the real gt-next strings.
import CU from '../../../../reference/chatly-ui-kit/chatly-ui.js';
export { CU };
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

// icons not in the kit, copied from packages/icons/src
const RAW = {
  people: '<svg viewBox="0 0 16 16" fill="none"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="SW" d="M11.833 9.649C13.42 9.982 14 11.06 14 11.963m-2.519-7.825a1.83 1.83 0 0 1 1.24 1.751 1.83 1.83 0 0 1-1.164 1.71M2 13.334c0-1.405 1.085-3.156 4.21-3.156s4.21 1.738 4.21 3.144M8.9 5.417c0 1.519-1.205 2.75-2.69 2.75s-2.69-1.231-2.69-2.75c0-1.52 1.205-2.75 2.69-2.75s2.69 1.23 2.69 2.75"/></svg>',
  lock: '<svg viewBox="0 0 16 16" fill="none"><path d="M12.1392 7.72719C12.1392 7.47686 12.0397 7.23679 11.8627 7.05978C11.6857 6.88278 11.4457 6.78334 11.1953 6.78334H4.58838C4.33805 6.78334 4.09799 6.88278 3.92098 7.05978C3.74397 7.23679 3.64453 7.47686 3.64453 7.72719V12.4464C3.64453 12.6968 3.74397 12.9369 3.92098 13.1138C4.09799 13.2908 4.33805 13.3903 4.58838 13.3903H8.30664M11.1953 6.68131V6.02711C11.1953 5.15097 10.8472 4.31072 10.2277 3.6912C9.60821 3.07168 8.76795 2.72363 7.89182 2.72363C7.01568 2.72363 6.17542 3.07168 5.55591 3.6912C4.93638 4.31072 4.58834 5.15097 4.58834 6.02711V6.68131M12.1404 7.72719V12.4464C12.1404 12.6968 12.041 12.9369 11.864 13.1138C11.687 13.2908 11.4469 13.3903 11.1966 13.3903H7.47832" stroke="currentColor" stroke-width="SW" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  msg: '<svg viewBox="0 0 18 18" fill="none"><path d="M6.75 7.531H11.25M6.75 10.531H11.25M2.25 7.132C2.25 5.068 3.929 3.395 6 3.395H12C14.071 3.395 15.75 5.068 15.75 7.132V13.859C15.75 14.272 15.414 14.607 15 14.607H6C3.929 14.607 2.25 12.934 2.25 10.87V7.132Z" stroke="currentColor" stroke-width="SW" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  trash: '<svg viewBox="0 0 16 16" fill="none"><path stroke="currentColor" stroke-width="SW" stroke-linecap="round" stroke-linejoin="round" d="m12.46 6.365-.394 5.585C11.984 13.105 11.053 14 9.93 14H6.064c-1.121 0-2.053-.895-2.135-2.051l-.395-5.584m9.797-2.097H2.664m7.767 0-.325-1.651A.81.81 0 0 0 9.33 2h-2.66a.81.81 0 0 0-.781.617l-.322 1.65m1.206 3.588v3.005m2.182-3.005v3.005"/></svg>',
  wand: '<svg viewBox="0 0 20 20" fill="none"><path d="M15.0252 7.98346L12.5421 5.63017M3.01524 17.0117C3.70223 17.6628 4.81135 17.6628 5.49835 17.0117L16.2585 6.81408C16.9454 6.16301 16.9454 5.11187 16.2585 4.46079C15.5715 3.80971 14.4623 3.80971 13.7754 4.46079L3.01524 14.6584C2.32825 15.3095 2.32825 16.3606 3.01524 17.0117ZM7.15383 2.84515L8.39538 2.5L8.03119 3.67665L8.39538 4.85329L7.15383 4.50814L5.91228 4.85329L6.27646 3.67665L5.91228 2.5L7.15383 2.84515ZM3.84297 7.55172L5.08452 7.20657L4.72033 8.38322L5.08452 9.55986L3.84297 9.21471L2.60142 9.55986L2.96561 8.38322L2.60142 7.20657L3.84297 7.55172ZM16.2584 11.4741L17.5 11.1289L17.1358 12.3056L17.5 13.4822L16.2584 13.1371L15.0169 13.4822L15.3811 12.3056L15.0169 11.1289L16.2584 11.4741Z" stroke="currentColor" stroke-width="SW" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  check: '<svg viewBox="0 0 18 18" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M1.688 9a7.312 7.312 0 1 1 14.624 0A7.312 7.312 0 0 1 1.687 9Zm10.02-1.36a.562.562 0 1 0-.915-.654l-2.427 3.397-1.218-1.218a.563.563 0 0 0-.795.795l1.687 1.688a.562.562 0 0 0 .855-.071l2.813-3.938Z" fill="currentColor"/></svg>',
};
export const ic = (n, size = 16, sw = 1, color = 'currentColor') => RAW[n]
  ? `<span class="ic" style="width:${size}px;height:${size}px;color:${color}">${RAW[n].replace(/SW/g, sw)}</span>`
  : CU.icon(n, { size, sw, color });

// ---- prompt text -> segments (core/utils/prompt-library/parse-segments) ----
const VAR = /\{\{([A-Z_]\w*)\}\}/gi;
export function segments(text) { const out = []; let c = 0; for (const m of text.matchAll(VAR)) { if (m.index > c) out.push({ t: text.slice(c, m.index) }); out.push({ v: m[1] }); c = m.index + m[0].length; } if (c < text.length) out.push({ t: text.slice(c) }); return out; }
export const chip = (label, state = 'empty', ed = false) => `<span class="chip ${state}${ed ? ' ined' : ''}">${esc(label)}</span>`;
// editor rendering: completed tokens become EMPTY chips showing the bare name (VARIABLE_CHIP_CLASS_NAME + data-prompt-variable)
export const editorText = (text, caret = false) => segments(text).map(s => s.v != null ? chip(s.v, 'empty', true) : esc(s.t)).join('') + (caret ? '<span class="caret"></span>' : '');

export const TEMPLATE = 'Write 3 scroll-stopping hooks for a {{platform}} video about {{topic}}, in the voice of {{account}}, for {{audience}}.';
export const NAME = 'Scroll-stopping hooks';
export const ORG = 'Chatly'; // org name in "Everyone at {orgName}" (assumed; the owner's real workspace name may differ)
export const USER = { name: 'Faseeh', plan: 'Ultra Plan', avatar: '' };

// ---- library page (modules/prompt-library) ----
const AV_COL = { Faseeh: '#6B5BD6', Sara: '#E0794A', Omar: '#2E9E6A' };
export const OTHER_PROMPTS = [
  { name: 'Caption in brand voice', prompt: 'Rewrite this caption in the voice of {{account}} and keep it under 150 characters: {{caption}}', vis: 'team', by: 'Sara' },
  { name: 'Hashtag pack', prompt: 'Give me 15 hashtags for a {{platform}} post about {{topic}}, mixing big and niche tags.', vis: 'private', by: 'Faseeh' },
  { name: 'Weekly content calendar', prompt: 'Plan 7 days of posts for {{account}}: one idea per day with the format and a hook.', vis: 'team', by: 'Omar' },
];
export const MINE = { name: NAME, prompt: TEMPLATE, vis: 'private', by: 'Faseeh' };
export const badge = vis => `<span class="badge">${ic(vis === 'team' ? 'people' : 'lock', 12, 1)}</span>`;
export function promptCard(p, { hover = false, glow = 0 } = {}) {
  return `<article class="pcard${hover ? ' hov' : ''}" ${glow ? `style="box-shadow:0 0 0 ${2 * glow}px rgba(0,136,255,${0.35 * glow})"` : ''}><div class="row">
    <span class="pic">${ic('PromptLibraryIcon', 16, 1.2)}</span>
    <div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:8px">
      <div style="display:flex;align-items:center;gap:8px;min-width:0"><h3 class="body-sm" style="margin:0;font-weight:400;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${esc(p.name)}</h3>${badge(p.vis)}</div>
      <p class="lbl-md c3" style="margin:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${esc(p.prompt)}</p></div>
    <div class="acts" style="opacity:${hover ? 1 : 0}"><span class="ibtn">${ic('msg', 18, 1.5)}</span>${p.by === 'Faseeh' ? `<span class="ibtn">${ic('PencilIcon', 18, 1.5)}</span><span class="ibtn">${ic('trash', 18, 1.5)}</span>` : ''}</div></div>
    <p class="by lbl-sm c3" style="margin:0">by <span style="display:inline-flex;align-items:center;gap:4px"><span class="av" style="background:${AV_COL[p.by] || '#888'}">${p.by[0]}</span><span class="c2">${esc(p.by)}</span></span></p></article>`;
}
export function libraryPage({ prompts, tab = 'all', hover = -1, glow = -1, glowA = 0 }) {
  const tabs = [['all', 'All'], ['mine', 'My prompts'], ['team', 'Team prompts']].map(([k, l]) => `<div class="tab${k === tab ? ' on' : ''}">${l}</div>`).join('');
  return `<div class="plc">
    <header class="plhdr"><div style="display:flex;flex-direction:column;gap:8px;min-width:0"><h1 class="h-xs" style="margin:0">Prompt library</h1>
      <p class="lbl-md c2" style="margin:0">Save prompts that work. Fill in the blanks each time you use them.</p></div>
      <span class="btn sm pri">${ic('PlusIcon', 16, 1.2, '#fff')}New prompt</span></header>
    <div style="display:flex;flex-direction:column;gap:24px">
      <div style="display:flex;align-items:center;justify-content:space-between;gap:12px"><div class="tabs">${tabs}</div>
        <div class="search">${ic('SearchIcon', 16, 1.5, 'rgba(15,15,15,.5)')}<span>Search prompts</span></div></div>
      <div class="grid">${prompts.map((p, i) => promptCard(p, { hover: i === hover, glow: i === glow ? glowA : 0 })).join('')}</div></div></div>`;
}
// sidebar + navbar + main (SidebarLayout); main = any HTML
export function shell({ main = '', activeNav = 'prompt-library', recents, h = 1080, overlay = '' }) {
  const sb = CU.sidebar({ activeNav, user: USER, recents: recents || ['Hooks for @gymtok.daily', 'Leg day carousel ideas', 'Study hacks captions', 'Sneaker drop countdown', 'Meal prep reel script'] });
  return `<div class="cu" style="display:flex;width:1920px;height:${h}px;background:#fff">${sb}
    <div style="flex:1;min-width:0;display:flex;flex-direction:column;position:relative">${CU.navbar({ home: true, upgrade: true })}
      <div class="plpage pl" style="position:relative;flex:1">${main}</div></div>${overlay}</div>`;
}

// ---- New / Edit prompt modal (prompt-editor-dialog) ----
export function editorModal({ edit = false, name = NAME, nameFocus = false, vis = 'private', text = TEMPLATE, caret = false, edFocus = false,
  ddOpen = false, ddHover = '', saveHover = false, saveDown = false, visHover = false }) {
  const count = `${text.length.toLocaleString('en-US')} / 20,000`;
  const visLabel = vis === 'team' ? `Everyone at ${ORG}` : 'Only you';
  const dd = ddOpen ? `<div class="dd" style="right:0;top:calc(100% + 4px)">${[['private', 'Only you', 'Only you can see and use it'], ['team', `Everyone at ${ORG}`, `Anyone at ${ORG} can find and use it`]].map(([v, l, d]) =>
    `<div class="ddo${v === vis ? ' on' : ''}${ddHover === v && v !== vis ? ' hov' : ''}"><span class="ci">${ic(v === 'team' ? 'people' : 'lock', 16, 1)}</span>
      <span style="flex:1;min-width:0;display:flex;flex-direction:column;gap:2px"><span class="lbl-md w5">${l}</span><span class="lbl-sm c2">${d}</span></span>
      <span style="width:18px;height:18px;flex:none">${v === vis ? ic('check', 18, 1, 'rgba(15,15,15,.5)') : ''}</span></div>`).join('')}</div>` : '';
  return `<div class="ovl"></div><div class="modal pl" id="modal">
    <div class="mh"><div class="tt"><h2 class="h-xs" style="margin:0">${edit ? 'Edit prompt' : 'New prompt'}</h2>
      <p class="lbl-sm c2" style="margin:0">Write it once and reuse it. Type {{ }} around a word, like {{audience}}, to make it a variable.</p></div>
      <span class="ibtn">${ic('CrossIcon', 18, 1.2)}</span></div>
    <div style="display:flex;flex-direction:column;gap:24px">
      <div style="display:flex;gap:16px">
        <div class="fld" style="flex:1;min-width:0"><span class="l">Name</span><div class="inp${nameFocus ? ' foc' : ''}">${name ? esc(name) : '<span class="ph">Give it a name</span>'}</div></div>
        <div class="fld" style="width:200px;flex:none;position:relative"><span class="l">Who can use it</span><div class="inp${ddOpen ? ' foc' : ''}" style="${visHover ? 'background:#F0F0F0;' : ''}">${ic(vis === 'team' ? 'people' : 'lock', 16, 1)}
          <span style="flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${visLabel}</span>${ic('DropdownIcon', 16, 0.5)}</div>${dd}</div></div>
      <div style="display:flex;flex-direction:column;gap:12px">
        <div style="display:flex;align-items:center;gap:8px"><span class="lbl-sm w5 c2" style="flex:1">Prompt</span><span class="btn xs ghost" style="margin:-4px 0">${ic('PlusIcon', 14, 1.2)}Add variable</span></div>
        <div class="ed${edFocus ? ' foc' : ''}"><div class="tx">${editorText(text, caret)}</div>
          <div style="display:flex;align-items:center;justify-content:space-between;gap:8px"><span class="btn xs outline">${ic('wand', 14, 1)}Enhance</span><span class="lbl-sm c3" style="font-variant-numeric:tabular-nums">${count}</span></div></div></div></div>
    <div class="mf"><span class="btn md ghost">Cancel</span><span class="btn md pri${saveHover ? ' hov' : ''}" style="${saveDown ? 'transform:scale(.97)' : ''}">${edit ? 'Save changes' : 'Save prompt'}</span></div></div>`;
}

// ---- Fill in the blanks (AddPromptModal -> FillPromptVariablesModal) ----
export const VARS = ['platform', 'topic', 'account', 'audience'];
const label = n => n[0].toUpperCase() + n.slice(1).toLowerCase(); // upperFirst(lowerCase(name))
export function fillModal({ values = {}, active = null, caret = true, addHover = false, addDown = false }) {
  const prev = segments(TEMPLATE).map(s => { if (s.v == null) return esc(s.t); const v = (values[s.v] || '').trim(); return chip(v || s.v, active === s.v ? 'active' : v ? 'filled' : 'empty'); }).join('');
  const fields = VARS.map(n => `<div class="vf"><span class="l">${label(n)}</span><div class="in${active === n ? ' foc' : ''}">${values[n] ? esc(values[n]) : ''}${active === n && caret ? '<span class="caret" style="height:17px"></span>' : ''}${values[n] ? '' : `<span class="ph">${label(n)}</span>`}</div></div>`).join('');
  return `<div class="ovl"></div><div class="modal pl" id="modal">
    <div class="mh"><div class="tt"><h2 class="h-xs" style="margin:0">${NAME}</h2><p class="lbl-sm c2" style="margin:0">Fill in the blanks. You can still edit the prompt before you send it.</p></div><span class="ibtn">${ic('CrossIcon', 18, 1.2)}</span></div>
    <div style="display:flex;flex-direction:column;gap:20px"><p class="prev" style="margin:0">${prev}</p><div style="display:flex;flex-direction:column;gap:16px">${fields}</div></div>
    <div class="mf"><span class="lbl-sm c3" style="margin-right:auto;align-self:center">Tab moves to the next field</span><span class="btn md ghost">Cancel</span><span class="btn md pri${addHover ? ' hov' : ''}" style="${addDown ? 'transform:scale(.97)' : ''}">Add to prompt</span></div></div>`;
}
export const fillPrompt = values => segments(TEMPLATE).map(s => s.v != null ? (values[s.v] || `{{${s.v}}}`) : s.t).join('');

// ---- @ mentions: search results for the typed query (mentions-menu, non-cascade) + prompt preview ----
export function mentionMenu({ items, selected = 0 }) {
  return `<div class="mm pl" id="mm"><div class="lst"><p class="gl" style="margin:0">Prompt library</p>${items.map((p, i) =>
    `<div class="opt${i === selected ? ' sel' : ''}">${ic('PromptLibraryIcon', 16, 1.2)}<span class="lbl-md" style="flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${esc(p.name)}</span></div>`).join('')}</div></div>`;
}
export function promptPreview(p) {
  const n = segments(p.prompt).filter(s => s.v != null).length;
  return `<div class="pv pl" id="pv"><div style="display:flex;align-items:center;gap:8px"><p class="lbl-md w5" style="margin:0;flex:1;min-width:0">${esc(p.name)}</p>${badge(p.vis)}</div>
    <p class="tx" style="margin:0">${segments(p.prompt).map(s => s.v != null ? chip(s.v, 'empty') : esc(s.t)).join('')}</p>
    <p class="ft" style="margin:0">${n} variable${n === 1 ? '' : 's'} · by you</p></div>`;
}

// ---- cursor (macOS), drawn in app coordinates ----
const ARROW = `<svg width="17" height="24" viewBox="0 0 17 24"><path d="M1 1 L1 18.5 L5.2 14.6 L8 21.3 L10.9 20.1 L8.1 13.5 L13.8 13.5 Z" fill="#111" stroke="#fff" stroke-width="1.3" stroke-linejoin="round"/></svg>`;
const HAND = `<svg width="20" height="23" viewBox="0 0 20 23" style="left:-6px;top:-1px"><path d="M7.2 1.2c.9 0 1.6.7 1.6 1.6v6.3l.4-.1V7.6c0-.9.7-1.5 1.5-1.5s1.5.6 1.5 1.5v1.5l.4-.1c0-.8.7-1.4 1.5-1.4s1.5.6 1.5 1.5v1.3l.3-.1c.1-.7.7-1.1 1.4-1.1.8 0 1.4.6 1.4 1.4v5.6c0 3.4-2.4 6-5.8 6h-1.6c-2 0-3.4-.8-4.6-2.4L2 13.8c-.5-.7-.3-1.6.4-2 .6-.4 1.4-.3 1.9.2l1.3 1.4V2.8c0-.9.7-1.6 1.6-1.6z" fill="#fff" stroke="#111" stroke-width="1.1" stroke-linejoin="round"/><path d="M8.8 9v4.6M11.7 9.2v4.4M14.6 10.2v3.6" stroke="#111" stroke-width=".9" stroke-linecap="round"/></svg>`;
export const cursor = (x, y, kind = 'arrow', s = 1) => `<div class="mcur" style="left:${x}px;top:${y}px;transform:scale(${s})">${kind === 'hand' ? HAND : ARROW}</div>`;

// ---- filmed-screen camera: app point (ax,ay) -> screen (sx,sy), scale s, keystone (ry/rx) + roll (rz); DOF = blurred copy + masked sharp copy ----
export const lerp = (a, b, u) => a + (b - a) * u, sm = u => u * u * (3 - 2 * u), clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
export function keys(K, t, ease = sm) { if (t <= K[0][0]) return K[0][1]; for (let i = 0; i < K.length - 1; i++) if (t <= K[i + 1][0]) { const u = ease((t - K[i][0]) / (K[i + 1][0] - K[i][0])); const a = K[i][1], b = K[i + 1][1]; return Array.isArray(a) ? a.map((v, j) => lerp(v, b[j], u)) : lerp(a, b, u); } return K[K.length - 1][1]; }
export function stage({ height = 1080 } = {}) {
  const st = document.getElementById('stage');
  st.innerHTML = `<div class="cam" id="blur" style="height:${height}px"></div><div class="cam" id="sharp" style="height:${height}px"></div>`;
  const S = document.getElementById('sharp'), B = document.getElementById('blur');
  return {
    sharp: S, blur: B,
    frame(html, c) {
      S.innerHTML = html; B.innerHTML = html;
      const tf = `translate(${c.sx}px,${c.sy}px) perspective(2400px) rotateY(${c.ry || 0}deg) rotateX(${c.rx || 0}deg) rotateZ(${c.rz || 0}deg) scale(${c.s}) translate(${-c.ax}px,${-c.ay}px)`;
      S.style.transform = tf; B.style.transform = tf;
      S.style.setProperty('--fx', (c.ax / 19.2) + '%'); S.style.setProperty('--fy', (c.ay / (height / 100)) + '%');
      B.style.filter = `blur(${c.blur ?? 4}px)`; S.style.filter = c.soft ? `blur(${c.soft}px)` : '';
    },
  };
}
