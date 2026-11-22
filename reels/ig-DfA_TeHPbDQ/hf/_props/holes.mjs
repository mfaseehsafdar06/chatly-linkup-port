// Dump the photo-window hole quad per frame for a report-card asset: node holes.mjs <assetDir> <frames>
// Writes <asset>/out/<name>-hole.json : [{frame, quad:[[x,y]x4] (TL,TR,BR,BL, output px)}] — where the live plate must sit.
import puppeteer from '/Users/faseeh/.npm/_npx/110f701c48e68d66/node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js';
import { writeFileSync } from 'node:fs'; import { resolve, basename } from 'node:path';
const dir = resolve(process.argv[2]), n = +process.argv[3];
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--allow-file-access-from-files', '--disable-web-security'] });
const p = await b.newPage(); await p.setViewport({ width: 1440, height: 1080 }); await p.goto('file://' + dir + '/index.html'); await p.evaluate(() => window.ready);
const out = []; for (let k = 0; k < n; k++) out.push({ frame: k, quad: await p.evaluate(t => window.hole(t), k / 24) });
await b.close(); writeFileSync(`${dir}/out/${basename(dir)}-hole.json`, JSON.stringify(out)); console.log('holes', out.length);
