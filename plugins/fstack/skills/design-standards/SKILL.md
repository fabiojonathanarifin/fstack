---
name: design-standards
description: Premium product design rules: no sparkles icon, purposeful motion with explicit timing and no springs, haptics that mirror visual state, progressive disclosure, reducing user work, and building experiences instead of screens (emotional takeaway, felt cost of skipping, enriching around a commoditized feature). Use when designing or reviewing any user-facing screen, flow, or interaction.
---

# Design standards

## Design & Motion Standards

These are style-agnostic — they apply whether the app is minimal/clean, neo-brutalist, playful, or editorial. Adapt the visual language per project, never these principles.

### Iconography — NEVER use the sparkles icon
Never use a sparkles icon anywhere, on any surface, in any project. This means `sparkles` (SF Symbol), the star-burst "AI shimmer" glyph, the ✨ emoji, and any variant. It is the single most overused "AI feature" cliche and instantly reads as cheap, templated, and generic, which directly undercuts the premium 2026-YC bar. It is banned on buttons, upgrade/paywall CTAs, section headers, empty states, onboarding, marketing, everywhere. Convey "premium," "AI," or "magic" through copy, type weight, color (e.g. the brand accent), and layout, never a sparkle. When an icon is genuinely needed, pick a concrete glyph that names the actual action or thing (an arrow for upgrade, a specific object for the feature). Zero tolerance, no exceptions; treat a stray sparkle as a ship-blocker.

### Animation — Purposeful, Not Decorative
Every animation must communicate something: state change, hierarchy, causality. If you can remove it without losing meaning, remove it.

- **Staggered entrances** — elements enter sequentially, guiding the eye top-to-bottom. Use incremental delays (80–120ms per item). Don't dump everything at once.
- **Delay = hierarchy** — what matters most appears first. Secondary content follows.
- **Easing** — ease-out (`Easing.out(Easing.cubic)`) for entrances (decelerates, feels natural). Ease-in for exits. Never linear — it feels robotic.
- **Duration sweet spots** — 300–500ms for most transitions. Under 200ms feels jarring. Over 600ms feels slow. Progress/draw-in animations can go 800–1200ms.
- **Functional animation** — fill a ring to show goal progress. Stagger checklist ticks to show work being done. Animate day dots in sequence to show a schedule being built. The animation *is* the communication.

### Haptics — Mirror the Visual Moment
Haptics should fire exactly when the visual state changes — not before, not after.

- Pair every meaningful visual event with a haptic: tap → select, item checks off → impact, flow completes → notification
- **Progressive intensity** — if the experience builds (checklist filling, streak milestone), escalate haptic weight: Light → Light → Medium → Heavy
- Use `selectionAsync()` for small toggles (chips, radio buttons). `impactAsync()` for confirmations. `notificationAsync(success)` for completions.
- Never haptic on passive/ambient events — only user-initiated or meaningful system moments

### Progressive Disclosure — One Thing at a Time
Don't show everything upfront. Reveal information as it becomes relevant.

- If two steps collect the same information, collapse them into one (derive what you can from what the user already gave you)
- Screens should have one primary question or action — secondary context supports it, never competes
- Use in-screen state transitions (step 1 → step 2 within a slide) only when truly necessary; prefer full-screen navigation otherwise

### Reduce User Work
If you can derive it, don't ask for it. If you can infer it, don't make them type it.
- Frequency of 3 days = they picked 3 days. Don't ask "how many days" then "which days" separately.
- Smart defaults > blank slates. Pre-select the most common option, let them change it.

### Motion on React Native
Never springs, on any platform. On React Native, the `expo-react-native` skill in fstack-mobile has the Reanimated motion stack and the bottom-sheet pattern.

## Experience Design: Build Experiences, Not Screens

Features are commoditized and copyable in a weekend. What users stay for is the
experience around the feature. This is a meta-principle, not a tactic list: it
applies to any product (mobile, web, a bot, a dashboard, an email a user reads).

The test before building any core surface: am I shipping a SCREEN (it shows data
or performs a function) or an EXPERIENCE (the user feels something, owns something,
or would miss it if it were gone)? If it is just a screen, one of the three lenses
below is the upgrade. Run them as questions, not templates.

### Lens 1: Is the emotional takeaway delivered, or just the raw output?
Most products hand over raw output (numbers, a list, a transcript, a generated
draft) and make the user assemble the meaning. The upgrade is delivering the
takeaway so they feel it before they parse it. Ask: when the user hits this
surface, what is the one thing they should feel or conclude? Lead with that, make
the detail secondary. You earn the emotional layer only AFTER the output is correct
and fast; feeling layered on a broken or slow core is a gimmick that churns.

### Lens 2: For a behavior you want to recur, is the cost of NOT doing it felt?
Tracking a metric is passive. The durable version makes the ABSENCE of the behavior
cost something the user can see. The form is product-specific (a streak, a status,
something they built that decays, a thread that goes cold); the constant is
"skipping it is felt." Boundary: the stake must be something the user chose to grow,
never a punishment you impose, and never their own data held hostage (see In-App
Premium Gating). Honest loss aversion, not a dark pattern.

### Lens 3: Assume the core feature is commoditized. What do you enrich around it?
If an AI can clone the headline feature overnight, the moat is the considered layer
around it: timing, the right metadata in the right place, friction removed, the
detail nobody asked for. Compete on that layer, not the feature list. This is WHY
the UI-constants, motion, and haptics rules exist. Craft is the moat, not a polish
item done last.

### The one distinction that catches most misses
Decoration on the edges (an effect on the periphery, a friendly label, a mascot) is
not the same as making the core moment feel different. Edge-decoration is cheap and
changes nothing; the lenses above are about the core. When in doubt, ask which one
you are actually doing.

(Grounding: Lens 1 is Norman's visceral/emotional design, Lens 2 is loss aversion
plus endowed progress, Lens 3 is Saffer's microinteractions. Exemplars: Carrot
Weather, Forest, Day One.)
