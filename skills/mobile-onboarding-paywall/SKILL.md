---
name: mobile-onboarding-paywall
description: B2C mobile app flow: welcome screen with aha-moment video, auth screen, the three-act onboarding arc, Socratic ask-agree-show cycles, hard paywall vs freemium, social proof, and app-store review prompt timing under Apple guideline 5.6.3. Use when building or changing onboarding, a welcome or auth screen, an onboarding paywall, or a rating prompt.
---

# B2C onboarding and paywall

## App User Flow (B2C Mobile Apps)

Standard navigation and conversion flow for all B2C mobile apps:

### Welcome Screen
1. **Record** the app's aha moment (8-12 seconds screen recording)
2. **Convert** to MP4: `ffmpeg -i input.MOV -vcodec h264 -acodec aac -crf 28 -vf "scale=720:-2" -movflags +faststart output.mp4`
3. **Host** on Cloudflare R2 (not bundled in app binary). See the global Object Storage rule: never Supabase Storage.
4. **Display** in a phone frame built with Views (border + borderRadius + overflow hidden)
5. Video plays muted, `contentFit="cover"`, using `expo-video` (`useVideoPlayer` + `VideoView`). **Never infinite-loop a UI clip — play it exactly 5 times, then hold on the last frame.** The native `loop` boolean is unreliable for bundled assets (it sometimes plays once and stops), so take explicit control: set `loop = false`, count `playToEnd` events, and call `player.replay()` until a `MAX_PLAYS = 5` ref is hit. This applies to every short product clip in the app (welcome aha-moment, widget-setup tutorial, any future how-to clip), not just the welcome screen. Looping forever is frantic and drains battery while the user reads.
6. Title + CTA below the phone frame, white background
7. Two buttons: **"Get Started"** → onboarding, **"Already have an account? Sign in"** → auth screen
8. Never bundle video in the app binary. Stream from Cloudflare R2 for zero app size impact and instant updates.

### Auth Screen
- Apple Sign-In + Google Sign-In only visible by default
- **7-tap debug unlock**: Tapping the logo 7 times reveals hidden email/password sign-in and sign-up fields. This is for App Store reviewers and internal testing only. Session-only (resets on app restart).
- Used from welcome page for returning users

### Onboarding (Long, Psychologically Persuasive)
The onboarding follows the endowment effect pattern (CALAI/Noom style). Users invest time answering questions, making them far more likely to convert at the paywall. Structure:

1. **Identity & greeting** (name, age, referral source) — low friction, gets them started
2. **Motivation anchoring** (what do you want to achieve? what makes X great?) — makes them feel understood
3. **Pain points** (what frustrates you about X?) — establishes the problem
4. **Preferences** (specific choices about how they use the product) — deeper investment
5. **Demo / aha moment** (fake loader → personalized result reveal) — delivers value before asking for money
6. **Paywall** — presented AFTER they're fully invested. Hard paywall (no trial). Weekly/monthly/yearly tiers, all prices from RevenueCat (localized per country)
7. **Auth / sign up** — AFTER paywall purchase. Apple + Google + Email. This reduces friction at the paywall since they don't need an account to buy.

Key principles:
- Each screen asks ONE question or shows ONE thing
- Progressive disclosure, never overwhelm
- Staggered animations on every screen (see Motion Standards)
- Haptic feedback on every selection
- "Fake loader" before results builds anticipation

## Onboarding & Paywall Conversion Rules

Onboarding is the highest-leverage surface in any B2C app. Treat it as a funnel, not documentation. Every screen either invests the user or converts them. Cut anything that does neither. This is one of two places in a codebase where "lean" does not apply — optimize for conversion, not code elegance.

### The three-act arc (the organizing frame)

Before the individual principles, hold the whole onboarding as one story with three acts. The numbered principles below are the tactics; this is the shape they serve. It generalizes across any app type (utility, health, social, content, B2B): an app is a sales funnel, and every screen between the first open and the paywall has one job, building the case for why to pay.

**Act 1, Introduction (first ~3 screens plus the first aha).** Frame the problem and the solution fast. Within seconds the user must know what the app does and what it solves. Welcome them, name the problem in a way that stings a little, present the app as the solution in the plainest terms, then deliver one aha in under a minute: ask two or three quick questions and use their answers to show them something about their own situation they had not confronted. The problem becomes real and the app becomes urgent in the same breath. (Principles 1, 3, 4, 12 live here.)

**Act 2, Climax (let them DO the core thing).** The emotional peak, and the act most teams skip. Do not describe the core feature, let the user operate it once, right inside onboarding. If the app generates something, generate one for them. If it blocks something, let them feel the block. If it reveals something, let them tap and watch it reveal. A real hands-on taste of the actual mechanic beats any mockup or illustration (it is the strongest form of principle 12's SHOW). The user should finish this beat thinking "ok, this actually works." Then, at that peak, ask for the review (principle 15). Timing is the whole game: a small win first, the prompt at the exact high.

**Act 3, Conclusion (summarize, commit, close).** Reflect their journey back: where they are, where they want to go, how the app bridges the gap. You will feel repetitive because you mirrored their answers in Act 1. Do it anyway, attention is short and repetition is how the case sticks. Anchor the outcome to a concrete timeframe they can picture (a habit in 30 days, a result by a date). Then the micro-commitment screen (principle 5), then social proof (principle 9), then the paywall. If you run a free trial, say the app is paid before the paywall and reframe the price against a recurring cost they already accept (one coffee a month versus the problem they just spent ten minutes admitting they have). Only pre-disclose price when there is a trial, never as a bait-and-switch.

The throughline: most screens are not about the product, they are about making the user feel heard, reflect, and convince themselves they need it. People distrust being sold to and trust their own conclusions. By the paywall they are not deciding whether to pay, they are confirming a decision they already made.

### Principles

1. **Lead with identity and outcome, not features.** Headlines describe who the user is becoming or what they will achieve. Save feature tours for after the paywall. Functional copy ("Calculate doses precisely") is a tell that the team skipped the emotion pass.

2. **One question per screen.** Progressive disclosure always. Batching questions causes bounce.

3. **Dialogue over monologue.** Front-load self-identification questions (goal, pain, experience, context) within the first 3–5 screens. Every answer must personalize something downstream: demo, reveal, paywall copy, first-use pre-fill. If an answer is never used again, don't ask it.

4. **Show the aha moment before asking.** Fake loader ("Building your plan…") followed by a personalized reveal screen. The user sees what they're paying for before the price appears.

5. **Commit before asking for money.** One micro-commitment screen ("I'm in" / "I'm ready") immediately before the paywall. Heavy haptic, confirming animation. Triggers consistency bias. This is the single highest-ROI screen in any onboarding.

6. **Personalize everything downstream of the questions.** The demo uses their selection. The plan references their answers. The paywall headline includes their goal or product. Never show a generic demo after personalization questions. The user just spent effort; respect it.

7. **Pick a paywall-timing lane and commit.**
   - *Utility apps*: paywall within ~2 minutes. 82% of conversions happen day zero, most within the first two minutes. Don't bury it.
   - *Investment apps (Noom, CALAI, Flo)*: 10–15 screens of questions, demos, plan reveal, and commitment, then paywall. Endowment effect converts higher for self-improvement categories.
   - The mushy middle (5–6 feature screens then paywall) is the worst of both.

8. **Hard paywall, no close button.** Non-dismissible. `gestureEnabled: false`. If no free trial, create urgency with launch pricing, a countdown, or a personalized plan they've already invested in.
   - *The freemium exception (know when to break this rule).* Hard paywall is the default and wins for most apps: cross-app data (RevenueCat) shows roughly 5x the download-to-paid of freemium with near-identical one-year retention, and most trial cancellations happen day zero, so the first session is the real shot. But freemium is the right call when free users ARE the growth engine: network effects (each user makes the product better for everyone), word of mouth, or a core value you cannot ethically or practically wall (content the user expects to be free, e.g. core reference material, public data). In those cases keep a genuinely useful free taste and gate the premium LAYER (analysis, export, advanced views), never the core value or the user's own data. When freemium, the trial still does the heavy lifting, and a reminder one day before it ends is the single highest-ROI add.

9. **Social proof on the paywall.** Numbers when real, testimonials always. Never fake numbers. One "Join 10,000 users" screenshot when you have 40 kills credibility permanently.

10. **Emotional framing is mandatory.** Every app should evoke a feeling. Flo makes you feel understood. Duolingo makes you laugh. Headway makes you feel productive. Calm makes you exhale. Decide the feeling before writing copy.

11. **Telemetry on every screen.** Fire `viewed` on mount, `completed` on next, `back` on back-nav, plus the answer value. Without step-level events you can't find where the funnel leaks.

12. **Socratic activation before every value preview.** Don't tell the user they have a problem. Make them name it. For each major value moment, run a 3-screen cycle: ASK → AGREE → SHOW.
    - **ASK**: surface the user's current pain as a question with 4–6 picker options ("How do you do X today?" / "Where do you keep Y?" / "How often do you worry about Z?"). One-tap, no typing.
    - **AGREE**: validate their selection with social proof or stat ("X% of users say their tracking is messy" / "Y per Z = a lot of work"). Read-only, one CTA.
    - **SHOW**: animated solution screen using their answer. App screenshot or mock. The dopamine reward for the question they just answered. **The SHOW title must be painfully clear about the benefit, not clever.** State what the user GETS in plain words, and ideally answer the exact pain the ASK/AGREE just raised ("did I take Tuesday's shot?" → "Never wonder if you dosed."). Cute wordplay or rhythm with no payload ("Tap. Inject. Rotate.") is a failure mode at the reveal beat — it sounds nice and says nothing. Clear is not the same as dry: "Always know where to inject next" is clear AND carries the relief. If a title doesn't tell a stranger what the feature does for them, rewrite it.

    **Visual anchor rule (mandatory): no screen in a cycle is ever words-on-whitespace.** Each beat earns its tap with something to look at or touch — ASK is interactive by definition (tap options), SHOW carries the product visual, and AGREE must carry a visual that dramatizes the pain: a mock of the user's current broken workflow (a phone-calc strip showing "0.125 or 0.0125?", a messy notes-app scribble), a stat rendered as a graphic (count-up number, filled ratio bar), or a before/after fragment. A headline + sub floating on 70% empty screen reads as a filler tap, burns cognitive goodwill, and across 5+ cycles trains the user to skim. Text alone is never enough — if the AGREE beat has no visual worth shipping, fold its copy into the SHOW headline and cut the screen rather than shipping it bare.

    Why this works: self-persuasion beats other-persuasion. When the user PICKS their problem from a list, they own it. When the app TELLS them they have a problem, they dismiss it. CALAI/Noom/Headspace/Cal AI/Duolingo all run 10–20 of these activation cycles before the paywall. The structure also activates loss aversion (current pain made visceral), self-categorization (each answer puts them in a "this is the kind of person I am" bucket), and investment (every tap is commitment).

    Pacing: alternate Q-heavy and reveal-heavy stretches. Don't put 6 questions back-to-back — rotate Q→A→S blocks. After 5+ cycles, AGREE screens should reference the user's actual prior answers ("You picked Notes app + 3 peptides + over $500/mo bill — most people in your situation see X"). Hyper-personalization compounds the investment effect.

    Reusable shell pattern: build one `ActivationCycle` component (Q + A + S props) so each new cycle is ~30 lines of copy + answer options instead of three custom screens. Keeps the codebase lean even as the onboarding grows past 30 screens.

13. **Onboarding screens are fixed pages, never scrollable.** Every onboarding step renders as one clean viewport: headline + sub at top, the visual or interaction filling the remaining space (flex-centered), CTA pinned at bottom. If content doesn't fit, the content is wrong — scale the visual down, cut a card, or split the screen; never wrap it in a ScrollView. A scrollable slide signals "there's more below," splits attention, and makes the page read as unfinished. The shell component should make the fixed layout the default for showcase/preview/AGREE beats. Legit exceptions only: long-form legal text (medical disclaimer, privacy), multi-select lists that genuinely exceed the viewport, and the ONE personalized reveal / plan-ready climax screen (the CALAI/Noom "your plan is ready" wow-factor moment). On that single screen a deliberate scroll that unveils a "tuned to you" breakdown built from the user's own answers reinforces "look how much it set up for me" instead of reading as unfinished, so the scroll earns its place. It is the only step allowed to scroll: gate the scroll behind an opt-in shell prop (e.g. `scroll`) so every other step stays a fixed single viewport by construction, and the personalization must be HONEST (real reflections of their answers, never fabricated data).

14. **Frame the problem before the solution, and think in sequences, not single slides.** Never show a solution, or ask the user to set up a feature, on a screen that hasn't first established the problem or proof it addresses. A cold config/feature ask ("when should X remind you?") reads as a chore; the same ask after a problem or proof beat reads as a payoff. Judge cognitive load per SEQUENCE, not per isolated screen: when one screen would have to carry both the "why" and the "ask", split it into a short sequence (proof or problem, then the feature, then the ask) rather than one dense slide. Each screen stays light and earns itself in context. This generalizes the Socratic ASK -> AGREE -> SHOW (principle 12) from value previews to every feature and config screen. Any proof must be HONEST (real, citable research framed conservatively), never a fabricated outcome stat ("people who do X earn more") or an unverifiable namedrop.

15. **Ask for the app-store review at the FIRST REAL WIN AFTER onboarding, never inside it.** Reviews are the most valuable thing the majority-who-never-pay can give you: social proof for every future visitor, and App Store ranking, starting with owning the top spot for your own app name. Every review compounds into free organic installs, so for ASO-dependent apps this beat is a growth lever, not a courtesy. Never gate the prompt behind anything dishonest, and never beg.

    **The hard constraint: Apple guideline 5.6.3 forbids a rating request on first launch or during onboarding, and they enforce it.** An earlier version of this rule said "fire it at the Act 2 climax, inside onboarding," and a production app was rejected in App Review for doing exactly that. The reviewer's wording: "The app requests users to rate the app on first launch or during onboarding, before they've had enough time to gain a clear understanding of the app's value." No StoreReview call may exist anywhere in the onboarding tree.

    The peak-timing instinct was right, the location was wrong. Ship it like this instead:
    - Trigger on a genuine post-onboarding win: their first saved artifact, their first completed session, a milestone they can see. Attach it to a peak the USER produced, not one the onboarding staged.
    - **The core habit must be a trigger, not just the rare features.** If the app's everyday action is reading, logging or listening, completing it counts as a win. One app triggered only on niche features that 3 to 6% of users touched, and under 3% of its users had ever been asked. Wire the nudge to the thing nearly everyone does.
    - Put an engagement floor in front of every trigger: **~8 hours since install**, so no prompt can fire in the sitting that installed the app. A reviewer tests in one sitting, and finishing a tutorial or walkthrough does not end it. Eight hours outlasts any sitting but still asks someone who comes back later on install day. Size the floor against the paywall timing: if there is a trial, the ask has to land inside it. A 2-day floor on a 3-day trial leaves one day to ask, and in one app it reached about 15% of new users; 8 hours reached about 37%. Never lower it into the first sitting, which is the rejection again.
    - Because the floor swallows early wins, the trigger must NOT also be gated on "first" or on an exact count (1st, 7th, 14th) at the call site, or a user whose qualifying win lands inside the floor burns their shot on a call that could never fire. Call the nudge on every win and let its own guards (already reviewed, lifetime cap, spacing, floor) decide.
    - Cap it: ~3 lifetime prompts, 7+ days apart, and never again once they have reviewed. iOS throttles `requestReview` to 3/year anyway.
    - Log an event every time the app asks, carrying which trigger fired it, so you can see which moment earns reviews. It records the request, not a display: iOS may show nothing, and Google Play only shows the sheet to installs from Play (test via internal app sharing or a testing track; a sideloaded build never shows it).
    - A user-initiated "Rate this app" button in Settings should deep-link to `https://apps.apple.com/app/id<APP_ID>?action=write-review`, NOT call `requestReview`. The system API is throttled and silently no-ops, so a button wired to it looks broken.

    Onboarding still gets its Act 2 climax. It just ends on a Continue, not on a rating sheet.

### Anti-patterns

- ❌ Feature tour carousel with no personalization
- ❌ Asking for email, account, or auth before the paywall (adds friction without adding investment)
- ❌ Generic demos AFTER collecting personalization answers
- ❌ Info overload — multi-bullet feature lists where one outcome sentence would convert better
- ❌ Over-branded vocabulary that new users don't recognize
- ❌ Em/en dashes in onboarding copy (reads as AI-written, see Copywriting Rules)
- ❌ A back button on the paywall
- ❌ A close button on the paywall
- ❌ Shipping onboarding without step-level analytics
- ❌ Showing a value-preview screen WITHOUT a Socratic activation question first (see principle 12). Telling the user "we do X" without first surfacing the pain "you're doing X badly today" leaks conversion.
- ❌ Socratic question screens with 9+ options (decision fatigue). Cap at 4–6.
- ❌ AGREE screens that don't reference back to the user's selection (wastes the personalization opportunity)
- ❌ Text-only screens anywhere in an activation cycle — headline + sub on empty whitespace with no visual anchor (see the visual anchor rule in principle 12). Every beat needs a visual or an interaction; a bare-text AGREE screen is a filler tap that should either get a pain visual or be folded into the SHOW screen.
- ❌ Scrollable onboarding slides (see principle 13). Showcase/preview/AGREE screens are fixed single-viewport pages; if the content overflows, shrink the visual or cut content — don't reach for a ScrollView. The sole exception is the personalized reveal/plan-ready climax screen, which may scroll (principle 13).

### Further reading

- https://www.revenuecat.com/blog/growth/fix-onboarding-funnels/
- https://www.revenuecat.com/blog/growth/onboarding-campaign-tutorial-onesignal-revenuecat/
