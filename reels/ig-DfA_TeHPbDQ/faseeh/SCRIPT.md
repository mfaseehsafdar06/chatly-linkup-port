# "This is Faseeh": a Chatly story (the real script, received 2026-11-22)

This is the owner's script. It replaces the LinkUp port as the deliverable. The style still follows the LinkUp reference (IG DfA_TeHPbDQ): paper, marker, stickers, captions placed around faces. Everything in `../` (REF.md, ASSETS.md, assets/, hf/) is the style library for it.

**Format:** narrated by the teammate ("you"), with Faseeh on camera and handmade props. Runtime ~70 s, 4:3 at 1440×1080, 24 fps.

## 1. HOOK: meet the hero (0:00–0:06)
**On screen:**
- Faseeh at his desk, grinning at camera.
- A "FASEEH" name sticker slaps on.
- His face appears inside a paper **report card** with a big red **FAIL** sticker. Comment: "POSTED 3 HOURS LATE. AGAIN."

**VO:** "This is my teammate Faseeh. We both work at Chatly… and I'm trying to save his job."

## 2. THE PAIN, ACTED OUT (0:06–0:14)
**On screen:**
- Faseeh hunched over his laptop, with a 2am clock sticker.
- His phone buzzes and a paper notification card slides in: "where's the 9am post??"
- He looks up: "it's 9am… **in NEW YORK**".
- Facepalm, then a fake "Upload failed" error pop-up.

**VO:** "Every morning Faseeh has to post. Except 'morning' means New York, London and San Francisco… at the same time."

## 3. RAISE THE STAKES (0:14–0:30)
**On screen:**
- "Faseeh has an **impossible** task" in huge type over him, head in his hands.
- A paper scroll unrolls: **"FEEDER ACCOUNTS TO FEED"**, one checkbox per account: ☐ @gymtok.daily (US) · ☐ @studyhacks.pk (PK) · ☐ @aitoolsfyi (UK) · ☐ @sneakerdrops (US) · ☐ @mealprep.co…
  Caption: "the list goes on… soooo"
- A red marker circles cities on a paper world map. Timezone stickers: **−5 · 0 · +5**.
- Sticky notes cover his monitor: HOOKS? · CAPTIONS? · HASHTAGS? · TRENDING AUDIO??
- A calculator with a "**30 × 3 × 7**" sticker = **630**.

**VO:** "He runs dozens of feeder accounts. Every one has its own niche, its own voice, its own timezone. Three posts a day, each needing hooks, captions and hashtags… so that's 630 posts a week."
**Faseeh:** "What the hell."

## 4. MAKE IT UNIVERSAL (0:30–0:40)
**On screen:**
- "he's not the only one"
- Quick cuts of other marketers: teammates, friends, a coffee-shop laptop.
- Phone close-up of a Notes app called **"PROMPTS — DO NOT DELETE"**.
- A Google Doc titled **"MASTER PROMPTS v12 FINAL"**: copy, paste, delete "gym", type "study", paste again…
- Faseeh cringing.

**VO:** "Every social media marketer has this. A notes app full of prompts you copy, paste and rewrite thirty times a day, swapping one word each time. Let's just say… it doesn't scale."

## 5. THE FIX (0:40–0:44)
**On screen:** the narrator slides a printed card across his desk. It's a prompt with blanks, Mad Libs style: "Write 3 scroll-stopping hooks for a {{platform}} video about {{topic}}, in the voice of {{account}}, for {{audience}}."

**VO:** "So I showed him the Prompt Library in Chatly."

## 6. THE DEMO, translated into props (0:44–1:00)
Each screen shot alternates with its paper version.

| Feature | Screen | Real life |
|---|---|---|
| Write it once, leave the blanks | Prompt saved with `{{audience}}` highlighted | Faseeh writes the card once in marker, wrapping words in big hand-drawn `{{ }}` |
| Type @ in any chat | Typing `@` in a Chatly chat makes saved prompts pop up | Faseeh says "@" and the narrator instantly hands him the card |
| Fill in the blanks | Fields fill in (`@gymtok.daily`, TikTok, "leg day"), then send | He fills the blanks with a marker, flips to the next account and fills again: three cards in seconds |
| Share with your team | "Share with workspace" toggle | The card goes into a photocopier and copies fan out to the whole team's desks |

**VO:** "Write a prompt once and leave the blanks. Type @ in any chat and it's right there. Fill in the account, the niche, the platform, and it's ready to send. And when he writes a good one, the whole team gets it."

## 7. PAYOFF: the report card flips (1:00–1:06)
**On screen:**
- The feeder scroll with every box ticked ✓✓✓.
- The same report card goes from **FAIL** to **PASS!**. The comment is replaced: "EVERY ACCOUNT. ON TIME."

**VO:** "Faseeh doesn't rewrite the same prompt thirty times… **anymore.**"

## 8. CTA + sign-off (1:06–1:12)
**On screen:** Faseeh and the narrator high-five / desk dance, then "Comment **PROMPTS**", then the end card "a 💜 Chatly story".

**VO:** "So if you're running ten accounts, or fifty… comment PROMPTS and I'll send you the exact one Faseeh uses."

## Props checklist (from the script)
- Report card, with two versions of the comment and FAIL and PASS stickers.
- "FEEDER ACCOUNTS TO FEED" paper scroll.
- Paper world map, red marker, and timezone stickers (−5, 0, +5).
- Sticky notes: HOOKS? / CAPTIONS? / HASHTAGS? / TRENDING AUDIO??
- Calculator with a "630" sticker.
- 3–4 printed fill-in-the-blank prompt cards with big `{{ }}`.
- An "@" sign, and a photocopier (or just a stack of copies).
- "Upload failed" error pop-up (overlay in the edit).

## Checked against the real product (reference/chatly-web @ 079919718c)
- **Prompt Library** has its own page (`/prompt-library`).
- **Prompts** have a name, the prompt text and a visibility setting of **Private or Team**. The script's "Share with workspace" is the real **Team** visibility; on screen, use the real control's label.
- **Variables** use the `{{name}}` syntax (`PROMPT_VARIABLE_PATTERN`). In the editor they show as chips with three states: empty, active and filled.
- **Typing @ in the chat composer** opens the saved prompts (mention-prompt-library-store). Picking one inserts it, and you fill in its variable chips.

## Open points for the owner
1. **Numbers:** 30 accounts × 3 posts × 7 days = 630. The script says to check the real figures with Faseeh.
2. **VO vs. stickers:** the VO says New York, London, San Francisco, but the stickers say −5 · 0 · +5. The +5 matches the PK account, not San Francisco (−8). Pick one set.
3. **The house rule against South Asian markers:** "@studyhacks.pk (PK)" breaks it. Swap it for a neutral handle unless the owner wants it.
4. **Closing line:** house rule says every Chatly video ends on "Chatly. AI that works 24/7 for you." Add it after the "a 💜 Chatly story" end card, using the official outro.
5. **Have a real prompt ready** for the people who comment PROMPTS.
