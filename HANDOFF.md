# Handoff: Chatly port of the Lovable "LinkUp" reel

Read this first. It covers what has been decided, what is built, how it was built, and what comes next. Last updated 2026-11-22.

## 1. The project

- **Reference:** Lovable's Instagram reel https://www.instagram.com/p/DfA_TeHPbDQ/ (76.2 s, 4:3, 960×720, 24 fps).
  - Ying narrates a creator story: her friend Leo has to book calls across five timezones, so Ying builds an app called "LinkUp" with one request to Lovable.
  - It ends "comment LINK UP" and "a ♥ Lovable story".
- **Goal:** an exact clone of that reel for **Chatly** (chatlyai.app). Same shots, timing, framing and look, with only the branding and the product UI changed.
- **Decisions already made:**
  - Brand: Chatly.
  - Aspect: 4:3 like the reference, at 1440×1080 and 24 fps.
  - Live-action shots: Seedance, kept lean. Every paid generation still needs the owner's go-ahead first.

## 2. What exists

| Part | Status | Where |
|---|---|---|
| Full study of the reference | Done | `reels/ig-DfA_TeHPbDQ/REF.md` (transcript, 55-shot list with cut times) |
| Chatly port plan | Done, not started | `reels/ig-DfA_TeHPbDQ/PORT.md` (script changes, 15 Seedance clips, ~30K credits, build order) |
| Storyboard of the reference | Done | `reels/ig-DfA_TeHPbDQ/storyboard/storyboard.jpg` (one frame per shot); single frames in `storyboard/frames/` |
| Contact sheets at 10 fps | Done | `reels/ig-DfA_TeHPbDQ/refs/sheets/s01–s39.jpg` (all 762 frames, timestamped) |
| **19.2–23.4 s section** (crayon globe + wall map) | **Built, current = real-v2** | `reels/ig-DfA_TeHPbDQ/seg1923/` |

### The 19–23 s section (the only shot sequence built so far)

8 shots, 4.25 s:

| # | Shot | Time |
|---|---|---|
| 1 | Crayon globe; "all / over / the / world" pops in word by word | 19.17–20.29 |
| 2 | Map close-up: a red marker circles Singapore | 20.29–21.04 |
| 3 | Circles Australia, counter-clockwise | 21.04–21.62 |
| 4 | Circles Canada; marker enters from the left | 21.62–22.08 |
| 5 | "NY!" is written, circle on New York, then the dot of the "!" | 22.08–22.67 |
| 6 | Circles the UK | 22.67–23.12 |
| 7 | Whip-zoom out with motion blur | 23.12–23.25 |
| 8 | Full world map with every mark | 23.25–23.42 |

Outputs, in `seg1923/out/`:
- **`seg1923-real-v2-4x3.mp4`:** current version.
- `seg1923-real-v2-side-by-side.mp4`: reference and ours side by side.
- `seg1923-final-4x3.mp4` and `seg1923-side-by-side.mp4`: the earlier all-code version (v1), rejected as "not real enough".
- `seg1923-storyboard.png`: our 8 shots with the reference frame at the same moment.

The audio on these clips is the reference's own voiceover, there only to check timing. It gets replaced in the Chatly version.

## 3. How the section is built (zero video generation)

- **`film.html`:** a canvas page with `window.render(t)` for t in seconds (0 = 19.167 s in the reference). It draws:
  - **Globe:** a generated photo of a real crayon drawing (`gen/globe.png`), fitted into 4 slightly warped variants (`gen/globe_v0-3.png`, from `prep.py`). They swap every 2 frames, so it wobbles like the reference. The words are Helvetica Neue Bold.
  - **Map:** the CIA 2015 political world map, which is public domain (`src/world_pol_2015.pdf` from the UT Austin map library). It was rasterised at 300 dpi and cropped to `src/map2.jpg`, with the outside-page white filled with ocean colour and the title and legend painted out.
    - Cameras are set per shot as map point → screen point at a given scale (`CAM` in film.html).
    - Scales were measured against the reference.
    - Each shot has a handheld drift and a slow push.
  - **Marker ink:** circles animate along hand-wobbled ellipses (`MARKS`), with a darker pooled edge, a lighter core and a dry streak.
  - **"NY!":** the reference's own handwriting, lifted as ink masks from the reference frames by `nyink.py` (`gen/ny_base.png`, `ny_bang.png`, `ny_dot.png`). The "!" stroke wipes in and the dot pops while the marker passes.
  - **Hand and marker:** a generated photo of a real hand holding a white/green/red marker, keyed off blue (`gen/hand.png` → `gen/hand_rgba.png`).
    - It is placed with the marker tip on the moving end of the stroke.
    - Per shot, it is foreshortened, rotated and blurred.
    - Motion blur comes from 6 sub-frames per frame; the whip-zoom uses 24.
- **`render.mjs`:** renders frames with puppeteer and Chrome. Usage: `node render.mjs <outdir> 0 101`.
- **`post2.py`:** the photographed-print look on the map shots:
  - focus falloff toward one edge
  - laminate glare band and paper texture
  - light vignette and slight chromatic aberration
  - per-shot Lab colour match to the reference shot, and grain

  The globe shots only get the colour match, softness and grain.
- **`compare.py`:** builds sheets with the reference on the left and ours on the right at the same frame numbers, into `qa/`. **Use it after every change.**
- **`gen/stills.mjs`:** the two fal `nano-banana-pro` calls (globe, hand). They have already been run and the results are committed, so **don't re-run them** unless the owner asks.

### Rebuild

```bash
cd reels/ig-DfA_TeHPbDQ
./fetch_ref.sh                       # re-downloads the reference + extracts refs/f10 and seg1923/ref24 (not in the repo)
cd seg1923
node render.mjs frames_v9 0 101      # 102 frames, ~20 s
python post2.py frames_v9 frames_v9g # grade + print look (needs ref24)
python compare.py frames_v9g v9 22 36 50 66 78 86 101   # pair sheets -> qa/v9_*.jpg
ffmpeg -framerate 24 -start_number 0 -i frames_v9g/k%03d.png -c:v libx264 -crf 14 -pix_fmt yuv420p out/seg1923.mp4
```

Requirements and setup:
- Node, plus `puppeteer-core` and Google Chrome. `render.mjs` has absolute paths to both from the original Mac; change them to your own.
- Python 3 with `opencv-python`, `numpy` and `pillow`.
- ffmpeg and yt-dlp.
- To generate images on fal, a `.env` at the repo root with `FAL=<key>` (read by `tools/lib/fal.mjs`).

`film_v1.html`–`film_v5.html` are the earlier rounds and `film_real_v2.html` is a snapshot of the current one. They're kept for history.

## 4. What the owner said, and the rules that follow

- **"Make me exact same thing… make it, compare it, fix it, compare it, fix it, compare it, finalize it."** Work in rounds: render, compare side by side with the reference at the same frame numbers (`compare.py`), list the differences, fix, repeat at least 3 times. Then hand over.
- **"Theirs is more real… the marker and the map, even the earth."** Code-drawn crayon and hands read as fake. Real textures come from photos: generated stills, or real footage. Code stays for timing, motion, layout and the accuracy of the map text.
- **Study at 10 fps.** Look at every frame of the reference section before building.
- **Ask before any paid generation.** State the model and the count, then wait for a yes. Only the required minimum: no drafts or spare variants. Seedance is opt-in every time.
- **Chatly brand rules:**
  - The site is chatlyai.app, never chatly.ai.
  - Every video ends on "Chatly. AI that works 24/7 for you."
  - Show the real Chatly UI and a finished deliverable; say "ask", not "prompt".
  - Never mix in EverAsk or ImagineArt branding.
- **Port the script almost word for word.** Change only the brand, the product UI and lines about things Chatly can't do (see PORT.md).

## 5. Known gaps in the 19–23 s section

- The map artwork differs from the reference's wall map: the reference has larger labels, Russia in pink and a legend box. The labels and colours can't match exactly, because a generated map would scramble the text in close-up.
- The hand is a still photo moved along the stroke, so the fingers don't flex.
- The reference's map is the "laminated wall map" type. If the owner wants the map closer, the realistic option is to buy or print a similar map and film a few seconds of it.

## 6. Next steps (from PORT.md)

1. Build every code and UI part of the rest of the reel, with the edit on placeholders, and check timing against the reference. These parts are:
   - the paper kinetic type
   - the report card
   - the Meet/webcam frames and the phone chat
   - the Chatly ask and build screens
   - the LinkUp app screens
   - captions and stickers
2. Make character sheets for Leo and Ying, and get them approved.
3. Generate the live-action clips (15 Seedance clips, about 77 s, about 30K credits), **after the owner approves the count**.
4. Grade, mix and add the Chatly outro, then do a final side-by-side compare with the reference.

## 7. Not in this repo

- **The reference video and its full-resolution frames.** It's Lovable's ad and this repo is public. `fetch_ref.sh` downloads it again.
- **The render frame folders** (about 3 GB). Re-render with `render.mjs`.
