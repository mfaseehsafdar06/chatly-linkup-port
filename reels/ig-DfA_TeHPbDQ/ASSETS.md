# ASSETS: production checklist for the Chatly port of IG DfA_TeHPbDQ ("a Chatly story")

Built 2026-11-22 from all 762 frames at 10 fps (`refs/sheets/s01–s39`), with full-size checks in `refs/f10/` and word timings from `refs/ref16.json`. Shot numbers follow REF.md. Output is 4:3, 1440×1080, 24 fps.

**Coordinates and timing:**
- All x/y values are in **1440×1080 output pixels** (reference 960×720 × 1.5). Treat them as approximate placement: the editor should still pair-check against the reference.
- `f` = frame at 24 fps (f = round(t × 24)).

**Nothing in this file has been generated or rendered.**

---

## 0. Two terms the owner used, and how this file reads them

- **"Chip box" style** means a word written on its own small piece of coloured paper (a "chip"), or a printed word with a crayon scribble box drawn round it. Examples:
  - Chips: **AT** (blue), **AMSTERDAM** (pink) + **TIME** (green), **THINK** (green), **GMT** (yellow) + **+8** (crimson), and the three **?** chips.
  - Scribble box: the box round **TUESDAY** that changes colour every frame.
  - Chips are paper art (gpt-image-2). The boxes and burst lines are line boil (HyperFrames).
- **Handwritten-style caption in shots 4–5** is the **LEO** name chip: purple wax crayon on bubblegum-pink paper, which pops on at 1.29 s.
  - The subtitle "And I'm trying to save" (2.0–3.7 s) is typeset bold sans, not handwriting, so it belongs to the subtitle system (HF-02).
  - LEO shares a look with the four app stickers (LOCATION, TIME, WORKING ON, PRIORITIES): crayon letters on coloured paper. That's why they are on one sheet (GPT-05).

---

## 1. Summary

| Method | Assets | Notes |
|---|---|---|
| **1. HyperFrames (code)** | **31** (HF-01 … HF-31) | 4 are shared systems (captions, subtitles, sticker motion, line boil); 27 are per-shot builds |
| **2. gpt-image-2** | **13 images** (GPT-01 … GPT-13) | 46 pieces of art grouped onto 13 sheets/plates (see grouping below) |
| **3. Live action / Seedance / stills (not ours today)** | **34 placeholder lines** | 32 shot plates/stills + 2 support plates (Ying PIP webcam, headshot pack) |
| **4. Done** | **1** (`seg1923/`) | Shots 17–19 plus the whip and full-map frames of 20, 19.17–23.42 s |

**Total gpt-image-2 images: 13.** If GPT-06 (the LinkUp logo) moves onto the crayon sheet GPT-05 and GPT-13 (chat stickers) is swapped for a plain 😭 emoji, the total drops to **11**.

### How the stickers are grouped onto sheets

| Sheet | Contents (count) | Why these go together |
|---|---|---|
| GPT-01 Chip sheet A | AT, AMSTERDAM, TIME (green), THINK, GMT, +8, 9PM (7) | Kinetic-type chips for shot 9. GMT, AMSTERDAM and +8 are reused on the map in shot 20 |
| GPT-02 Chip sheet B | SINGAPORE, NEW YORK, LONDON, UTC, +2, ? green, ? blue, ? pink (8) | Map pile-up chips (shot 20). The three ?s are used in shots 9 and 20 |
| GPT-03 Report card | 1 poster, with the photo window left blank | Bookend prop for shots 5–7 and 49–50 |
| GPT-04 Slap stickers | FAIL, PASS!, SETS MEETINGS INSTANTLY!! (3) | All slapped onto the report card |
| GPT-05 Crayon sheet | LEO, LOCATION, TIME (blue), WORKING ON, PRIORITIES (5) | Same wax-crayon-on-paper look |
| GPT-06 LinkUp logo | 2 smiley stars + "LiNKUP!" (1) | Felt-tip logo; needs its own render for quality |
| GPT-07 Poster base | MEETING TIME? painted globe, no cards (1) | High-res plate for the close-ups in shot 22 |
| GPT-08 Name cards | 5 cards + 2 ✓ chips + 2 ✗ chips (9) | Same card-on-black-stock look |
| GPT-09 Status signs | ANYTIME, MAYBE?, LEAVE ME ALONE! (3) | The hand-held signs (shots 44–46) |
| GPT-10 List poster | LIST OF CREATORS TO COORDINATE (1) | Seedance prop ref (shot 21) |
| GPT-11 Prop sheet | A BETTER WAY sketchbook + "WHAT." sign (2) | Seedance prop refs (shots 35 and 24) |
| GPT-12 Hand cutouts | Slap palm, pinch-place, edge grip (3) | All slaps and placements (6, 22, 49, 50, 44, 46) |
| GPT-13 Chat stickers | Original pink bear, 2 poses (2) | Replaces the copyrighted Loopy sticker (shots 30, 32) |

### Hidden competitor and real-name mentions to swap (every swap only changes branding)

| Where | Reference | Chatly port |
|---|---|---|
| End card (55) | "a ♥ Lovable story" | "a [Chatly mark] Chatly story" (kit `LogoWithText`, never retyped) → official outro + "AI that works 24/7 for you." |
| LinkUp header (40–42) | LOVABLE TEAM | CREATOR CREW |
| Calendar popover + event chip (48) | LOVABLE TEAM | CREATOR CREW |
| Calendar block (48) | "FINISH EDITING DRAFT FOR LOVABLE" | "FINISH EDITING DRAFT FOR CLIENT" |
| Safari tab on converter (34) | "Home \| Lovable" (Lovable heart favicon) | "Chatly" with the Chatly favicon |
| Chrome omnibox (36) | lovable.dev/projects/…, "lovable dev", "lovable script" | chatlyai.app, "Chatly - chatlyai.app", "chatly ai" |
| Lovable home (37–38) | "What should we build, Ying?", Build ⌄, pink-blue gradient | Real Chatly home V2 (kit `CU.homeV2`) with the ask typed into the composer |
| LinkUp URL bar (39) | creator-time-harmony.lovable.app | Chatly Sites URL. **The published Sites domain still needs confirming**; the builder path is `/sites/<id>` with a "Made with Chatly" badge |
| Meet title (55) | "3:29 PM \| Ying/Leo Lovable Shots" | "3:29 PM \| Ying/Leo catch-up" |
| Meet toolbar (8, 51, 55) | "✦ Ask Gemini · Only you" | Remove it, because it names a competitor AI. Leave the left of the toolbar blank or show the meeting title |
| Meet name labels | "Leonie Rasch", "Ying Xuan Ng" (real people) | New characters: "Leo" + a new surname, "Ying" + a new surname (user to pick). The same names apply in the LinkUp chips |
| Chat names (30) | "baby sean", "Yvonne Tai" | Fictional names (suggestion: "baby sam", "Mia T.") |
| Converter site (34) | "Savvy Time" (real site) | Fictional brand, e.g. "TimeHop" |
| Chat sticker (30, 32) | Zanmang Loopy (copyrighted) | GPT-13 original bear |

### Points for the user to decide (rule conflicts)

- House rules for Chatly (memory, 11-11/11-12) say **no blue type** and **no pink highlights** in captions and stickers. This is a near-verbatim port, and the reference's look depends on coloured paper chips (blue AT, blue ?, blue app TIME, pink AMSTERDAM, pink burst lines).
  - All the lettering is black or purple marker, so no *type* is blue, only the paper.
  - **This file assumes the reference palette.** Check with the user before building.
- **Shot 11** (13.50–13.75, over the shoulder onto a laptop) has no clip in PORT.md's Seedance list.
  - Cheapest fix: comp HF-08 onto a desk/laptop still, or hold shot 12's plate 6 frames longer.
- **Headshot photos** (Izy, Mullet/Max, Fin, Luke, Leo & Max duo, Ying with camcorder) are needed for the name cards and the LinkUp status cards. They are **not in PORT.md's still budget** (+6 stills, or one 2×3 contact-sheet gen).

---

## 2. HyperFrames (code) assets

Look notes that apply to every code build:
- Paper scenes get a stop-motion feel: content updates on 2s (12 fps), with ±1–2 px jitter.
- Screens get a filmed-screen feel: slight keystone, shallow depth-of-field falloff and a faint moiré. Optional.
- The film-wide grade (warm green cast, grain, vignette, fisheye on the Ying shots) is a post pass, not an asset.

### Shared systems

**HF-01 · Word-pop caption system (style W)**
- **Shots:** almost all; full cue list below.
- **Style:**
  - White #FFFFFF heavy grotesk (Inter Bold or Helvetica Neue Bold look) with a soft 2 px drop shadow at 35% black.
  - Lowercase as spoken, except "HER", "JOB.", "ONE", "TIME" and "ANYMORE.", which are caps.
  - Standard size about 64 px.
  - "only" (32.6 s) is **Bold Italic**.
  - Emphasis words are set apart by size, not colour: "impossible" 84, "friends" 96, "work out." 76 vs "it doesn't really" 52, "ANYMORE." 88.
- **Animation:**
  - Each word appears on its spoken frame. It's a hard cut-in, with an optional 2-frame scale 0.9→1.0.
  - Words build up into a scattered layout round the subject and all clear together on the next cut, unless the table below says otherwise.
  - The words carry across cuts in shots 1–3: same screen position, new plate behind.
- **Cue list** (t = in time, x,y = left/centre of the word in 1440×1080):

| t | Word(s) | Pos | Clears |
|---|---|---|---|
| 0.10 / 0.30 / 0.70 / 0.90 | This / is / my / friend | (345,608) / (480,425) / (945,240) / (1100,563) | 1.29 |
| 3.70 / 4.00 | HER / JOB. | (210,548) caps 75 px / (1190,548) | 4.75 |
| 4.80 / 5.00 / 5.30 / 5.40 | Ying / are / you / free | (270,342) / (375,482) / (920,595) / (1100,765) | 5.83 |
| 14.80 / 15.10 / 15.30 / 15.50 | Leo / has / an / almost | (270,567) / (495,330) / (1010,360) / (1050,670) | 16.00 |
| 16.00 / 16.60 | impossible / task | (430,792) 84 px / (1060,910) | 17.54 |
| 25.70–26.10 | the / list / goes / on… (stacked) | x≈1190, y 480 / 548 / 615 / 683 | 26.75 |
| 26.80 → 27.40 | SO→SOO→SOOO→SOOOO→SOOOOO→SOOOOOOOO→SOOOOOOOOO (grows 1 letter per ~0.1 s, small caps 40 px, top centre (720,190)) | | 27.50 |
| 27.90 / 28.40 | ONE / TIME (caps) | (270,257) / (1160,880) | 28.65 |
| 30.50 / 30.80 | hell / no. | (1190,418) / (1260,508) | 31.25 |
| 32.00 / 32.10 / 32.40 / 32.60 / 32.90 | she's / not / the / *only* / one. | (355,420) / (700,300) / (1035,532) / (420,765) italic / (1010,770) | "only" holds over the 33.3 photo, clears 33.40 |
| 35.30 / 35.60 / 35.90 / 36.00 / 36.20 | common / time / to / meet / up | (1100,193) / (1100,255) / (1100,322) / (297,414) / (297,486) | 37.54 |
| 38.60 / 38.90 / 39.10 | let's / just / say… | (220,342) / (285,445) / (383,571) | 39.92 |
| 39.90 / 40.50 | it doesn't really (52 px) / work out. (76 px) | left, (60–560, 428) / (60–560, 505) | 41.79 |
| 47.10 / 47.20 | for / good. (stacked) | (1197,500) / (1197,560) | 47.96 |
| 50.10 / 50.40 / 50.80 | where / everyone / is, | right of globe (1170,522) / (1150,580) / (1250,640) | 51.46 |
| 51.50 / 52.00 | what / it is for them, | (500,180) / (945–1340,190), with the TIME sticker between | 53.08 |
| 53.10 / 53.30 / 54.40 | what / they're / & | (290,887) / (545,887) / (1228,887), with WORKING ON between | 54.75 |
| 54.80 / 55.00 / 55.30 | based / on / their | (330,945) / (470,945) / (610,945), PRIORITIES after | 56.50 |
| 61.70 / 61.90 | maybe / next time… | top right (1180,158) / (1150,230) | 62.75 |
| 66.80 | ANYMORE. | caps 88 px, centred low (720,922) | 67.67 |
| 68.80 → 69.90 | just → just like → just like Leo, → just like Leo, OR | lower left, line grows from x≈200, y 810, 54 px | 70.25 |
| 70.30 / 70.50 / 70.60 / 70.70 / 70.90 / 71.00 | you / just / need / a / time / to | (180,545) / (1150,865) / (608,783) / (1206,693) / (1110,230) / (1143,440) | 71.30 |
| 71.40 / 71.40 / 71.50 | meet / your / friends | (880,738) / (1000,775) / (1080,868) 96 px | 72.42 |
| 73.00 / 73.50 | and I'll send / you the link! | right (1044–1372, 500) / (1044–1372, 560) | 74.85 |

- **Depends on:** nothing.
- **Note:** shot 17's "all over the world" is already in `seg1923`.

**HF-02 · Bottom subtitle system (style S)**
- **Style:** white bold sans (same family) about 42 px, centred at y≈1008, with a soft shadow. Hard on and off.
- **Cues:**

| t in–out | Text |
|---|---|
| 2.00–3.70 | And I'm trying to save |
| 14.50–14.75 | See, |
| 17.54–17.95 | She has to |
| 17.95–19.17 | coordinate creators from |
| 27.50–27.85 | finding |
| 28.70–29.25 | that works |
| 29.25–30.25 | for everyone? |
| 33.30–33.85 | Everytime |
| 33.85–34.55 | my friends and I |
| 34.58–35.30 | try to find a |
| 41.79–43.46 | So I knew |
| 44.46–45.30 | So I decided |
| 45.30–46.05 | to make something |
| 46.05–47.10 | that will solve this problem |
| 49.20–50.05 | An app that shows |
| 56.50–57.96 | they can set their status to |
| 62.75–63.25 | With Link Up |
| 63.25–64.30 | as her partner, |
| 64.30–65.05 | Leo doesn't have to |
| 65.05–66.00 | convert timezones |
| 66.00–66.75 | one by one, |
| 67.67–68.45 | Soooo |
| 68.45–68.75 | If you're |
| 72.42–73.00 | Comment "LINK UP" |

- **Depends on:** nothing.

**HF-03 · Sticker motion kit**
- **Moves:**
  - **pop:** 1-frame appear, scale 1.06→1.0 over 2 frames, ±2° random rotation fixed per sticker.
  - **slap:** a hand cutout enters with 2 frames of motion blur, presses for 2–3 frames (sticker 1.0, hand scale 0.98), then exits with 2 blur frames.
  - **slide-in:** from the frame edge over 3–4 frames with directional blur, then settles with a 2-frame overshoot.
  - **wipe-reveal:** a left→right mask.
  - **stop-motion jitter:** ±1–2 px and ±0.5° on 2s.
  - **drop shadow:** 0 2 px 3 px at 25% for paper on paper.
- **Depends on:** GPT-12 hands for slaps and grips; all sticker sheets once cut out.

**HF-04 · Line-boil crayon stroke kit**
- **What it does:** procedural rough strokes (wax-crayon texture brush, 8–12 px at 1440, ragged edges) that are redrawn every 2 frames with new noise seeds.
- **Primitives:**
  - rough rectangle box
  - radiating burst dashes
  - coil scribble (loop-de-loop)
  - small starburst
  - ring
- **Palette:** pink #E4338A, green #22D07A, cyan #34B8E8, plus orange #F2A23A, blue #5468E8 and red #E0263F for the shot-55 scribbles.
- **Depends on:** nothing.

### Per-shot builds

**HF-05 · LEO name chip pop** (shot 4, 1.29–2.08, f31–f50)
- **What it shows:** the GPT-05 "LEO" chip, about 380×170 px, at x 788–1170, y 698–923, rotated −2°.
- **Animation:** pops on at f31 on the punch-in, holds with stop-motion jitter, and carries 1 frame into shot 5's first frame (2.0 s still shows it).
- **Depends on:** GPT-05 LEO; LA L2 plate.

**HF-06 · Report card sequence A** (shots 5–7, 2.08–4.75, f50–f114)
- **Shot 5 (2.08–2.71):** a cut to the card scaled about 2.6× so the photo window (x 143–1298, y 128–1005) fills the frame.
  - The window holds a **still** frame of Leo from L2, printed look: slightly washed, matte, with a faint paper grain.
  - The teal border and black crayon frame show round the edges. Handheld drift is about 6 px over the shot.
- **Shot 6 (2.71–3.71):** reframed onto the card's top-left at about 3×. The "REPORTC…" crayon letters run across the top and the photo sits lower right.
  - **Slap at f79 (3.30):** the hand (GPT-12 pose a) brings in **FAIL** from the bottom-left. It is fully down by f84 and the hand is gone by f86.
  - FAIL ends up big, rotated −12°, at x 323–1155, y 162–870.
- **Shot 7 (3.71–4.75):** the full card, static, centred at x 413–990, y 162–1017, on a pale sage background (#CAD6BA).
  - FAIL sits small over the photo's top-left corner.
  - Comment strip: "TAKES TOO LONG / TO FIND A MEETING TIME".
  - Word pops "HER" and "JOB." are from HF-01.
- **Depends on:** GPT-03, GPT-04 FAIL, GPT-12, HF-01, HF-02, HF-03; LA L2 still.

**HF-07 · Google Meet chrome component** (reused in 8, 12, 51, 54, 55)
- **Toolbar:** dark #202124 bar. The left text is removed (see the swap table). Centre controls, in order: ⋯, mic, ^, camera, present, emoji (active = pale blue-grey #C9D6EA rounded square), CC, ✋, ⋮, then the red hang-up pill #DC362E. Right: chat and apps icons.
- **Reaction row** above the toolbar: 💖 👍 🎉 👏 😂 😮 😢 🤔 👎 ➕ (Noto/Google emoji).
- **Tiles:** rounded speaker tile (r 15), name label bottom-left (white, 18 px, plate shadow), blue "speaking" bars top-right, self-view PIP (r 10) with its own small name label.
- **Depends on:** nothing, though the plates come from LA.

**HF-08 · Meet speaker view on black** (shot 8, 4.75–5.83, f114–f140)
- **Layout:** black surround. Meet window x 98–1358, y 207–840. Leo's webcam fills the tile.
- **Labels:** name label "Leo [surname]" at (117,818). The PIP with Ying's webcam is at x 1143–1340, y 717–827. The toolbar row sits at y≈877.
- **Captions:** word pops "Ying / are / you / free".
- **Depends on:** HF-07, HF-01; LA L3 plate; Ying PIP plate.

**HF-09 · Kinetic paper type** (shot 9, 5.83–11.13, f140–f267)
- **Background:** off-white paper #FBFBF9 with sparse grey dust specks and a faint crease. The speck pattern changes on every "new card" (each word change), as if each word were photographed separately.
- **Printed words:** heavy grotesk caps (Helvetica Neue Heavy / Arial Black look), colour #3B3B3B, a slight print softness, and the faint edge of a cut paper strip round each word.
- **Timeline:**
  - **5.83 (f140):** "TUESDAY" (cap height ~97 px) at x 135–728, y 495–593, inside a **crayon scribble box** (HF-04) at x 117–759, y 435–645. The box redraws every 2 frames, cycling pink → green → cyan without repeating a colour, with ±4 px corner wobble.
  - **6.20 (f149):** "EVENING" at x 765–1336, same baseline. The box stays round TUESDAY only.
  - **6.80 (f163):** a hard cut to a clean card with only the blue **AT** chip, at x 194–368, y 214–390.
  - **7.00 (f168):** big black brush **9PM** with a hand-drawn underline appears: letters x 293–1200, y 315–780; underline x 300–1200, y 780–870. AT stays at its top-left.
  - **7.50 (f180):** cut to the pink **AMSTERDAM** chip, x 249–1149, y 390–638.
  - **7.90 (f190):** green **TIME** chip pops below-right, x 545–897, y 593–788, rotated −2°, overlapping AMSTERDAM's lower edge.
  - **8.20 (f197):** cut to "WHICH" (cap ~70 px, smaller than TUESDAY) at x 135–435, y 488–563.
  - **8.30:** "I" at x 488–510.
  - **8.50 (f204):** green **THINK** chip, x 570–1107, y 398–642.
  - **8.60:** "IS" at x 1155–1238.
  - **8.90 (f214):** cut to the yellow **GMT** chip, x 222–822, y 368–693.
  - **9.50–9.70 (f228–f233):** the crimson **+8** chip wipe-reveals left→right from x 870 to 1190 (y 398–687). At 9.5 only "+" shows; by 9.7 "+8" is complete.
  - **10.10 (f242):** cut to "IN" at x 285–368, y 488–555.
  - **10.30:** "YOUR" at x 450–675.
  - **10.50 (f252):** "TIMEZONE" at x 765–1193, plus pink **burst dashes** (HF-04) round it: about 8 dashes above, 8 below and 2–3 at each end, within x 705–1230, y 405–660, boiling on 2s.
  - **10.80 (f259):** green **?** (x 327–582, y 405–780, rotated −5°) and blue **?** (x 578–815, y 330–743, upright) slap on together.
  - **10.90 (f262):** pink **?** (x 815–1122, y 383–795, rotated +8°) slaps on.
  - **11.13–11.20:** the blue and pink ?s carry over the first 2 frames of shot 10, a deliberate overlap cut.
- **Depends on:** GPT-01 (AT, 9PM, AMSTERDAM, TIME, THINK, GMT, +8), GPT-02 (? ×3), HF-03, HF-04.

**HF-10 · Ying spotlight tile + "UmMMmMmm" + "its" + "3AM"** (shot 10, 11.13–13.50, f267–f324)
- **Tile:** Meet spotlight tile x 60–1403, y 128–885, radius 36, with a 7 px lavender border #A9B9F3. Name "Ying [surname]" at (113,795), white 48 px with a shadow. The surround is a dark blurred enlargement of the plate (#1E1E1E–#3A3A3A).
- **"UmMMmMmm"** (verbatim final spelling): white heavy grotesk about 115 px, centred at x 720, baseline y 330. It grows one letter at a time and stays centred:
  - 11.13 "Um"
  - 11.30 "UmMM"
  - 11.40 "UmMMm"
  - 11.50 "UmMMmM"
  - 11.60 "UmMMmMm"
  - 11.70 "UmMMmMmm"
  - clears 11.80
- **"its":** 50 px at (155,180) from 11.80, held to the end.
- **"3AM":** giant white heavy grotesk (cap ~465 px) at x 87–1347, y 225–690, appearing at **12.60 (f302)**. It sits **behind Ying's head**: her face covers the "A". That needs a per-frame person matte from the Y1 clip (SAM/rembg).
- **Depends on:** HF-07; LA Y1 plate and matte; HF-09's ? carry-over.

**HF-11 · "Hard drive error" dialog (Win98/XP style)** (shot 12, 13.75–14.75; pops at **14.08, f338**)
- **Position:** dialog at x 455–993, y 380–750.
- **Title bar:** 60 px tall, blue gradient #2A5BD7→#3D7BEA, "Error" in white Tahoma about 33 px. A grey square close button with ✕ sits at x 925–970.
- **Body:** cream #ECE9D8. Red circle icon with a white ✕ (r 30) centred at (540,520). "Hard drive error" in black Tahoma 27 px at x 618, y 505. **OK** button at x 550–718, y 597–663, with a 3 px black border and "OK" 27 px.
- **Animation:** hard pop-on, no fade. It holds static to the cut, with optional ±1 px jitter on 2s. The webcam plate's own shake carries the energy.
- **Rest of the shot:** Leo's webcam fills the frame. Ying's PIP is bottom-right at x 1143–1440, y 870–1080 (rounded). Subtitle "See," from HF-02.
- **Depends on:** HF-07 (PIP); LA L3 plate.

**HF-12 · Map sticker pile-up** (shot 20 remainder, 23.42–25.42, f562–f610)
- **Background:** the last frame of `seg1923/out/seg1923-final-4x3.mp4` (full world map with the red circles and NY!), held with about 4 px of handheld drift.
- **Chips** pop on with 1-frame appear + 2-frame settle, no hand, in this order (final positions and rotations):

| t | Chip | Position | Rotation |
|---|---|---|---|
| 23.40 | yellow **GMT** | x 365–642, y 413–660 | −12° |
| 23.70 | green **UTC** | x 787–1057, y 540–810 | +35° |
| 23.80 | pink **AMSTERDAM** | x 473–990, y 518–690, over GMT | −4° |
| 24.00 | green **+2** | x 923–1133, y 578–750 | −3° |
| 24.30 | crimson **+8** | x 270–450, y 585–780 | −25° |
| 24.40 | red **SINGAPORE** | x 540–1050, y 338–525 | −3° |
| 24.70 | green **NEW YORK** | x 398–975, y 615–840 | +6° |
| 24.90 | teal-blue **LONDON** | x 308–705, y 248–480 | −12° |
| 25.00 | blue **?** | x 845–1092, y 600–900 | +20° |
| 25.10 | pink **?** | x 207–402, y 330–623 | −3° |
| 25.20 | green **?** | x 605–837, y 383–675 | +25° |

- **Depends on:** seg1923 (done), GPT-01 (GMT, AMSTERDAM, +8), GPT-02, HF-03.

**HF-13 · MEETING TIME? poster, stop-motion** (shots 22–23, 27.50–30.25, f660–f726)
- **Shot 22 (27.50–29.13), top-down close-ups at about 2.5× with handheld drift:**
  - **27.50:** a 2-frame zoom/motion-blur arrival onto the red **IZY** card.
  - **27.90–28.20:** a hand (GPT-12 pose b) comes in from the right and places a green ✓ chip in IZY's tick slot; the ✓ is visible at 28.20.
  - **28.30:** cut to the yellow **MULLET** card (top right, under the "…ME?" letters). The hand places a red ✗, visible at 28.50.
  - **28.70:** cut to the pink **FIN** card (lower right) with ✓ already placed; the hand exits right over 28.70–28.85.
  - Word pops "ONE" and "TIME"; subtitles "finding" and "that works".
- **Shot 23 (29.13–30.25), the wide poster:**
  - Title arc spans x 255–1200, y 165–465. Globe x 330–1110, y 450–1080, cropped at the bottom.
  - Cards:
    - **LEO** CEST(UTC+2), green: x 195–525, y 390–600
    - **MULLET** BST(UTC+1), yellow: x 930–1275, y 375–555
    - **IZY** MDT(UTC-6), red: x 607–900, y 645–855
    - **LUKE** EDT(UTC-4), blue: x 255–555, y 855–1050
    - **FIN** AEST(UTC+10), pink: x 960–1335, y 840–1050
  - **Tick flicker:** each card's chip swaps between ✓ and ✗ at random every 2–3 frames, and never shows all ✓ at once. End state at 30.0: LEO ✗, MULLET ✓, IZY ✗, LUKE ✓, FIN ✗.
  - The whole poster has stop-motion jitter on 2s. Subtitle "for everyone?".
- **Depends on:** GPT-07, GPT-08, GPT-12; headshot stills composited into the cards' photo slots; HF-01, HF-02, HF-03.

**HF-14 · Black photo-window trick** (shots 26–27, 32.00–34.00; shot 52, 70.33–71.54)
- **Shot 26 (32.00–33.10):** pure black. A window at x 518–935, y 390–702 plays Leo's kitchen clip (the same plate as shot 25). Word pops surround it.
  - **33.10:** the window content hard-swaps to an old group photo in a smaller window, x 437–999, y 347–729.
- **Shot 27, photo flashes on black:**
  - 33.30: school group photo at x 315–1125, y 257–824, with subtitle "Everytime"
  - 33.50: two-girls photo, x 248–1193, y 225–855
  - 33.60: light-leak photo, x 171–1269, y 180–900
  - 33.80: night photo, x 180–1260, y 158–914
  - The cut to the mall is at 34.00.
- **Shot 52 (stepped growth, not a smooth scale):**
  - 70.33: a tiny window, x 633–819, y 480–605
  - 70.50: x 301–819, y 225–585
  - 70.70: x 293–1089, y 59–599
  - 70.80: x 248–1440, y 59–932
  - 71.00: full frame
  - Words follow the HF-01 cues.
- **Depends on:** HF-01, HF-02; LA L5 plate; 6 friend stills.

**HF-15 · Phone group chat (WhatsApp-style)** (shot 30, 36.00–37.54; shot 32, 38.25–39.92)
- **Look:** phone screen close-up filling the frame at a slight angle. A thumb enters from the right (cutout taken from the Y4 plate, or GPT-12). The phone edge shows at the right.
  - A diagonal **iridescent rainbow light leak** sweeps across the glass in 30a.
  - A thin **screen crack** line runs diagonally in 30b.
  - Wallpaper: sunset sky (orange/amber), with a black city-skyline silhouette in shot 32.
- **Screen 30a (36.00–36.45):**
  - Sticker top right (GPT-13 pose 1) with "1:23 PM ✓✓"
  - "Today" pill
  - Outgoing light-green bubble **"GUYS CAN WE MEET UP PLSPLSPLS"**, "4:02 PM" with a pending clock icon
  - Composer: "+", text field, sticker icon
  - Keyboard: suggestion bar "THE / I'M" and caps QWERTY row
- **Screen 30b (36.50–37.54):**
  - Top "1:20 PM ✓✓"
  - Incoming white bubble, sender "baby sean" (→ swap): **"I HAVE TUITION THIS WEEEK 💩💩"**, then two rows of emoji: 🥀🥀🤑😭😂😍👀💁‍♀️💁‍♀️💁‍♀️🧑‍⚕️🙏 / 😏👍👽💋😈🤑👍💔👽🤑💋😏🙏, "1:22 PM", grey "B" avatar
  - **36.80:** a typing "•••" bubble appears
  - **37.10:** incoming "Yvonne Tai" (→ swap): **"Can't make it this week"** "1:22 PM", with a small avatar
  - Composer: + / field / sticker / camera / mic
- **Screen 32 (38.25–39.92):** outgoing **"NEXT WEEK????"** (4 ?) "1:23 PM ✓✓", **"HELOOOOOOO"** (HEL + 7 O's, checked at full size) "1:23 PM ✓✓", sad-bear sticker (GPT-13 pose 2) "1:23 PM ✓✓", grey forward-arrow circle.
- **Animation:** the bubbles cut on (no slide). Slight handheld float on the whole phone.
- **Rule:** memory says on-camera screens should be rendered by Seedance from a real UI ref. Here the screen fills the frame, so a direct HF render plus a thumb comp is fine.
- **Depends on:** GPT-13; emoji font; HF-01.

**HF-16 · Time-converter website** (shot 34, 41.79–43.50)
- **Chrome:** Safari, tab title "Chatly" with the Chatly favicon (swap). Site logo: a fictional brand with a multicolour ring clock, replacing "Savvy Time".
- **41.79:** tight on the search field (about 2.2×). Fragment "…gapore Time Conv…" across the top; tabs "Converter | Singapore, Singapore"; search typing "AMSTERD" → "AMSTERDA" (41.9) → "AMSTERDAM" (42.0) with a caret; below, "Singapore / Singapore | SGT".
- **Page cuts** (a wider page each time):
  - 42.10: "Singapore to Amsterdam Time Converter", "Best time: 3:00 pm – 6:00 pm  Mon, Oct 19 · Works for both places"
  - 42.20: "Singapore to London Time Converter", "Best time: 4:00 pm – 6:00 pm  Mon, Oct 19 · Works for both places"
  - 42.40: "Singapore to New York City Time Converter", "Best time: 7:00 pm – 8:00 pm  Mon, Oct 19 · No shared working hours · 2h late"
  - Each page has a breadcrumb "Home / Converter / …", tabs "Converter · Time Difference · Table · …", a field "Add time zone, city, or town" and a date "Oct 18, 2026".
- **42.60–42.90:** a blurred push onto the controls.
- **43.00–43.45:** tight on the time card.
  - Buttons "↻ Now" (blue #2F6FA8 filled), "✎ Edit", "More ⌄".
  - The time reads "8:00 pm" → 8:30 pm (43.1) → 10:15 pm (43.2) → 11:00 pm (43.3) → 11:30 pm (43.4), under it "UTC+8 | Sun, Oct 18".
  - Slider: sand→steel-blue gradient track, white knob dragged right by a hand cursor; tick labels "6pm" "9pm"; × at top right.
- **Overall:** light page, pale grey-green cast from the grade, subtitle "So I knew".
- **Depends on:** HF-02.

**HF-17 · Chrome omnibox typing chatlyai.app** (shot 36, 44.46–45.29)
- **Menu bar:** black macOS bar: " Chrome File Edit View History Bookmarks Profiles Tab Wi…".
- **Tab strip:** traffic lights, ⌄, tab "New Tab ×", "+".
- **Omnibox:** Chatly favicon, with the autocomplete-highlighted **"chatlyai.app"**. Typed text steps every ~0.15 s: "c" → "ch" → "cha" → "chat" → "chatl" → "chatly".
- **Dropdown rows:**
  - selected (blue left bar): "Chatly - chatlyai.app"
  - "chat… - Google Search"
  - history: "chatly ai", "chatlyai.app"
- **Filming look:** the top 20% of the frame is red/green bokeh (out-of-focus room); slight angle; pointer cursor near the URL.
- **Depends on:** HF-02; Chatly favicon (`assets/logos/`).

**HF-18 · Chatly home: the ask** (shot 38, 46.13–47.96; plus a still for shot 37 / Y5)
- **Shot 38:** screen close-up of the real Chatly home V2, built with the kit `CU.homeV2` in `reference/chatly-ui-kit/`. V2 has **no greeting**, so the Lovable "What should we build, Ying?" headline is not recreated. Show the Chatly logo/carousel edge instead.
  - **46.13–46.60:** tight on the composer while the ask is typed: "l" → "le" → "lets" → "lets b" → "lets bu" …
  - **46.70–47.10:** wider. The line scrolls: "…a tool that can generate meeting tim" → "meeting times" → "meeting times ins".
  - Suggested full ask (near-verbatim): **"lets build a tool that can generate meeting times instantly for my friends in different time zones"**.
  - **47.20–47.90:** pan to the composer's bottom right: mic + black ↑ send. The cursor arrives and clicks send at **47.50 (f1140)**.
  - Camera: rotateY about 8°, slow push, depth-of-field falloff.
  - Captions: subtitle "that will solve this problem", word pops "for / good.".
- **Still for Y5 (shot 37):** a 16:10 PNG of the home V2 with an empty composer, to use as Seedance's in-camera screen ref.
- **Depends on:** Chatly UI kit; HF-01, HF-02.

**HF-19 · LinkUp login inside the Chatly Sites pane** (UI ref still for shot 39 / Y6; it can also be cut in directly)
- **Pane:** the Chatly Sites builder preview (path "/", "Made with Chatly" badge, per memory `chatly-ui-facts`).
- **LinkUp page:**
  - cream #F4EFE2 background with soft white clouds
  - header strip "— LINK UP! — get set up in a minute"
  - centred GPT-06 logo, with a short pink dash under it
  - card "What's your name?" in a handwritten font (Gaegu / Patrick Hand look)
  - input with placeholder "e.g. Ying"
  - pink pill button "Next" (#E88AA0)
- **Depends on:** GPT-06; Chatly UI kit.

**HF-20 · LinkUp globe view "CREATOR CREW"** (shot 40, 49.50–51.46)
- **Header:** "CREATOR CREW" (was LOVABLE TEAM), hand-drawn spaced caps (Gaegu Bold / Patrick Hand SC look), ink #2B2B2B, top centre.
- **Chip row** (pill chips, Nunito-style 500):
  - "● Ying [surname] 1:33 PM · Singapore" (green dot)
  - "● Fin 3:33 PM · Brisbane" (yellow)
  - "● Izy 11:33 PM · Edmonton" (red)
  - "● Leo and Max 7:33 AM · Zurich" (red)
  - second row: "● Luke 1:33 AM · New York" (yellow)
- **Globe:** orthographic 3D globe (d3-geo or three.js), teal ocean #5FA7B5 with a fine dot grid, mint land #8FE3A7, rotating slowly east.
  - Coloured pins: red #C8102E, yellow #D4A83A, green #3DBE5A.
  - Mini status cards float above the pins (Izy "Late for class in Uni"; Luke "Couch surfing for the m…" with photo; Leo and Max "Frolicking in the Swiss …" with photo).
  - A red-and-white cartoon **plane** (SVG) crosses South America → North America.
- **Controls:** right side, pink locate button #E86FA0 + "+", "−", ⊙. The cursor clicks locate at about 49.6.
- **Legend** at the bottom: "● leave me alone!  ● maybe?  ● always available".
- **Sticker:** **LOCATION** pops at **50.10** to the left of the globe, x 112–473, y 518–615.
- **Captions:** word pops "where / everyone / is,".
- **Depends on:** GPT-05 LOCATION; headshot stills; HF-01, HF-03.

**HF-21 · LinkUp time cards** (shot 41, 51.46–53.08)
- **Layout:** small top-left logo "LINK" (grey) + "UP!" (pink); subline "60 min · 7-day window · 5 people"; big "CREATOR CREW" in the handwritten caps.
- **Time cards** (white rounded cards, handwritten numerals):
  - "Ying [surname] 1:36 PM Singapore"
  - "Fin 3:36 PM Brisbane"
  - "Izy 11:36 PM ↺ Edmonton"
  - "Leo and Max 7:36 AM ↺ Zurich"
  - "Luke 1:36 AM ↺ New York"
- Below: "where everyone is" (handwritten), with the globe peeking in bottom right.
- **Camera:** an angled screen with a focus pull from blurred to sharp by 52.3, and drift.
- **Sticker:** blue **TIME** pops at **51.80**, x 690–900, y 158–228.
- **Captions:** "what" and "it is for them,".
- **Depends on:** GPT-05 TIME; HF-01.

**HF-22 · LinkUp status cards on the globe** (shot 42, 53.08–56.50)
- **Setup:** globe close-up with the chip row (now "1:31 PM…"). A hand cursor hovers each pin and a card pops (cream card, r 18, soft shadow; name + time + city, status line, photo):

| t | Card | Status line | Photo |
|---|---|---|---|
| 53.60 | **Leo and Max** · 7:31 AM · Zurich | "Frolicking in the Swiss Alps" | duo selfie |
| 54.20 | **Izy** · 11:31 PM · Edmonton | "Late for class in Uni" | large b&w photobooth portrait |
| 54.80 | **Luke** · 1:31 AM · New York | "Couch surfing for the month" | man in a NY cap at a dinner table |
| 55.40 | **Ying [surname]** · 1:32 PM · Singapore (green dot) | "Working on the next banger" | girl with a camcorder |
| 56.00 | **Fin** · 3:32 PM · Brisbane | "Being the next ice cream delivery man" | guy in a cap, tongue out |

- The globe rotates between pins.
- **Stickers:** red **WORKING ON** pops at **53.40**, x 698–1170, y 855–920. Pink **PRIORITIES** pops at **55.40**, x 833–1148, y 905–985.
- **Captions:** "what they're … &", "based on their".
- **Depends on:** GPT-05; headshot stills; HF-01.

**HF-23 · LinkUp priority picker** (shot 43, 56.50–57.96)
- **Settings panel:**
  - top: bottom edge of the photo + "🗑 Remove"
  - "What I'm working on" with input "Working on the next banger"
  - **Priority** with three option cards: "● Green (always available)", "● Yellow (maybe?)", "● Red (leave me alone!)"
  - "Time zone" with "Search — try Canada, Calgary, Switzerland…" and a select "Asia/Singapore ⌃⌄"
  - "Available from 8:00 ⌃ / until 22:00 ⌃"
  - pink double line down the right edge
- **Animation:** Green is selected at start (pink outline #D9708E). The cursor moves and clicks **Yellow** at **57.00**; the selection jumps to Yellow. The cursor then drifts toward Red by 57.9.
- **Captions:** subtitle "they can set their status to".
- **Depends on:** HF-02.

**HF-24 · Status-sign slide-ins over live plates** (shots 44–46, 57.96–62.75)
- **ANYTIME (shot 44):** slides in from the left edge at 57.96–58.30 with blur, held by a hand gripping its left end (GPT-12 pose c). Settles at x 68–585, y 270–428 with a ±4 px bob.
- **MAYBE? (shot 45):** rises in from the bottom left at 60.20–60.40 with blur and settles at x 99–675, y 675–900. In the reference it is held at both ends.
- **LEAVE ME ALONE! (shot 46):** swings in from the top left at 61.60–61.70 and settles rotated −8° at x 158–675, y 158–518. The arm enters from the left edge; fisheye warp matches the plate.
- **Note:** if Seedance renders the signs in-camera from the GPT-09 refs (plan Y7) and the text holds up, skip this. Keep it as the fallback for garbled lettering.
- **Depends on:** GPT-09, GPT-12, HF-03; LA Y7 plates.

**HF-25 · LinkUp "Find Best Time"** (shot 47, 62.75–63.63)
- **Layout:** partial view of the page. Text fragments "…ays available / …e everyone at once", a "~~" squiggle doodle, a dark plum rounded bar #2B1430, and inside it the pink pill **"✨ Find Best Time"** (#D9708E with a darker pink bottom shadow). Below: outlined pill "Done marking". Top: ⊙ and ⛶ icon buttons.
- **Animation:** the hand cursor clicks at **62.90 (f1510)** and the button depresses 2 px for 3 frames. Angled screen with focus drift.
- **Captions:** subtitles "With Link Up" and "as her partner,".
- **Depends on:** HF-02.

**HF-26 · Calendar event "Scheduled with LINK UP!"** (shot 48, 63.63–64.46)
- **Week view:** Google-Calendar-style grid of colourful blocks, for example:
  - "[TUT] CC0016 HEALTH & WELLBEING 12:30 – 2:30pm"
  - "[TUT] DD1101 PRESENTATION!!! 1:30 – 4:30pm"
  - "GO TO CENTRAL TO WORK 1 – 6:45pm"
  - "WORK AT …", "gem fair"
  - "BUILD WEBSITE CONTINUE 3:45 – 5pm"
  - "FINISH EDITING DRAFT FOR CLIENT 7:30 – 10pm"
  - "VAL FILM 7:30 – 9:30pm", "NG 8 – 10"
  - "DD1102 PRE…", "JIAK KENTA…"
  - a purple "CREATOR CREW 9 – 10pm" chip
- **Popover:**
  - "■ CREATOR CREW"
  - "Friday, 23 October · 9:00 – 10:00pm" (correct for 2026)
  - "< Invite via link" button
  - "≡ Scheduled with LINK UP!"
  - "🔔 30 minutes before"
  - "📅 DD1100"
  - toolbar ✎ 🗑 ✉ ⋮ and a ⊗ close with tooltip "Close"
- **Animation:** the popover slides up 20 px and settles over 3 frames, with a slight push-in.
- **Captions:** subtitle "as her partner,".
- **Depends on:** HF-02.

**HF-27 · Report card sequence B** (shots 49–50, 64.46–67.67)
- **Shot 49 (64.46–66.04):** close on the card's top left, with FAIL tilted about −40° over the photo corner.
  - A hand comes in from the bottom left at 64.90 carrying green **PASS!**. It presses 65.00–65.10 and is gone by 65.25.
  - PASS! settles rotated −10° at x 488–1005, y 398–773, with red corners of FAIL peeking out from under it.
- **Shot 50 (66.04–67.67):** close on the lower card: "comments:" + the red strip.
  - A hand slaps the green **SETS MEETINGS / INSTANTLY!!** strip at 66.10 (blur), presses 66.20–66.30 and exits at 66.40. The strip covers most of the red one, but red edges and the letters "T…" and "…E." stay visible.
  - Word pop "ANYMORE." at 66.80.
- **Captions:** subtitles "Leo doesn't have to", "convert timezones", "one by one,".
- **Depends on:** GPT-03, GPT-04, GPT-12, HF-01, HF-02, HF-03.

**HF-28 · Meet dance view + rising emoji reactions** (shot 51, 67.67–70.33)
- **Layout:** full-screen Meet speaker view with Leo's plate filling it, the HF-07 toolbar along the bottom and the reaction row above it.
- **Reactions:** emoji bubbles (mostly 🎉, some 💖 and 👍) with small "You" pills rise from the bottom-left edge to the top left over about 2 s each, 4–8 at a time, with gentle sway.
- **Captions:** subtitles "Soooo" and "If you're", then the lower-left growing line "just like Leo, OR".
- **Depends on:** HF-07, HF-01, HF-02; LA L4 plate.

**HF-29 · Meet reaction bar macro** (shot 54, 72.42–73.00)
- **Framing:** extreme close-up (about 3×). The reaction row 💖 👍 🎉 👏 😂 😮 😢 🤔 runs across the middle. Below it: ⋯, mic (dark circle), ^, camera, present, and the highlighted emoji button (pale blue-grey square).
- **Top:** Leo's chin and lips, heavily blurred (from the L4 plate).
- **Animation:** the hand cursor clicks 🎉 at **72.50 (f1740)**. The whole frame drifts left about 30 px over the shot.
- **Captions:** subtitle 'Comment "LINK UP"'.
- **Depends on:** HF-07, HF-02; LA L4 frame.

**HF-30 · Meet on a laptop + emoji confetti + scribble loops** (shot 55, 73.00–74.90)
- **Laptop view:**
  - Safari chrome (sidebar, ‹ ›, "meet.google.com", red recording icon)
  - Meet header "3:29 PM | Ying/Leo catch-up ⓘ"
  - Leo's tile, Ying PIP bottom right, toolbar + reaction row
  - slight keystone
- **Confetti:** 🎉 burst from **73.00 (f1752)**. About 60 tiny multicolour emoji/confetti particles (8–14 px) drift up and to the right from the bottom left.
- **Scribble loops** (HF-04, each draws on over 2–3 frames, then boils on 2s):
  - blue coil from 73.40
  - orange/yellow coils 73.50–73.90 (left of the face)
  - red coil 73.90–74.20
  - red ring round the mouth 74.30–74.45
  - small red/orange starbursts 74.60–74.80
  - all clear at 74.90
- **Captions:** word pops "and I'll send / you the link!".
- **Depends on:** HF-04, HF-07, HF-01; LA L4 plate; Ying PIP plate.

**HF-31 · End card + 4:3 Chatly outro** (74.90–76.17, then the outro)
- **74.90 (f1798):** centred over the still-playing Meet view at y≈545: "a" (white bold, about 60 px) + **[Chatly mark + wordmark]** from the kit's `LogoWithText` (white, about 105 px cap; never type "Chatly" in another font).
- **75.30 (f1807):** "story" (about 60 px) is added on the right.
- Hold to 76.17 (f1828).
- **Outro:** cut to the official outro adapted to 4:3.
  - Source: `Chatly Updated Outro/[16-9] Chatly Outro + CTA.mp4`.
  - Remove the tagline with delogo (16:9 box x800 y632 w322 h72), centre-crop to 1440×1080, then overlay **"AI that works 24/7 for you."** in Google Sans 500, 46 px (scaled), white, fading in at +0.98 s.
  - VO: "Chatly. AI that works twenty-four seven for you."
- **Depends on:** `assets/logos/chatly-mark-white.png` or the kit SVG; the outro mp4.

---

## 3. gpt-image-2 assets

**Shared prompt rules:**
- Sticker sheets: "top-down flat scan, even soft daylight, no cast shadows, items spaced apart on a plain flat light-grey #D9D9D9 background".
- Set `background: transparent` if the endpoint supports it; otherwise cut out with background removal.
- Ask for the **exact spelling in quotes**.
- Check every letter at full size before cutting out. Re-roll any sheet with a misspelling rather than fixing it in post.

Paper colours seen in the reference:

| Paper | Hex |
|---|---|
| blue | #1EA7E1 |
| bubblegum pink | #F4A6D7 |
| emerald-mint green | #22CC7F |
| pale lemon | #F8F19E |
| crimson | #C8102E |
| red | #E01E37 |
| teal-blue | #3E9FC0 |

Marker: black chisel-tip paint marker, condensed hand-lettered caps, uneven stroke weight.

**GPT-01 · Chip sheet A: kinetic type** (shots 9 and 20)
- **Items:**
  - "AT" on blue
  - "AMSTERDAM" on pink (a darker pink smudge near the left edge, as in the reference)
  - "TIME" on green
  - "THINK" on green
  - "GMT" on pale lemon
  - "+8" on crimson (needs to read as two glyphs for the wipe reveal)
  - "9PM" as huge black brush-marker letters with a thick hand-drawn underline, **directly on white paper with no chip**
- **Format:** transparent cutouts. The 9PM letters are cut out as ink only.
- **Prompt:**
  > A flat top-down scan of seven hand-made paper word stickers laid out separately on a plain light grey background. Each is a rectangle of matte coloured construction paper, hand-cut with scissors (slightly uneven straight edges), with bold condensed hand-lettered capitals in thick black chisel-tip paint marker, slightly irregular, like a zine collage. Exact words and paper colours: "AT" on bright sky-blue paper; "AMSTERDAM" on bubblegum-pink paper; "TIME" on emerald-mint green paper; "THINK" on emerald-mint green paper; "GMT" on pale lemon-yellow paper; "+8" on deep crimson paper; and separately "9PM" written very large in black brush marker directly on white paper with a thick wobbly hand-drawn underline beneath it. No other text, no shadows, even lighting, high resolution, every letter crisp and correctly spelled.

**GPT-02 · Chip sheet B: map cities + question marks** (shots 20 and 9)
- **Items:**
  - "SINGAPORE" on red
  - "NEW YORK" on green
  - "LONDON" on teal-blue
  - "UTC" on green
  - "+2" on green
  - three tall "?" chips: one green, one blue, one pink. The ?s are fat brush-marker question marks with a blobby dot.
- **Format:** transparent.
- **Prompt:**
  > A flat top-down scan of eight hand-made paper stickers spaced apart on a plain light grey background, hand-cut construction paper with bold condensed hand-lettered capitals in thick black chisel-tip paint marker, zine-collage style. Exact items: "SINGAPORE" on bright red paper; "NEW YORK" on emerald-mint green paper; "LONDON" on teal-blue paper; "UTC" on emerald-mint green paper; "+2" on emerald-mint green paper; and three tall upright rectangles each with one huge fat black brush-marker question mark with a blobby dot: one on emerald-mint green paper, one on bright sky-blue paper, one on bubblegum-pink paper. No shadows, even light, crisp, correctly spelled.

**GPT-03 · REPORT CARD poster, photo window left blank** (shots 5–7 and 49–50)
- **Look:**
  - portrait rounded-rectangle card of teal construction paper (#3E9DB0)
  - thick black **wax-crayon** outline round the card
  - "REPORTCARD" in tall squeezed black crayon caps across the top, written as one run with no space
  - a large photo window below it, framed by a thick black crayon rectangle, filled **flat mid-grey #808080** for compositing
  - "comments:" in lowercase black crayon handwriting
  - a red paper strip (#D7263D) glued across the lower third with black marker caps "TAKES TOO LONG" (underline under "TOO LONG") / "TO FIND A MEETING TIME"
  - **No FAIL sticker.**
- **Format:** flat scan on plain pale sage paper (#E3EADB). Generate at the largest size available (1024×1536, then upscale 2×), because shot 6 crops into the "REPORT" letters at about 3×.
- **Prompt:**
  > A flat top-down scan of a hand-made school "report card" poster on a plain pale sage-green paper background. Portrait rounded rectangle of teal construction paper with a thick black wax-crayon outline. Across the top, tall squeezed black crayon capitals reading "REPORTCARD". Below, a large rectangular photo window framed by a thick black crayon rectangle, the window itself filled with flat plain mid-grey (empty, for a photo to be added later). Under it the word "comments:" in lowercase black crayon handwriting. Across the bottom a glued strip of red paper with black marker capitals on two lines: "TAKES TOO LONG" (with "TOO LONG" underlined) and "TO FIND A MEETING TIME". Waxy crayon texture, kid-craft but neat, even lighting, no shadows, no other text or stickers.

**GPT-04 · Report-card slap stickers** (shots 6, 7, 49 and 50)
- **Items:**
  - "FAIL" on red/crimson paper (about 4:3 rectangle, big brush letters)
  - "PASS!" on emerald-green paper
  - "SETS MEETINGS / INSTANTLY!!" on a long emerald-green strip (two lines, italic-leaning marker caps)
- **Format:** transparent. The hand is comped in separately (GPT-12).
- **Prompt:**
  > A flat top-down scan of three hand-cut paper stickers on a plain light grey background, bold black brush-marker capitals: "FAIL" on a crimson-red paper rectangle; "PASS!" on an emerald-green paper rectangle; and a long emerald-green paper strip with two lines "SETS MEETINGS" and "INSTANTLY!!" in leaning hand-lettered marker capitals. Slightly uneven scissor-cut edges, matte paper, even light, no shadows, crisp and correctly spelled.

**GPT-05 · Crayon sticker sheet** (shot 4 LEO; shots 40–42 app stickers)
- **Items:**
  - "LEO": bubblegum-pink paper #F7B3E6, **purple** wax-crayon letters #8B2FB0, no border. This is the "handwritten caption" look.
  - "LOCATION": cream/pale butter paper #F6E3A1 with a black crayon border box and black crayon letters
  - "TIME": blue paper with a black border and black letters
  - "WORKING ON": red paper with a black border and black letters (two words, tightly spaced, as in the reference "WORKINGON")
  - "PRIORITIES": pink paper with a black border and black letters
- **Format:** transparent.
- **Prompt:**
  > A flat top-down scan of five hand-made paper labels on a plain light grey background, letters drawn in thick waxy crayon with visible crayon grain. Exact items: "LEO" in purple crayon capitals on bubblegum-pink paper, no border; "LOCATION" in black crayon capitals on pale butter-yellow paper with a black crayon rectangle drawn around the edge; "TIME" in black crayon capitals on bright blue paper with a black crayon border; "WORKING ON" in black crayon capitals on red paper with a black crayon border; "PRIORITIES" in black crayon capitals on pink paper with a black crayon border. Childlike but legible, even light, no shadows, correctly spelled.

**GPT-06 · LinkUp logo** (shots 39 and 40–43 header, HF-19)
- **Look:**
  - two overlapping hand-drawn **outline stars with smiley faces**, left pink #E0428A and right green #3DBE6A, thin felt-tip lines
  - below them, the wordmark **"LiNKUP!"** in multicolour felt-tip hand lettering: L pink, lowercase i teal with a tiny star as its dot, N teal, K pink, U pink-purple, P purple, ! pink-red
- **Format:** transparent PNG.
- **Prompt:**
  > A hand-drawn app logo on a transparent background: two overlapping outline five-point stars with simple smiley faces drawn in thin felt-tip pen, the left star pink and the right star green; below them the word "LiNKUP!" hand-lettered in felt-tip marker with each letter a different colour (pink L, a teal lowercase i whose dot is a tiny star, teal N, pink K, pink-purple U, purple P, pink-red exclamation mark). Playful, clean lines, no background, no other text.

**GPT-07 · MEETING TIME? painted globe poster, no cards** (shots 22–23)
- **Look:**
  - large off-white poster paper
  - "MEETING TIME?" hand-lettered in black marker capitals, arching across the top
  - a big hand-painted globe: ocean in blue poster paint with visible brush strokes and white streaks; continents (the Americas centred, Europe/Africa edge at the right) in bright green poster paint; thick black outlines
  - a small painted island dot near the lower left
  - no cards, no ticks
- **Format:** flat top-down scan, 4:3 landscape. Use the largest size available and upscale, since shot 22 zooms to about 2.5×.
- **Prompt:**
  > A flat top-down photo-scan of a hand-made poster on off-white paper. Across the top, black marker capitals "MEETING TIME?" arching in a curve. Below, a large hand-painted globe: ocean in blue poster paint with visible brush strokes and lighter streaks, continents (North and South America centred, the edge of Europe and Africa on the right) in bright green poster paint, all outlined with thick black marker. Kid-craft but bold, even daylight, no cards or stickers on it, no other text.

**GPT-08 · Name cards + tick chips** (shots 22–23)
- **Cards:** coloured paper cards mounted on black card stock (black margin all round). Each has a **blank grey photo slot** at the top left (for compositing headshots), black marker caps for the name, timezone below, and an empty small square slot right of the name.
  - "LEO" / "CEST(UTC+2)" on green #3DCB6E
  - "MULLET" / "BST(UTC+1)" on pale yellow #F3E3A0
  - "IZY" / "MDT(UTC-6)" on red #D7263D
  - "LUKE" / "EDT(UTC-4)" on blue #3C8FC6
  - "FIN" / "AEST(UTC+10)" on pink #F2A7C3
- **Ticks:** two small green squares with a black ✓, two small red squares with a black ✗.
- **Format:** transparent.
- **Prompt:**
  > A flat top-down scan on a plain light grey background of five hand-made name cards and four small tick squares. Each card is coloured construction paper glued onto slightly larger black card (black border all round), with an empty plain grey rectangle in the top-left corner where a photo will go, a name in big black marker capitals, a small empty square box to the right of the name, and a timezone in black marker capitals underneath. Exact cards: green card "LEO" / "CEST(UTC+2)"; pale yellow card "MULLET" / "BST(UTC+1)"; red card "IZY" / "MDT(UTC-6)"; blue card "LUKE" / "EDT(UTC-4)"; pink card "FIN" / "AEST(UTC+10)". Plus two small green paper squares each with a black hand-drawn check mark and two small red paper squares each with a black hand-drawn X. Even light, no shadows, correctly spelled.

**GPT-09 · Status signs** (shots 44–46)
- **Items:**
  - "ANYTIME": long green card #2ED47A, thin black border, condensed black marker caps
  - "MAYBE?": pale yellow card #F4E9A6, **thick** black border
  - "LEAVE ME / ALONE!": red card #E0263F, two lines, black marker
- **Format:** transparent cutouts for the HF-24 comp. The same flat art serves as the **Seedance prop ref** for Y7. A hand-held version is not generated here: the hand comes from Seedance or from GPT-12.
- **Prompt:**
  > A flat top-down scan of three hand-made cardboard signs on a plain light grey background, bold condensed black marker capitals: "ANYTIME" on a long bright green card with a thin black border; "MAYBE?" on a pale yellow card with a thick black border; "LEAVE ME" / "ALONE!" on two lines on a red card. Matte card, slightly uneven hand-cut edges, even light, no shadows, correctly spelled.

**GPT-10 · LIST OF CREATORS TO COORDINATE poster** (shot 21)
- **Look:** large white poster paper, slightly wavy as if just unrolled. Black brush/paint-marker caps, uneven and energetic:
  - "LIST OF CREATORS" / "TO COORDINATE", underlined
  - "☐ MULLETMAX" / "@ENGLAND" (ENGLAND in a teal box)
  - "☐ FIN@AUS" (AUS in a teal box)
  - "☐ LUKE@NYC" (NYC in a pink box)
  - "☐ IZY@CANADA" (CANADA in a pink-red box)
  - "☐ YING@SINGAPORE" (in a purple box)
- **Format:** flat front view, as the **Seedance prop ref** for Y2, so it's held and unrolled in-camera. If the text garbles in Seedance, track this flat art onto the poster in post.
- **Prompt:**
  > A flat front-on photo of a large white poster sheet, slightly wavy from being rolled, hand-written in bold black brush marker capitals: "LIST OF CREATORS" and "TO COORDINATE" underlined, then a checklist with hand-drawn empty square boxes: "MULLETMAX" with "@ENGLAND" below it, "ENGLAND" boxed in teal marker; "FIN@AUS" with "AUS" boxed in teal; "LUKE@NYC" with "NYC" boxed in pink; "IZY@CANADA" with "CANADA" boxed in pink-red; "YING@SINGAPORE" boxed in purple. Even light, plain background, correctly spelled.

**GPT-11 · Prop sheet: A BETTER WAY sketchbook + "WHAT." sign** (shots 35 and 24)
- **Sketchbook:** a top-spiral sketchbook with a faint grid page. A small pink paper chip with a black "A" sits at the top left, "BETTER" is huge in black paint marker, and a small yellow paper chip reading "WAY" sits at the bottom right.
- **"WHAT." sign:** a red paper strip with black marker "WHAT." and a big full stop. In the reference it's taped across a phone.
- **Format:** flat, as Seedance prop refs for Y2 and Y3.
- **Prompt:**
  > Two hand-made props photographed flat and front-on on a plain light grey background. Left: an open top-spiral sketchbook with a faint grid page; at the top left a small pink paper square with a black hand-written capital "A"; across the middle the word "BETTER" written huge in black paint marker; at the bottom right a small yellow paper rectangle with "WAY" in black marker. Right: a strip of red paper with "WHAT." written in bold black marker capitals with a big full stop. Even light, no shadows, correctly spelled.

**GPT-12 · Hand cutouts** (shots 6, 22, 49 and 50; HF-24)
- **Poses:**
  - (a) open flat palm pressing down, seen from above, entering from the bottom left (slaps)
  - (b) fingertips pinching and placing a small card, entering from the right (poster ticks)
  - (c) a hand and forearm entering from the left edge, gripping a sign's end with the thumb in front (signs)
- **Skin:** light skin with short natural nails, matching an off-camera friend of Ying.
- **Format:** transparent, realistic photo. HyperFrames adds the motion blur. (`seg1923/gen/hand.png` holds a marker and isn't reusable for these poses.)
- **Prompt:**
  > Three realistic photographs of a young woman's hand with light skin and short natural nails, each isolated on a transparent background, soft even daylight: (1) an open flat palm pressing down, seen from directly above, wrist entering from the bottom-left; (2) thumb and fingertips pinching a small card as if placing it, entering from the right; (3) a hand and forearm entering from the left edge, gripping the end of a flat sign with the thumb in front. Natural, sharp, no motion blur.

**GPT-13 · Chat stickers: original pink bear** (shots 30 and 32)
- **Poses:** a cute 3D-rendered pink bear (an original character, **not** Zanmang Loopy): (1) cheerful, paws on cheeks; (2) distressed, both paws on its head, angry brows, gritted buck teeth.
- **Format:** each a square image on a white background (chat-sticker style). It doesn't need to be transparent.
- **Prompt:**
  > Two square chat stickers of the same original cute 3D-rendered chubby pink bear character with round ears and a big dark nose, soft clay-like render, plain white background: (1) happy, both paws pressed to its cheeks; (2) frustrated, both paws on top of its head, angry eyebrows, gritted teeth. Not based on any existing character.
- Fallback with no gen: a 😭 emoji sticker.

---

## 4. Live-action / Seedance / stills placeholders (not ours today)

The editor drops in a grey slate with the label for each. Clip IDs refer to PORT.md.

1. Shot 1 (0.00–0.50): Leo leaning over a street café table, low wide (L1)
2. Shot 2 (0.50–0.92): Leo drinking iced coffee on the street (L1)
3. Shot 3 (0.92–1.29): Leo in a Chinese restaurant, hand on chin (L2)
4. Shot 4 (1.29–2.08): punch-in on Leo, same set (L2), under HF-05
5. Shots 5 and 7: a **still frame** from L2 for the report-card photo window (HF-06 and HF-27)
6. Shot 8 (4.75–5.83): Leo's webcam, rubbing her forehead, talking (L3), in HF-08
7. Shot 10 (11.13–13.50): Ying's webcam grimace (Y1) **plus a per-frame person matte** for "3AM"
8. Shot 11 (13.50–13.75): over the shoulder onto a laptop with Leo on the call. **Not in PORT's clip list** (see the decisions above)
9. Shot 12 (13.75–14.75): Leo's webcam, face in hand, laughing (L3), under HF-11
10. Shot 13 (14.75–16.00): 2 direct-flash Leo stills (plant shop with straw; couch with burrito)
11. Shot 14 (16.00–17.54): Leo at home, hands on head laughing, then a punch-in (L5)
12. Shot 15 (17.54–18.29): Leo on a couch with two laptops (L6)
13. Shot 16 (18.29–19.17): Leo in a car passenger seat, cap, laughing (L6)
14. Shot 21 (25.42–27.50): fisheye, Ying unrolls the LIST poster and peeks over it (Y2 + GPT-10 ref)
15. Shot 24 (30.25–31.25): fisheye, Ying shoves a phone calculator with the WHAT. sign at the lens (Y3 + GPT-11 ref)
16. Shot 25 (31.25–32.00): Leo laughing in her kitchen (L5)
17. Shot 26 (32.00–33.10): the same kitchen plate as 25, played inside the HF-14 window
18. Shot 27 (33.10–34.00): 4–5 old friend photos (group photo, school group, two girls, light-leak, night)
19. Shot 28 (34.00–34.58): three friends cheering in a mall (F1)
20. Shot 29 (34.58–36.00): Ying in a dorm room, wide, then a fisheye close-up on her phone (Y4)
21. Shot 31 (37.54–38.25): Ying furious at her phone, fisheye (Y4)
22. Shot 33 (39.92–41.79): Ying scratches her head and swings at the camera (Y4)
23. Shot 35 (43.50–44.46): Ying hides behind the A BETTER WAY sketchbook (Y2 + GPT-11 ref)
24. Shot 37 (45.29–46.13): handheld at the laptop on a messy desk, with the Chatly home in-camera (Y5 + HF-18 still)
25. Shot 39 (47.96–49.50): the laptop shows LinkUp in-camera (Y6 + HF-19 still)
26. Shot 44 (57.96–59.96): Ying on a sofa with her phone; ANYTIME sign (Y7 + GPT-09, or HF-24)
27. Shot 45 (59.96–61.25): Ying against a wall holding a yellow paperback; MAYBE? sign (Y7). Use a generic book, not "The Power of Habit"
28. Shot 46 (61.25–62.75): top-down fisheye, Ying hunched at a laptop; LEAVE ME ALONE! sign (Y7)
29. Shot 51 (67.67–70.33): Leo's webcam, dancing wildly (L4), in HF-28
30. Shots 52–53 (70.33–72.42): friends' group photo with ok-hand gestures (1 still, grainy film flash)
31. Shot 54 (72.42–73.00): blurred close frame of Leo's chin and lips (from L4), in HF-29
32. Shot 55 (73.00–76.17): Leo pointing at the camera, laughing (L4), in HF-30
33. **Support plate:** Ying's webcam loop for the Meet PIPs in shots 8, 12 and 55 (from Y1)
34. **Support stills:** headshot pack for the name cards and status cards: Izy (b&w photobooth, cap + sunglasses), Mullet/Max (curly mullet), Fin (cap, tongue out), Luke (NY cap at dinner), Leo & Max duo selfie (Swiss Alps), Ying with a camcorder, Leo (card). **Not in PORT's budget.**

---

## 5. Done

- `seg1923/`, 19.17–23.42 s:
  - crayon globe with "all over the world"
  - wall map: Singapore and Australia circles, Canada, "NY!", UK circle, whip-zoom, full map with every mark
- Final: `seg1923/out/seg1923-final-4x3.mp4`.
- Its last frame is HF-12's background.
- Nothing from this section is re-listed above.

---

## 6. Build order for tonight (most-used first)

1. **HF-01 word pops + HF-02 subtitles.** Used in about 40 of the 55 shots, and they unblock timing checks for the whole edit.
2. **HF-03 sticker motion kit + HF-04 line-boil kit.** Every sticker, slap, scribble box and burst depends on them (shots 4, 6, 9, 20, 22–23, 40–42, 44–46, 49–50, 55).
3. **HF-07 Meet chrome.** Shots 8, 10, 12, 51, 54 and 55.
4. **GPT-01 + GPT-02 chip sheets**, then **HF-09 kinetic type** (5.3 s, the biggest code shot) and **HF-12 map pile-up**.
5. **GPT-03 report card + GPT-04 slap stickers + GPT-12 hands**, then **HF-06 and HF-27** (both bookends, 5 shots).
6. **GPT-05 crayon sheet**, then **HF-05 LEO** and the app stickers.
7. **HF-11 Win95 dialog, HF-10 Ying tile / 3AM, HF-08 Meet speaker view.** These are owner call-outs.
8. **GPT-07 + GPT-08**, then **HF-13 MEETING TIME? poster** (owner call-out).
9. **LinkUp UI set:** GPT-06 logo, then HF-20, 21, 22, 23, 25, 26 and HF-19.
10. **Chatly ask:** HF-17 omnibox and HF-18 home. Also HF-16 converter, HF-15 chat (+ GPT-13), HF-14 black window.
11. **Seedance prop refs, needed before any Y2/Y3/Y7 gen:** GPT-09, GPT-10, GPT-11. Then HF-24 as the fallback.
12. **Close:** HF-28, HF-29, HF-30, HF-31 end card and 4:3 outro.
