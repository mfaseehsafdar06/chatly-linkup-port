# "This is Faseeh" (Chatly Prompt Library): final edit build

**Output:** `reels/ig-DfA_TeHPbDQ/out/this-is-faseeh-chatly-v1-4x3.mp4` (1440×1080, 24 fps, 78.3 s, AAC 256k, −14 LUFS).

**Sources:** the owner's rough cut `1122.mov` and its VO `1122.WAV` (Downloads, 2026-11-22). The rough cut's timing is kept exactly; every black gap in it is filled with code graphics. The raw footage is in `faseeh/footage/`, which is not in git.

## Pipeline
1. **`fix_assets.py`:** pixel fixes on the gpt-image sticker cutouts, so they match the VO and cost nothing to regenerate. It writes `assets/cut/*_v1122.png`.
   - =630 → =360: the real 6 and 3 glyphs are swapped.
   - "in NEW YORK" → "in SAN FRANCISCO": Covered By Your Grace font on a widened sticker.
   - "+5" → "−8": the SF timezone sticker.
   - The scroll loses "@STUDYHACKS.PK [PK]" and gets a "[UK]" box (house rule: no South Asian markers).
2. **Re-renders:**
   - `hf/P-25-map`: the "−8" sticker on SF.
   - `hf/P-28-scroll-ticks`: the clean scroll.
   - `seg1923/film.html` with `PARAMS.nowords` set (the baked LinkUp words are removed). Run `render.mjs frames_nw 0 101 '{"nowords":1}'`, then `post2.py`, which gives `seg1923-real-v2-nowords-4x3.mp4`.
3. **New graphics** (`hf/lib/render.mjs <dir> <sec>`):
   - **`hf/P-31-posts-math`** (5.9 s):
     - "3 POSTS A DAY", with 3 notes labelled HOOKS, CAPTIONS and #HASHTAGS
     - the board floods with 360 notes
     - the "=360" sticker slams down, then "POSTS A WEEK"
   - **`hf/P-32-notes-montage`** (2 s): 6 marketers' Notes windows full of copy-paste prompts, after the reference's photo montage.
4. **`compose.py`:** the picture, built from one timeline function `frame_at(t)`.
   - **Grade:** live shots get the HeyClicky warm grade (`reels/chatly-chatapps/comp/grade.py`) and a 4:3 crop per shot (`cx`).
   - **Report cards:**
     - FAIL (3.63–4.97) shows Faseeh's Meet tile.
     - PASS (64.3–65.5) shows the dance continuing.
     - Both use the quads in `hole.json`.
   - **"Not the only one" (35.8–37.3):** a window on black with words around it, after reference 32 s.
   - **Stickers:** code-drawn (SF, #@$%!, 10 ACCOUNTS, OR 50, "PROMPTS"), each popping in with a 2-frame scale.
   - **Captions:** W are LinkUp-style Helvetica Neue Bold word pops. S are subtitles; over the UI screens they sit as dark text on a white pill.
   - **Transitions:** whips at 12.0, 18.967, 28.1, 62.467 and 65.533. A punch-in on "hell?" at 34.8.
   - **Black-frame guard:** live frames never come from the rough cut's black gaps.
   - Use `python compose.py --stills 1.4,6.6,...` for QA stills.
5. **`audio.py`:** the sound mix.
   - **VO:** 1122.WAV. The f-word at 10.89–11.31 is cut sample-accurately and replaced with a 1 kHz bleep. On screen it shows a "#@$%!" sticker and "What the".
   - **Music:** messwave "Lost in the Right Direction" (the HeyClicky / chat-apps pick).
     - Offset 0.28 s, so its drop lands on "So I showed him the prompt library" (47.52).
     - A record-scratch stop at 10.24, and back on the globe at 11.9.
     - Muffled under the window on black (35.8–37.3).
   - **SFX:** 86 cues from `chatly-chatapps/audio-ref/picks` and `mix/sfx`. Each matches the object on screen.
   - **Outro:** its own audio from 73.35.
6. **Mux:** `ffmpeg -i out/picture.mp4 -i out/audio.wav -c:v copy -c:a aac -b:a 256k -af apad -shortest`.

**Python:** `reels/chatly-chatapps/.venv/bin/python` (OpenCV) for compose.py and fix_assets.py.

## Timeline (output s = VO s)
| Time | Content |
| --- | --- |
| 0–3.6 | Hook live shots + word pops; FASEEH name sticker |
| 3.6–5.0 | Report card FAIL, "HIS JOB." |
| 5.0–12.0 | Meet call: "where's the 9am post??" card, "Is it 9am?", "in SAN FRANCISCO" sticker, facepalm with the bleep |
| 12.0–19.0 | Globe → NY! map (seg1923), then the London/SF circles and −8/−5/0 stickers (P-25) |
| 19.0–28.1 | Live: the FEEDER ACCOUNTS sign ("impossible task."), scroll, monitor, bean bag, typing |
| 28.1–34.0 | P-31 posts math |
| 34.0–35.8 | "What the hell?" with a punch-in |
| 35.8–37.3 | "He's not the only one" window |
| 37.3–39.3 | P-32 montage |
| 39.3–47.4 | Notes app → Google Doc → "let's just say… it doesn't scale." with the Upload failed popup |
| 47.4–62.5 | Blank prompt card → P-01 save → P-02 @hook → P-03 fill the blanks → P-04 Everyone at Chatly |
| 62.5–65.5 | Dance → PASS card, "ANYMORE." |
| 65.5–68.8 | Scroll ticks + "10 ACCOUNTS" / "OR 50" |
| 68.8–72.1 | CTA live, "PROMPTS" sticker |
| 72.1–73.35 | "a 💜 Chatly story" |
| 73.35–78.35 | Official outro: "AI that works 24/7 for you." |

## v2 (2026-11-22, after "no music, improve the artifacts")
**Output:** `out/this-is-faseeh-chatly-v2-4x3.mp4`

**Music:** the reference reel's own music.
- It was separated from its voice with Demucs (htdemucs two-stem) into `faseeh/edit/music/ref_music.wav` (not in git).
- It's spliced bar-aligned onto our structure: the 103 bpm cue and the 136 bpm cue, see `SEG` in audio.py.
  - intro, then silence on the Meet call
  - hits on the globe and map
  - the 103 bpm cue from the cut to "impossible task" (18.967), with one bar repeated, through "360 posts a week"
  - silence on "What the hell?"
  - the quiet 136 bpm intro under the problem section
  - the drop at 47.52 ("So I showed him…"), running into the outro
- It's mixed like the reference: the bed at −21 LUFS, about 5 LU under the VO, with a light sidechain. The record scratch was dropped.
- **Licence:** this is Lovable's ad audio, so it has to be cleared or replaced before publishing.

**Screens 37.3–62.5:** the reference's app-section treatment (`refscreen`, `screen`).
- Sage-cream whites (L85, a −11, b +15), lifted blacks and softness, matching the reference.
- Handheld drift, and eased punch-ins on the Doc, the library list, @hook and the reply.
- Paper stickers on the VO words (`SCR_STK`): REWRITE, 30x A DAY, ONE WORD, PROMPT LIBRARY, {{ BLANKS }}, ACCOUNT / NICHE / PLATFORM, SEND!, WHOLE TEAM.

## v3 (2026-11-23, "add gradient… soft cinematic colour like HeyClicky")
**Output:** `out/this-is-faseeh-chatly-v3-4x3.mp4`

- **One grade for the whole film:** `finish()` in compose.py runs on every frame except the official outro, before stickers and captions. It replaces the per-shot live grade and the v2 sage screen tint.
- **What `finish()` does:**
  - the HeyClicky Lab grade (the chat-apps grade.py LUTs) + lens bloom
  - blues and skies muted by 38%, overall saturation −6%
  - Pro-Mist diffusion at 14%
  - **the soft gradient:** warm amber light falling from the top left (screen-blended at 15%), a 10% shade toward the bottom, and a vignette
