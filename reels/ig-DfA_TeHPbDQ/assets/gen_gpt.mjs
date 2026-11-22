// node assets/gen_gpt.mjs [ids...]  -> assets/gpt/GPT-XX.png via fal openai/gpt-image-2 (quality high, 1 image each)
import { fal, falKey, grab } from '../../../tools/lib/fal.mjs';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
const D = new URL('./gpt/', import.meta.url).pathname;
const key = falKey(new URL('../../../', import.meta.url).pathname);
const P = JSON.parse(readFileSync(D + 'prompts.json', 'utf8'));
const SIZE = { 'GPT-03': [1536, 2048], 'GPT-07': [2048, 1536], 'GPT-10': [1536, 2048], 'GPT-13': [2048, 1024], 'GPT-06': [1536, 1536] };
const ids = process.argv.slice(2).length ? process.argv.slice(2) : Object.keys(P);
await Promise.all(ids.map(async id => {
  if (existsSync(`${D}${id}.png`)) return console.log(id, 'exists, skipped');
  const [w, h] = SIZE[id] || [2048, 1536];
  let r;
  try { r = await fal(key, 'openai/gpt-image-2', { prompt: P[id], image_size: { width: w, height: h }, quality: 'high', num_images: 1 }); }
  catch (e) { console.log(id, 'ERR', String(e).slice(0, 300)); return; }
  writeFileSync(`${D}${id}.json`, JSON.stringify(r, null, 1));
  await grab(r.images[0].url, `${D}${id}.png`); console.log(id, 'ok', w, h);
}));
