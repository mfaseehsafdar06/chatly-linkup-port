# Chatly port of IG DfA_TeHPbDQ: "a Chatly story"

The user decided on 2026-11-22: brand Chatly, live action made with lean Seedance, 4:3 at 1440×1080, 24 fps like the reference. Shot numbers below refer to the shot list in REF.md.

## Script (near-verbatim port)

Only these lines change from the transcript:

| t | Reference | Chatly port | Why |
|---|---|---|---|
| 44.4 | "So I decided to make something that will solve this problem for good." | unchanged (the screen shows Chatly instead of Lovable) | The reference doesn't name the tool in the VO either. |
| 44.5–47.9 | Chrome "lovable.dev", Lovable home "What should we build, Ying?", ask typed | chatlyai.app in the address bar, the real Chatly app home, the ask typed in the composer, then the Sites pane builds LinkUp | Brand and product UI |
| 49–64 | "LOVABLE TEAM" in the app | "CREATOR CREW" | Removes the competitor name |
| 74.9 | "a ♥ Lovable story" end card | "a [Chatly mark] Chatly story", then the official outro with "AI that works 24/7 for you." | Brand plus the required close |
| end | (none) | VO: "Chatly. AI that works twenty-four seven for you." | Every video must close on this line (core message) |

The rest stays word for word: Leo, Ying, LinkUp, every city list, "Hell no.", "comment LINK UP and I'll send you the link!".

The people are newly designed characters in the same spirit as the reference. They are not lookalikes of the real Leo and Ying.

- **Leo:** woman, late 20s, messy dirty-blonde bob, small tattoos, cap in the outdoor shots.
- **Ying:** East Asian woman, early 20s, short hair with a fringe, oversized white tee.

## How each part is made

**Built in code (free):**
- the kinetic paper type (shot 9)
- the crayon globe (17)
- the map sticker pile-up (20)
- the "MEETING TIME?" poster (22–23), as stop-motion paper with a hand cutout
- the report card, with FAIL/PASS/SETS MEETINGS slapped on (5–7, 49–50)
- the black photo-window trick (26, 52)
- Meet/webcam frames and the Win95 error
- the phone group chat (30, 32)
- the time-converter site (34)
- the Chatly ask (36, 38) and every LinkUp screen (40–43, 47–48), all built from the real Chatly UI kit and recorded like screen captures
- the Meet reaction bar (54)
- both caption styles and all stickers

**Seedance 2.5, 1080p, 4:3, with character sheet refs: 15 clips, about 77 s in total**

| Clip | Shots | Content | Length (s) |
|---|---|---|---|
| L1 | 1–2 | Leo on the street: leans in grinning, then drinks iced coffee (two cuts) | 4 |
| L2 | 3–4 | Leo in a Chinese restaurant, hand on chin, mouth open, wide and low | 4 |
| L3 | 8, 12 | Leo's webcam: asks about Tuesday 9pm, then buries her face in her hand laughing | 8 |
| L4 | 51, 55 | Leo's webcam: dances wildly, then points at the camera | 8 |
| L5 | 14, 25 | Leo at home: hands on head laughing, then laughing in the kitchen | 5 |
| L6 | 15–16 | Leo on a couch with two laptops, then laughing in a car passenger seat (two cuts) | 5 |
| Y1 | 10–11 | Ying's webcam: "Ummm… it's 3am", grimacing | 4 |
| Y2 | 21, 35 | Fisheye: unrolls the LIST OF CREATORS poster and peeks; hides behind the "A BETTER WAY" sketchbook (props from code-rendered refs) | 6 |
| Y3 | 24 | Fisheye: shoves the phone calculator with the WHAT sign at the lens, screaming | 3 |
| Y4 | 29, 31, 33 | Dorm room: wide shot, phone close-up, furious, scratches her head and swings at the camera | 8 |
| Y5 | 37 | Handheld at the laptop: the Chatly home screen in-camera (UI ref) | 3 |
| Y6 | 39 | The laptop shows the LinkUp app in-camera (UI ref) | 3 |
| Y7 | 44–46 | Holding the signs: ANYTIME on the sofa, MAYBE? against a wall, top-down LEAVE ME ALONE! | 8 |
| F1 | 28 | Three friends cheering in a mall | 3 |
| M1 | 18–19 | Hand with a red marker circling Singapore, Australia and Canada, writing "NY!" on a wall map | 5 |

**Images: about 11 stills**
- 2 character sheets (Leo and Ying)
- 2 direct-flash Leo photos (13)
- 6 old friend photos (27, 52–53)
- 1 hand cutout for the paper slaps

**Voice:**
- Ying's narration: ElevenLabs TTS, auditioning 2–3 voices so the user can pick.
- On-camera lines (L3, Y1, Y3): ElevenLabs voice-changer on the takes' own audio, so the lip-sync is kept.

**Music:** first try a bed from the archive music-lib; generate one only if nothing fits.

## Cost

These figures come from the rate in chatly-yt-clickup's cost.tsv, where Seedance 2.5 1080p cost about 360 credits per second:

| Item | Credits |
|---|---|
| 15 clips, ~77 s of video | ~28K |
| ~11 stills | ~1.1K |
| Voice | under $1 on fal |
| **Total** | **~30K credits** |

There are no drafts and no second takes, unless a shot is unusable.

On 2026-11-22 the ImagineArt connector was not connected. It has to be reconnected in claude.ai settings, or fal can be used as the fallback (fal returned an IP-block 403 on 2026-11-20).

## Build order

1. Build every code and UI part, plus the edit on placeholders, and check timing against the reference at 10 fps.
2. Make the character sheets, then show them for approval.
3. Generate the 15 clips, drop them in, grade (warm green cast, grain, vignette, fisheye on the Ying shots), mix.
4. Compare side by side with the reference at the same timestamps, then hand over.
