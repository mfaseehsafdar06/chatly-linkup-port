# Review: 1122 rough cut (2026-11-22)

**Source files:** `~/Downloads/1122.mov` (1920×1080, 30 fps HEVC, 72.13 s) and `1122.WAV` (the same VO, 44.1 kHz). Both are copied to `faseeh/footage/`, which is kept out of git.

**The cut:** 16 live shots laid on the full VO, with black gaps where graphics go: 12.0–19.0, 28.1–34.0, 35.8–62.5 and 65.5–68.8.

**Audio:** clean, −19 LUFS, LRA 2.1. The .mov audio is the same as the WAV, so use the WAV.

**Storyboard:**
- `STORYBOARD-1122.jpg` is labelled; `frames/NN_{L,G,N}.jpg` are plain 1440×1080 4:3 crops.
- Each gap is filled with the built P-xx graphics.
- `build_storyboard.py` rebuilds it, and `storyboard-1122.json` is the timing table.

## Must fix
1. **Profanity at 10.2 s:** "What the f***?". It breaks Meta ad policy and differs from the script's "What the hell." Fix it one of these ways:
   - bleep it
   - reuse the 34.2 s "What the hell?"
   - re-record that line
2. **The numbers don't add up:** the VO says "dozens of accounts … 3 posts a day … 360 posts a week". 360/21 isn't a whole number of accounts, so the P-27 sticker (30×3×7=630) has to change. The recommendation is a plain "360 posts / week" sticker with no multiplication.
3. **City name:** the VO says "In San Francisco", so P-24c "in NEW YORK" becomes "in SAN FRANCISCO".

## Missing
- **"He's not the only one" (35.8–39.3):** P-14 needs 3–4 quick clips of other people on laptops. Without them it's a placeholder.
- **28.1–34.0 (5.9 s):** only the 1.5 s calculator exists. A code graphic for "hooks · captions · hashtags" and "360/week" still has to be built.
- **65.5–68.8 ("10 accounts or 50"):** the P-28 scroll is 2 s, so a "10 or 50" pop needs adding.
- **The 35.8–62.5 run:** it's 27 s of screens with no live action. The reference cuts back to faces, so cutaways of Faseeh reacting would help. Spare takes from the shoot would cover this.
- **Report card FAIL/PASS (P-22/P-23):** no straight-to-camera plate was filmed. Either drop them or freeze a frame of L06/L15.

## Notes
- **Format:** the footage is 16:9 at 30 fps, and the edit is 4:3 at 24 fps. Live shots use a centre crop. L04 is offset right (cx .62), L05/L07 left (.42), L13 left (.40). The Meet tiles L06/L08 are centred.
- **Meet tiles L06/L08:** they're soft because they're zoomed screen recordings. They're usable, but a light sharpen and grain will help them sit with the phone footage.
- **L01:** the tagged person is the teammate. Nobody is named on screen except Faseeh.
