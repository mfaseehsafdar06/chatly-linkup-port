// Render one HyperFrames-style asset.
// node hf/lib/render.mjs <assetDir> <durSec> [--alpha] [--from s] [--params json]
//   assetDir/index.html must define window.render(t) (t = seconds from the asset's own start) and window.ready (promise).
//   1440x1080, 24 fps. Writes assetDir/tmp/frames/k%04d.png then assetDir/out/<name>.mp4 (or .mov ProRes 4444 with --alpha).
import puppeteer from '/Users/faseeh/.npm/_npx/110f701c48e68d66/node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js';
import { mkdirSync, rmSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { resolve, basename } from 'node:path';
const a = process.argv.slice(2); const dir = resolve(a[0]); const dur = +a[1];
const alpha = a.includes('--alpha'); const fi = a.indexOf('--from'); const from = fi > 0 ? +a[fi + 1] : 0;
const pi = a.indexOf('--params'); const params = pi > 0 ? a[pi + 1] : '{}';
const only = a.indexOf('--frames'); // --frames 0,12,40 : stills only (for compare), no encode
const F = `${dir}/tmp/frames`; rmSync(F, { recursive: true, force: true }); mkdirSync(F, { recursive: true }); mkdirSync(`${dir}/out`, { recursive: true });
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', protocolTimeout: 600000,
  args: ['--allow-file-access-from-files', '--disable-web-security', '--force-color-profile=srgb', '--font-render-hinting=none'] });
const p = await b.newPage(); await p.setViewport({ width: 1440, height: 1080, deviceScaleFactor: 1 });
await p.evaluateOnNewDocument(`window.PARAMS=${params}`);
p.on('pageerror', e => console.log('ERR', e.message)); p.on('console', m => { if (m.type() === 'error') console.log('console:', m.text()); });
await p.goto('file://' + dir + '/index.html'); await p.evaluate(() => window.ready);
const ks = only > 0 ? a[only + 1].split(',').map(Number) : [...Array(Math.round(dur * 24)).keys()];
for (const k of ks) {
  await p.evaluate(t => window.render(t), from + k / 24);
  await p.screenshot({ path: `${F}/k${String(k).padStart(4, '0')}.png`, omitBackground: alpha, clip: { x: 0, y: 0, width: 1440, height: 1080 } });
}
await b.close();
if (only > 0) { console.log('stills in', F); process.exit(0); }
const name = basename(dir);
if (alpha) execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', '24', '-i', `${F}/k%04d.png`, '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', `${dir}/out/${name}.mov`]);
else execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', '24', '-i', `${F}/k%04d.png`, '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', `${dir}/out/${name}.mp4`]);
console.log('wrote', `${dir}/out/${name}.${alpha ? 'mov' : 'mp4'}`, ks.length, 'frames');
