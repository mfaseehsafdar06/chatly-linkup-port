// node gen/stills.mjs globe|hand   -> gen/<name>.png  (fal nano-banana-pro, 1 image each)
import { fal, falKey, grab } from '../../../../tools/lib/fal.mjs';
import { writeFileSync } from 'node:fs';
const D = new URL('./', import.meta.url).pathname;
const key = falKey(new URL('../../../../', import.meta.url).pathname);
const P = {
  globe: { aspect_ratio: '4:3', prompt: 'Top-down flat photograph of a hand-drawn crayon drawing of planet Earth on plain white printer paper. One filled circle in the center taking about 70% of the frame height, simple childlike continents in bright grass green wax crayon, oceans in bright cyan sky-blue wax crayon, heavy waxy diagonal crayon strokes, visible paper tooth showing through as tiny white specks, slightly uneven rough circle edge, small crayon crumbs on the paper. Lots of empty white paper around the circle, no text, no shadows, even soft daylight, shot on a phone, realistic, slightly soft focus.' },
  hand: { aspect_ratio: '16:9', prompt: 'Realistic close-up photo of a young woman\'s right hand holding a chunky marker pen like writing, entering from the right edge of the frame. The marker is held horizontally with its tip pointing to the left, tip near the left-center of the frame. Marker: white plastic barrel with green wavy stripe pattern, red plastic collar and rounded red felt chisel tip. Thumb and index finger visible gripping the barrel, natural skin texture, short natural nails, no rings. Isolated on a perfectly flat solid pure blue background (#0047FF), no shadows on the background, soft even studio light, sharp focus, photographic.' },
};
const name = process.argv[2];
const r = await fal(key, 'fal-ai/nano-banana-pro', { ...P[name], resolution: '2K', num_images: 1, output_format: 'png' });
writeFileSync(`${D}${name}.json`, JSON.stringify(r, null, 1));
await grab(r.images[0].url, `${D}${name}.png`); console.log(name, r.images[0].url);
