// One full-res still of an asset page at any viewport size (for the in-camera UI refs).
// node hf/_linkup/still.mjs <assetDir> <w> <h> <out.png> [t] [paramsJSON]
import puppeteer from '/Users/faseeh/.npm/_npx/110f701c48e68d66/node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js';
import { resolve } from 'node:path';
const [dir, w, h, out, t = '0', params = '{}'] = process.argv.slice(2);
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new',
  args: ['--allow-file-access-from-files', '--disable-web-security', '--force-color-profile=srgb', '--font-render-hinting=none'] });
const p = await b.newPage(); await p.setViewport({ width: +w, height: +h, deviceScaleFactor: 1 });
await p.evaluateOnNewDocument(`window.PARAMS=${params}`);
p.on('pageerror', e => console.log('ERR', e.message));
await p.goto('file://' + resolve(dir) + '/index.html'); await p.evaluate(() => window.ready);
await p.evaluate(t => window.render(t), +t);
await p.screenshot({ path: out, clip: { x: 0, y: 0, width: +w, height: +h } });
await b.close(); console.log('wrote', out);
