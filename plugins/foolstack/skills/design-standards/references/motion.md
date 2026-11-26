# Motion, interaction and illustration

The rules for making a surface feel alive without decorating it. Code recipes for each pattern (React Native Reanimated plus expo-haptics, web CSS, Tailwind, Framer Motion) are in `motion-patterns.md`. A project's own motion rules override the defaults here; read them first.

## Rule 1: every animation communicates

If you can remove it without losing meaning, remove it. Each animation answers one question:
- **Where did it come from?** (entrance direction)
- **What changed?** (state transition)
- **Where should I look?** (attention, hierarchy)
- **Did it work?** (confirmation)

## Rule 2: timing

| Duration | Use for | Feel |
|---|---|---|
| 50-100ms | Press down (scale or opacity) | Instant, crisp |
| 150-200ms | Press release, hover in | Responsive |
| 200-300ms | Toggles, state changes | Quick but visible |
| 300-500ms | Transitions, reveals, sheets | Smooth, intentional |
| 500-800ms | Progress fills, celebrations | Satisfying |
| 800-1200ms | Draw-in, onboarding reveals | Cinematic, use rarely |

Under 200ms reads as instant, over 600ms reads as slow for anything a user waits on. Exits run slightly faster than entrances.

## Rule 3: easing

- **Ease-out** for entrances (`Easing.out(Easing.cubic)`, CSS `cubic-bezier(0.33, 1, 0.68, 1)`).
- **Ease-in** for exits.
- **Ease-in-out** only for loops (skeleton pulse, ambient breathing).
- **Linear never** for UI motion; only for indeterminate progress.
- **Springs never,** on any platform. Explicit duration and easing every time.

## Rule 4: stagger creates hierarchy

What matters most enters first. Base delay about 200ms to let the screen settle, then 60-100ms per item, total stagger under about 800ms, animate at most about 8 items and show the rest instantly. Never make the user wait for an entrance before they can act.

## Rule 5: hover, press and focus (web and desktop)

Pointer devices deserve the same care touch devices get from haptics.

- **Hover says "this is interactive, and here is what it does".** Use it on things that are clickable and not already obvious: cards, rows, chart marks, secondary actions. Small and fast: 150-200ms ease-out, a 1-2px lift, a background tint, an underline, a revealed secondary action, a tooltip with the exact value on a chart. Never hover on static content.
- **Hover is never the only way in.** Anything revealed on hover must also be reachable by tap and keyboard; touch devices have no hover. Gate hover styles behind `@media (hover: hover)` so they do not stick after a tap.
- **Press always,** even when hover exists: scale 0.93-0.98 down in 60-80ms, back in 180-200ms.
- **Focus visible always:** a clear `focus-visible` ring in the accent token, offset from the element. Removing outlines without a replacement is a P0.
- **Cursor tells the truth:** pointer on clickable, default on static, not-allowed on disabled with a reason shown.
- **Charts:** hover or tap a mark to show its exact value, dim the others; crosshair on time series.

## Rule 6: haptics (mobile) mirror the visual moment

Fire exactly when the visual state changes, never before or after, only for user-initiated or meaningful moments.

| Interaction | Haptic |
|---|---|
| Primary button | `impactAsync(Medium)` |
| Toggle, chip, slider tick | `selectionAsync()` |
| Swipe snap, pull-to-refresh threshold | `impactAsync(Light)` |
| Long-press entering a mode | `impactAsync(Heavy)` |
| Destructive confirm | `notificationAsync(Warning)` |
| Success, completion | `notificationAsync(Success)` |
| Error | `notificationAsync(Error)` |
| Progressive build-up | Light, Light, Medium, Heavy, then Success |

Guard haptics on web builds. Web has only the Vibration API, Android-only; feature-detect it or skip.

## Rule 7: animated illustration

Illustration earns its place where the user is waiting, starting, finishing or stuck, and the layout alone cannot carry the emotion:

- **Empty and first-run states:** an inviting, on-brand illustration plus one clear next action, so empty reads as a start, not breakage.
- **Success and milestones:** a short animated moment (under about 2 seconds, never blocking) whose intensity matches how rare the win is.
- **Onboarding:** one illustration per step that shows the value, not decoration beside a form.
- **Long known waits:** an illustrated progress moment instead of a bare spinner.
- **Errors and offline:** a calm, slightly human illustration that lowers the stakes, with the fix next to it.

How:
- **Tools:** Lottie (`lottie-react`, `lottie-react-native`) for designed animations, Rive for interactive or state-driven ones, CSS or SVG for simple line draws and loops. Keep files small and lazy-load them.
- **One illustration system per product:** a single style, stroke weight and palette drawn from the brand tokens. Mixed styles read as bought assets.
- **No generic stock:** no floating 3D blobs, no generic people-with-laptops, no unedited AI-generated art. If no fitting illustration exists, a strong typographic empty state beats a weak picture.
- **Budget by ICP and stakes:** money, health and grief get calm, sparse illustration; playful consumer products can go further.
- **Reduced motion:** show the final frame as a still.

## Rule 8: reduced motion

Respect `prefers-reduced-motion` (web) and the OS setting (mobile): skip entrances and decorative motion, keep functional state changes, show illustrations as stills, keep haptics.

## Pattern quick reference

| Element | Motion | Haptic (mobile) |
|---|---|---|
| Button | press 0.93, 60ms down, 180ms up | Medium |
| Card, row | press 0.98 or opacity 0.85, 80ms; hover lift 2px, 200ms (web) | Light |
| Toggle, chip | color and border 200ms, no delay | Selection |
| List | fade-up 350ms, 200ms base plus 80ms per item | None |
| Sheet, modal | in 350ms ease-out, out 250ms ease-in, backdrop fade 200ms, content staggers after | Light on open |
| Progress ring, bar | fill 600-800ms ease-out after the container settles | Success at 100% |
| Number change | count up 600ms ease-out | None |
| Milestone | appear, overshoot to 1.2, settle; under 2s | Escalating |
| Empty state | illustration fades in 400ms, text 100ms later, CTA last | None |
| Tab switch | cross-fade 200ms, no slide | Selection |
| Navigation | forward slide-in 300ms ease-out, back 250ms ease-in | None |

## What not to do

- Do not animate everything; static content stays static.
- Do not hide slow loading behind animation; use a skeleton.
- Do not run more than about 5 concurrent animations on screen.
- Do not use the same animation for every element; variety carries hierarchy.
- Do not add haptics to passive events (data loading, background refresh).
- React Native: no `TouchableOpacity`, `TouchableHighlight`, `TouchableWithoutFeedback` (use `Pressable`), no `Animated` from `react-native` (use Reanimated).
