/* ============================================================
   FAL — the queue API, over plain fetch

   Shared by tools/intro.mjs (cold opens) and tools/ugc.mjs (UGC
   talent clips) so the one non-obvious thing about this API is
   written down once. Zero dependencies, same as the rest of the
   pipeline.
   ============================================================ */
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { setTimeout as sleep } from 'node:timers/promises';

export const falKey = (root) => {
  const env = readFileSync(resolve(root, '.env'), 'utf8');
  const key = env.match(/^FAL=(.+)$/m)?.[1]?.trim();
  if (!key) throw new Error('no FAL= in .env');
  return key;
};

/* fetch() rejects outright on a dropped connection, and these jobs
   run for minutes at a time — one blip 18 minutes in should not
   throw away the work or the money already spent. Everything that
   touches the network goes through here.

   Only the transport is retried. An HTTP error the server actually
   returned is a real answer and is left to the caller, because
   retrying a rejected prompt just pays for the same refusal twice. */
async function tryFetch(url, init, what) {
  let last;
  for (let attempt = 1; attempt <= 4; attempt += 1) {
    try { return await fetch(url, init); } catch (e) {
      last = e;
      if (attempt < 4) await sleep(attempt * 2000);
    }
  }
  throw new Error(`${what}: ${last?.message ?? 'fetch failed'} after 4 tries`);
}

export async function fal(key, model, input) {
  const headers = { Authorization: `Key ${key}`, 'Content-Type': 'application/json' };
  const submit = await tryFetch(`https://queue.fal.run/${model}`, {
    method: 'POST', headers, body: JSON.stringify(input),
  }, `${model} submit`);
  if (!submit.ok) throw new Error(`${model}: submit ${submit.status} ${await submit.text()}`);
  const job = await submit.json();

  /* THE ONE TRAP. fal hands back status_url and response_url on the
     BASE model path, not the sub-path you posted to — a POST to
     /nano-banana-pro/edit answers with /nano-banana-pro/requests/…
     and a POST to /seedance-2.0/fast/image-to-video answers with
     /seedance-2.0/requests/…. Build those URLs yourself from the
     model id and every poll 404s. Follow the ones it gives. */
  for (let i = 0; i < 600; i += 1) {
    await sleep(2000);
    /* A long outage mid-poll is not a failed job — the job keeps
       running (and billing) on fal's side. Keep polling. */
    let st;
    try { st = await (await tryFetch(job.status_url, { headers }, `${model} status`)).json(); } catch { continue; }
    if (st.status === 'COMPLETED') break;
    if (st.status !== 'IN_QUEUE' && st.status !== 'IN_PROGRESS') {
      throw new Error(`${model}: ${JSON.stringify(st).slice(0, 400)}`);
    }
    if (i === 599) throw new Error(`${model}: still ${st.status} after 20 min`);
  }
  const out = await (await tryFetch(job.response_url, { headers }, `${model} response`)).json();
  if (out.detail) throw new Error(`${model}: ${JSON.stringify(out.detail).slice(0, 400)}`);
  return out;
}

export const grab = async (url, dest) => {
  const r = await tryFetch(url, {}, 'download');
  if (!r.ok) throw new Error(`fetch ${url}: ${r.status}`);
  writeFileSync(dest, Buffer.from(await r.arrayBuffer()));
};

export const dataUri = (path, mime) =>
  `data:${mime};base64,${readFileSync(path).toString('base64')}`;
