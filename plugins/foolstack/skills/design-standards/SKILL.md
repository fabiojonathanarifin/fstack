---
name: design-standards
description: The design bar for every user-facing surface: top-tier 2026 UI/UX as a FAANG-level CDO would ship it, built from the ICP's point of view on Don Norman's three levels of emotional design, with purposeful motion, hover and press states, micro-interactions, haptics and animated illustration where they earn their place. Load BEFORE building or changing any screen, page, component, dashboard, chart, form, onboarding, paywall, landing page, email or other UI, on any platform (web, React Native, Softr Vibe Coding, HTML artifacts), even when the user does not mention design. Also use to review or polish existing UI - "make this top tier", "feels templated / generic / AI slop / flat / dead", "polish pass", "design pass", "Don Norman", "micro-interactions", "animation", "haptics", "does this match our brand".
---

# Design standards

Every surface a user sees is designed as if a top Silicon Valley CDO, FAANG level, will review it in 2026. "It works" is not done. **It works beautifully, for this specific person,** is done.

The default output of an AI agent is generic: stock components, centered cards, a gradient, a sparkle, copy that says "seamlessly". That is the failure this skill exists to stop, and it happens most when nobody asked for design explicitly. So this skill applies to all UI work, asked or not.

**Two modes:**
- **Build** a new or changed surface: follow the build workflow below, in order, before you show anything.
- **Review** an existing surface ("polish this", "feels like AI slop"): follow `references/audit.md`.

## The bar, in five lines

1. **For someone.** Good UX only exists for a named ICP. No ICP, no design.
2. **Norman's three levels, all of them.** Visceral (right in the first second), behavioral (effortless, every action answered), reflective (they would be proud of it, or miss it if it were gone).
3. **One takeaway per screen.** The user feels or concludes the one thing that matters before they read the detail.
4. **Alive, not decorated.** Motion, hover, press, haptics and illustration each communicate something. Remove anything that only decorates.
5. **Nothing default.** No stock look, no placeholder copy, no unhandled state, no raw values where a token exists.

## Build workflow

### Step 0: Load the bar for this project

Read, in this order: the PRD, README, `CLAUDE.md` (project and global), any brand guidelines or design-token files, the shared UI primitives, and two or three surfaces the project already got right. Code is the truth about tokens; a stale brand file is a bug to fix, not to follow.

- **ICP gate.** State the ICP back in one sentence: age and vision, tech and gesture fluency, context of use (one-handed on the move, desk, in bed), frequency, domain expertise, emotional stakes. If the docs do not say, **ask before designing.** Never infer it from the product category.
- **House style.** State the accent rule, the type rule and the motion rule you found. If there is no brand definition at all, propose a three-line direction (palette and accent job, type pairing, motion personality), say it is a proposal, and offer the `branding-strategy` skill. On a time-boxed build, proceed on the proposal; otherwise get a yes first.

### Step 1: Write the design brief (five lines, before any code)

```
For:        <ICP in one sentence>
Takeaway:   <the one thing this screen makes them feel or conclude>
Visceral:   <what makes the first second right>
Behavioral: <the primary action, and how every action is answered>
Reflective: <the moment they would mention to someone, or would miss>
```

Then pick the **reference level that matches this ICP**, not your taste: Linear, Things or Arc for dense expert daily tools; Apple Wallet, Monzo or Headspace for calm consumer money and health; Duolingo for playful habit loops. Copying the wrong exemplar produces a screen that photographs well and fails its user.

Then commit to an **art direction with a signature**, in three lines, before any code:

```
Idea:       <the one concept the screen is built around, e.g. "the card is the meter: it fills like a glass">
Signature:  <the one element nobody else ships, that a judge or user would remember and describe>
Type/color: <a pairing chosen for THIS idea, with a reason, plus the single job of the accent>
```

A layout that could hold any product's data is not a direction. If the honest description of the screen is "cards with a label, a number and a progress bar", start over. When asked for several directions, each must be a different **idea**, not the same layout in a new palette.

Set the **motion budget** from the ICP: high emotional stakes (money, health, grief) means calm, sober, reversible, and celebration only for real wins. Low stakes and playful means more expressive. Old hardware or poor connectivity caps it further.

### Step 2: Build it

Experiences, not screens. Before building the core surface, ask the three lenses:

1. **Takeaway, not raw output.** Most products hand over numbers or lists and make the user assemble the meaning. Lead with the meaning ("$45 left, 85% used"), make the detail secondary. Feeling only counts once the output is correct and fast.
2. **For a behavior you want repeated, is skipping it felt?** A streak, a status, something they built. It must be something the user chose to grow, never a punishment and never their data held hostage.
3. **Assume the feature is commoditized.** What considered layer around it would a competitor not bother with? Timing, the right detail in the right place, friction removed. Craft is the moat.

Craft rules while building:

- **Hierarchy through type,** weight, size and color, not boxes and borders. One focal point. Density matches intent: scanning surfaces dense, decision surfaces airy.
- **Color is load-bearing.** Every non-neutral color means one thing. The accent is scarce.
- **Tokens only.** Colors, type, spacing, radii, motion durations come from the project's centralized tokens. A missing token gets added to the token file, never hardcoded in a component.
- **Every interactive element answers within one frame:** press state, plus hover and visible focus on web, plus a haptic on mobile where it is meaningful. A control with no feedback reads as broken, not minimal.
- **Every state change animates** so the user sees what changed, not just that something did.
- **Design every state,** not just the happy one: first run, loading (skeleton when the shape is known), partial, error with the one thing to do, offline that recovers, empty after filtering, overflow, success, permission denied, locked. See `references/rubric.md` section 5.
- **Motion, hover, haptics and illustration** follow `references/motion.md`. Platform recipes (React Native Reanimated, web CSS, Framer Motion, Tailwind) are in `references/motion-patterns.md`.
- **Platform references, read only when the task touches them.** iOS system surfaces (anything growing out of the Dynamic Island, hiding the status bar, coach-mark tips, sheet-then-share sequencing, invite messages) follow `references/ios-system-surfaces.md`. Read it before building any of them.
- **Copy** follows the `copywriting-rules` skill: plain, concrete, no em dashes, en dashes or ellipses, no AI phrases.
- **One thing at a time.** Each screen has one primary question or action; secondary context supports it, never competes. Reveal detail as it becomes relevant.
- **Reduce user work.** If you can derive it, don't ask for it; if you can infer it, don't make them type it. Smart defaults over blank slates: pre-select the most common option.
- **Accessibility is part of the bar:** contrast, tap targets sized for the ICP, keyboard and screen-reader paths, reduced motion respected.

### Step 3: Self-check before showing anything

Never hand over an unchecked first version. Walk these against what you built:

1. **The ten premium checks** in `references/rubric.md` section 2.
2. **Every slop tell** in `references/rubric.md` section 4. Any hit gets fixed now.
3. **The state matrix** in section 5. Missing states get built or named as deferred.
4. **Every interaction traced twice:** how did they know they could (signifier), how did they know it worked (feedback).
5. **The five-line brief:** does the result deliver the takeaway and all three levels? If not, it is not done.

If a check fails, fix it before showing. Then report briefly: the brief, what was checked, and **what needs a real device or browser to confirm** (motion feel, haptics, hover and focus, theme rendering, screen readers). Never call those verified from code alone; use the project's verify skill or the `run` skill when one exists.

## Non-negotiables (zero tolerance)

- **No sparkles icon,** star-burst AI glyph or ✨, anywhere, ever. Say "AI" or "premium" through copy, type and color.
- **No springs.** Explicit timing, ease-out for entrances, ease-in for exits, never linear for UI motion. Most transitions 300 to 500ms.
- **No emoji as icons,** no mixed icon sets or stroke weights in one row.
- **No unmotivated gradients, glassmorphism everywhere, drop shadows on everything, everything centered.**
- **No hardcoded colors, font sizes or spacing** in components.
- **No copy-rule violations** in any string a user reads.
- **No dead interactions.**

## Rationalizations to reject

| Thought | Reality |
|---|---|
| "The user didn't ask for design, just build it" | Every UI is judged on design. Unasked is exactly when slop ships. |
| "Default shadcn / stock components look clean enough" | Stock is what every other app looks like. Clean is the floor, not the bar. |
| "It works, polish later" | Later is a review round the user has to ask for. Polish is part of done. |
| "I know good design, I don't need the ICP" | You know your taste. A dense expert UI aimed at a low-fluency user is a worse screen that photographs better. |
| "A gradient / glow / mascot would lift this" | Decoration on the edges does not fix the core moment. Fix what the screen is for first. |
| "Animate it so it feels premium" | Motion that communicates nothing is noise. Each animation answers where it came from, what changed, where to look, or did it work. |
| "There's no token, I'll hardcode it once" | Add the token. One literal becomes forty. |
| "Looks good in my head, it's done" | Run the self-check, then name what needs a real device. |

## Red flags: stop and go back a step

- Writing UI code before the five-line brief exists
- No ICP stated, or one you made up
- The phrase "here's a clean, modern design" forming in your head
- Any new hex, font size or spacing literal
- A sparkle, an emoji icon, a purple-to-blue gradient, glassmorphism
- A spring, or motion with no stated duration and easing
- A control with no press, hover or focus state
- Showing the user a first version you have not self-checked

## Related skills

- `copywriting-rules` (and `humanizer` for long-form): every word a user reads.
- `branding-strategy`: when no brand definition exists.
- `mobile-onboarding-paywall`, `in-app-premium-gating`, `subscription-winback`: surface-specific rules that sit on top of this bar.
- `ux-audit`: flow-level friction. This skill asks "is it worth owning"; that one asks "can they get through it".
- `expo-react-native`: the Reanimated stack and bottom-sheet pattern on mobile.
