# Design Pass Rubric

Walk every section on the surface being audited. Each check that fails becomes a finding in the contract shape defined in `audit.md`.

This rubric is platform-agnostic. Where it names a platform primitive (a haptic, a touch target, a native control) read it as "that platform's equivalent" — on web that is hover and focus states, keyboard reachability, and pointer affordances; on desktop it is cursor states, keyboard shortcuts, and window behavior.

---

## 0. ICP Calibration — apply this to every section below

**Every check in this rubric resolves differently depending on who the product is for.** There is no ICP-free reading of "premium", "dense", "obvious", or "delightful". Settle the ICP first (build Step 0 or review Phase 0), then carry it through every section as the tiebreaker.

| ICP dimension | What it shifts |
|---|---|
| **Age and vision** | Minimum type size and contrast, tap target size, whether the surface must survive the largest OS text setting. An older audience moves the floor up and makes dynamic-type support a P0, not a nicety. |
| **Tech and gesture fluency** | Whether a gesture-only affordance is acceptable at all. A fluent audience tolerates swipe-to-reveal and long-press menus; a non-fluent one needs a visible control for every action, and a hidden gesture becomes a P0 rather than a refinement. |
| **Context of use** | One-handed and on the move pushes controls into thumb reach and enlarges targets. At a desk permits density, hover, and keyboard paths. In bed or low light makes dark mode and glare the primary case, not the alternate. |
| **Frequency** | A daily driver earns density, speed, and learned shortcuts; labels can shrink into icons. An occasional or once-a-year surface must re-teach itself every time, so labels stay and guidance stays. |
| **Domain expertise** | Whether the surface may use the field's vocabulary directly or must translate it. Translating for experts is condescending; not translating for novices is exclusion. Both are findings. |
| **Emotional stakes** | High-stakes domains (health, money, legal, grief) call for calm, sober, reversible, and explicit confirmation. Low-stakes social and entertainment surfaces can be expressive, fast, and playful. Motion budget and celebration intensity follow directly from this. |
| **Device reality** | Old or low-end hardware, small screens, and poor connectivity cap the motion budget and make the loading and offline states primary rather than edge cases. |

**Two failure modes this section exists to prevent:**

1. **Auditing to your own taste.** Without a stated ICP, "make it premium" resolves to whatever the auditor finds beautiful. That is not a craft standard, it is a preference.
2. **Copying the wrong exemplar.** Linear, Arc, and Things are the reference for dense, expert, daily-driver tools used by fluent users at a desk. Holding a once-a-month surface for a low-fluency audience to that standard produces a screen that looks impressive and cannot be used. Name the exemplar that matches THIS ICP.

When a finding depends on the ICP, say so in the finding: "for a low-gesture-fluency audience, swipe-only delete is unreachable." That makes it arguable on the merits instead of on taste.

---

## 1. Brand Conformance

Graded against the project's own sources, loaded in Step 0 or Phase 0. This section is a list of QUESTIONS; the answers live in the brand file.

| Check | How to grade |
|---|---|
| Color | Every color in the surface traces to a named token. No raw hex, no `rgba()` literals, no `Colors.dark` reached directly where a theme hook exists. |
| Accent budget | The accent is doing the job the brand file assigns it (usually CTAs, active states, one signal), and covers roughly the share the file allows. A screen washed in accent has spent its scarcity. |
| Type | Every text style comes from the type presets. No ad-hoc `fontFamily` + `fontWeight` pairs. Font family count stays inside the brand limit. |
| Sizing | Every numeric size goes through the project's scaling utils, per its rule of thumb (fonts/radii vs. widths vs. heights). Hairline borders are the usual exemption. |
| Spacing rhythm | Gaps land on the project's base grid. Three arbitrary values where one token exists is a finding. |
| Corners, borders, shadows | Match the component-style section. A stock platform shadow where the brand specifies a hairline is a finding. |
| Motion | Duration, easing, and stagger match the motion rules. Any banned primitive (springs, legacy animation APIs, legacy touchables) is P0. |
| Copy | Every user-visible string obeys the copywriting rules: punctuation bans, the AI-ism blacklist, sentence rhythm. Read them out loud. |
| Brand don'ts | Walk the don'ts list literally, item by item, against the surface. |
| Dark and light | Both themes are correct, not just the default one. Check every hardcoded-feeling value: skeletons, scrims, disabled states, and any color that happens to equal the other theme's background. |

**Divergence rule:** when the code's real tokens disagree with the brand file, the code is the fact and the file is the bug. Note both, fix the file in the same pass.

---

## 2. The Premium Bar

Ten checks. A surface at the bar passes all ten; most failing surfaces fail three or four.

1. **One focal point.** Name the single thing this screen is for. If two elements compete for it, hierarchy has failed. If nothing claims it, the screen is a container, not a design.
2. **Type carries the hierarchy.** Weight, size, and color separate levels. Boxes, borders, and cards are how a weak layout fakes hierarchy it did not earn.
3. **Color is load-bearing.** Every non-neutral color means something specific. Decorative color is the fastest way to look templated.
4. **Optical alignment.** Edges line up down the column. Icons are optically centered, not mathematically centered. Text baselines relate.
5. **Density matches intent.** A scanning surface is dense; a decision surface is airy. A settings list and a paywall must not breathe the same way.
6. **Every state is designed.** See section 5 — this is where "good enough" surfaces are actually caught.
7. **Motion is one system.** The same category of change animates the same way everywhere in the app. Two different modal animations is a finding.
8. **Nothing is default.** No stock system alert where the app has a sheet, no default blue, no unstyled scrollbar, no platform-default shadow, no untouched placeholder text.
9. **The first second is right.** Before reading anything, does it look considered? Squint at it: the composition should still read.
10. **Reflective payoff exists.** Somewhere on this surface, or one step from it, is a moment the user would mention to someone. If the whole app has none, that is the finding.

---

## 3. Norman's Three Levels

Grade the surface at all three. Most working apps pass behavioral and fail the other two.

The three levels come from Norman's *Emotional Design* (2004): visceral is the immediate, pre-conscious reaction to appearance and feel; behavioral is the experience of USE; reflective is self-image, meaning, and the story the user tells afterward. The behavioral checks below additionally use the tools from *The Design of Everyday Things* — the two gulfs, signifiers, and mapping — because "does it give feedback" only tests half of that level.

### Visceral — the pre-conscious reaction
- Does the first frame look right before anything is read?
- Does the initial entrance have direction and sequence, or does everything arrive at once?
- Is anything visibly cheap: a stretched image, a jagged radius, mismatched icon weights, a font-substitution flash, a layout that jumps as data loads?
- **Test:** screenshot it, look for one second, look away. What is the impression?

### Behavioral — the experience of use

**Gulf of execution — can the user tell what they can DO here?**
- Is every available action signified by something visible? An affordance nobody can perceive does not exist.
- Is anything reachable ONLY by a gesture the surface never taught? (Weight this by ICP gesture fluency — see section 0.)
- Does the primary action look like the primary action, and is it reachable in this ICP's grip and context?
- Is the mapping natural: does the control sit near, and move like, the thing it changes?
- Are disabled controls explained, or do they just sit dead?

**Gulf of evaluation — can the user tell what HAPPENED and what state it is in?**
- Does every action produce feedback within one frame: a press state, and a haptic or hover/focus equivalent for the platform?
- Is every state change animated rather than cut, so the user sees WHAT changed and not just that something did?
- Is the current state legible at a glance without acting to find out?
- Do errors say what went wrong AND what to do, and distinguish offline from a real failure?
- After a slow or async action, is the outcome reported, or does the surface just quietly settle?

**Conceptual model**
- Would the user's mental model of what this screen does match what it actually does? A privacy control that silently governs nothing, a toggle whose label implies more than it changes, and a "save" that only saves locally are all P0 behavioral failures no amount of feedback polish can fix.

**Test:** trace each user action through the code twice. First for execution (how did they know they could?), then for evaluation (how did they know it worked?). Any missing link is a finding.

### Reflective — meaning and self-image
- Does the surface deliver a takeaway, or hand over raw output and make the user assemble the meaning?
- Is there anything here the user would screenshot, share, or miss if it disappeared?
- Does it reflect something the user built or chose, rather than something generic?
- Does the copy sound like a person who knows this domain, pitched at this ICP's expertise?
- **Test:** would the user tell a friend about this moment? If not, what would have to change?
- **Note:** Norman observes the levels can conflict, and reflective usually wins. A beautiful animation (visceral) that slows a daily task (behavioral) loses for a daily driver and may win for a once-a-year celebration. Resolve conflicts by ICP and frequency, not by which is prettier.

---

## 4. Slop Tells (2026)

Each of these reads as machine-generated or template-bought on sight. Any hit is at least P1.

**Visual**
- Sparkles / star-burst "AI" glyph / ✨ anywhere
- Purple-to-blue (or any unmotivated) gradient as a hero background
- Glassmorphism applied everywhere rather than to one deliberate layer
- Emoji standing in for icons
- Uniform card grid where every item carries equal visual weight
- The dashboard stack: white rounded cards with a hairline border, each holding a small label, a number and a progress bar, repeated down the page
- No signature: nothing on the screen a user could describe to a friend ("the one where the card fills up")
- Default-safe type with no reason (Inter, Geist, Manrope, system) and a palette that could belong to any product
- Fade-up on every element as the only motion idea
- "Multiple directions" that are one layout in different colors
- Drop shadows on every element
- Everything centered, including body text
- Three-column feature grid with an icon, a title, and two lines
- Icons from mixed sets, or mixed stroke weights in one row
- A mascot or illustration doing the work the layout should do

**Copy**
- "Unlock", "Discover", "Seamlessly", "Effortlessly", "Elevate", "Empower", "Take control of", "Introducing"
- Em dashes, en dashes, trailing ellipses
- "Welcome back!" with an exclamation mark and nothing else
- A headline that rhymes or alliterates but states no benefit
- Feature lists where an outcome sentence would convert better

**Structure**
- A settings screen that is a flat list of every toggle in creation order
- An empty state that is one grey icon and the word "Nothing here"
- A loading spinner where the content shape is known and a skeleton belongs
- Modal-inside-modal, or a system alert used as a design element

---

## 5. State Coverage

Walk the matrix. A missing cell is a finding, and unhandled states are the most common gap between a demo and a product.

| State | What to verify |
|---|---|
| First run / zero data | Reads as an invitation with a clear next action, not as breakage |
| Loading | Skeleton mirroring the real layout when the shape is known; the app's loading signature otherwise. Never a bare platform spinner. |
| Partial / slow | Something meaningful renders before everything arrives |
| Error | Says what failed and the one thing to do; recoverable without a restart |
| Offline | Distinguished from a real failure, and it RECOVERS on reconnect rather than sitting on the error forever |
| Empty after filtering | Distinguished from empty-because-new. Different copy, different action. |
| Maximum / overflow | Long titles, 3-line names, huge numbers, 200 items, the largest dynamic type setting |
| Success / completion | The moment is marked. Silence after a user finishes something is a wasted reflective beat. |
| Permission denied | The surface still works or explains itself; it does not dead-end |
| Locked / gated | Shows what is behind the gate rather than hiding it (tease, don't hide) |

---

## 6. Per-Surface Expectations

Extra checks by surface type, on top of everything above.

**Feed / list** — entrance stagger with hierarchy; refresh has a clear activation signal; pagination has a designed footer, not a bare spinner; each row has one clear primary target and any secondary action is discoverable without a hidden gesture.

**Detail** — the hero answers "what am I looking at" without scrolling; the primary action is reachable one-thumbed; secondary metadata is demoted typographically, not boxed.

**Form / input** — one question per screen where the flow allows; keyboard never covers the field or the CTA; validation appears on blur, not on every keystroke; the CTA states the outcome, not "Submit"; anything derivable is not asked.

**Sheet / modal** — follows the project's sheet doctrine exactly (panel and scrim animate independently where that is the house rule); dismiss is obvious; content staggers after the panel settles.

**Onboarding** — one viewport per step where the platform allows, no incidental scroll; one question or one reveal per screen; every answer is used downstream, and anything derivable is never asked; entrances staggered; every selection acknowledged.

**Paywall / gate** — the headline matches the surface that triggered it; the value is shown, not described; price framing is honest; no close button where the product's design says hard paywall.

**Celebration** — intensity matches rarity; the everyday win and the rare win must not fire the same effect; never blocks the user; respects reduce-motion by dropping movement while keeping feedback.

**Settings** — grouped by meaning, not by creation order; destructive and churn-adjacent actions live at the bottom, never the top; every toggle's effect is stated in plain words.
