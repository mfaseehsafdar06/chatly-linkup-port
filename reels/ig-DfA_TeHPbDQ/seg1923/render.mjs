// node render.mjs [outdir] [k0] [k1] [params-json]
import puppeteer from '/Users/faseeh/.npm/_npx/110f701c48e68d66/node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js';
import { mkdirSync } from 'node:fs';
const D = new URL('./', import.meta.url).pathname;
const [out = 'frames', k0 = '0', k1 = '101', params = '{}'] = process.argv.slice(2);
mkdirSync(D + out, { recursive: true });
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', protocolTimeout: 300000,
  args: ['--allow-file-access-from-files', '--disable-web-security', '--force-color-profile=srgb'] });
const p = await b.newPage(); await p.setViewport({ width: 1440, height: 1080, deviceScaleFactor: 1 });
await p.evaluateOnNewDocument(`window.PARAMS=${params}`);
p.on('console', m => console.log('page:', m.text())); p.on('pageerror', e => console.log('ERR', e.message));
await p.goto('file://' + D + 'film.html'); await p.evaluate(() => window.ready);
for (let k = +k0; k <= +k1; k++) {
  await p.evaluate(t => window.render(t), k / 24);
  const el = await p.$('canvas'); await el.screenshot({ path: `${D}${out}/k${String(k).padStart(3, '0')}.png` });
}
await b.close(); console.log('done');
