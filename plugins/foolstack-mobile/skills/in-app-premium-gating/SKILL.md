---
name: in-app-premium-gating
description: Post-onboarding premium gates: tease don't hide, source-aware paywall copy, frequency caps over hard locks, growing personalized counters, never holding user data hostage, tier laddering. Use when adding or changing any locked feature, upgrade prompt, or paywall that fires after signup.
---

# In-app premium gating

## In-App Premium Gating (Post-Onboarding)

These rules govern paywalls that fire AFTER signup, when a user hits a feature locked behind premium. Different problem from the onboarding paywall: in-app gates fire over weeks of repeated usage, so they have to keep working without feeling hostile. The reference designs are CMB's "Likes You" feed and Bumble's Beeline — both convert well because they exploit loss aversion correctly.

### Core principle: tease, don't hide

Loss aversion is asymmetric. An unopened door is abstract; a glass wall with the prize behind it is visceral. Free users should SEE what premium unlocks, not hit a flat "you can't do this" wall.

- Show blurred previews of locked content (a sample AI conversation, a redacted CSV preview, a chart that visibly cuts off).
- Show locked items as cards/rows with redacted detail, not as missing entries.
- Show real, growing numbers ("23 entries beyond your 14-day window") instead of static caps ("history limited to 14 days").

CMB shows blurred faces of people who liked you with a live count. Bumble's Beeline does the same. The user has mentally claimed the value before they've paid for it. That's the conversion engine.

### Source-aware paywall copy (pure-win optimization)

The paywall headline must match the surface that triggered it. Same SKUs, same screen, different framing per entry point. Zero downside, lifts conversion.

```js
// ✅ Good — gate sheet receives source, swaps headline + hero per surface
requirePremium('save_habit')
//   Headline: "Track unlimited habits"
//   Hero:     "Keep every habit you care about, not just three."

requirePremium('csv_export')
//   Headline: "Export your data"
//   Hero:     "Download a CSV of every check-in for your spreadsheet or coach."

requirePremium('ai_coach')
//   Headline: "Ask the coach"
//   Hero:     "Get protocol guidance whenever you need it."

// ❌ Bad — same generic headline regardless of trigger
requirePremium('save_habit')
//   Headline: "Unlock Pro" (identical for every gate in the app)
```

If you're already plumbing a `source` string through to analytics, reuse it for copy. Build a copy table keyed by source.

### Frequency caps over hard locks (when feasible)

For repeatable actions, free users should TASTE the feature and run out, not be locked out cold. A user who has used a feature once is dramatically more likely to pay than one who has only seen it gated.

- ✅ "3 free AI messages, then upgrade" — they feel the value
- ✅ "1 CSV export per quarter, then upgrade" — they get the workflow once
- ✅ "5 SuperSwipes per week" (Bumble) — premium feature, free trickle
- ❌ "AI is locked" with zero usage — abstract value proposition

Not every feature fits this. One-time-setup features (e.g., "save more than one protocol") work better as quotas with teased previews.

### Personalized, growing counters

Static cliffs don't compound. Personalized counters do. The longer the user uses the app, the bigger the locked number, the more it hurts to walk away.

- ✅ "47 entries beyond your 14-day window" — grows with engagement
- ✅ "12 saved habits waiting" — locked habit cards visible with name redacted
- ❌ "History limited to 14 days" — flat message, same for everyone

### Boundary: never hold the user's own data hostage

Dating-app patterns DON'T transfer cleanly to health, finance, productivity, or any app where the user produces their own data. Crucial distinction:

- ✅ Tease premium-only features (AI, exports, advanced analytics, sharing)
- ✅ Tease premium-only VIEWS of user data (a chart that cuts off, with "see full trend" CTA)
- ❌ Hide entries the user logged behind a paywall as if they don't exist
- ❌ Block read access to data they previously created

Apple App Review has rejected health/medical apps that hold logged user data behind paywalls. The user must always be able to see and export their own data, even at the free tier. Gate the premium *analysis layer*, not the data itself.

Mental model: a paid view is a feature; the data is theirs.

### Tier laddering (when applicable)

If you have multiple tiers, position them as anchors:
- Cheap tier: frequency unlocks (more uses, faster, more often) — Bumble Boost
- Expensive tier: the killer feature only paid users get — Bumble Premium's "see who likes you"

Two doors with one obvious upgrade. Don't prematurely build this for v1; single-tier is fine until you have a killer feature worth anchoring against.

### Anti-patterns

- ❌ Generic gate sheet that shows the same headline for every triggered surface
- ❌ Hard locks on features the user has never seen (greyed-out icon with no preview)
- ❌ Hiding the user's own logged data behind a paywall
- ❌ Static quota messages instead of personalized growing counters
- ❌ Putting the only paywall in onboarding and never re-engaging users mid-session
- ❌ Em/en dashes in any paywall copy (see Copywriting Rules)

### Reference designs

- CMB "Likes You" feed: blurred faces with count, premium reveals identities
- Bumble Beeline: same pattern, more aggressive count display
- Hinge "Roses": frequency-capped premium action (1 free per week)
- Duolingo Hearts: frequency-capped resource that regenerates over time, paid tier removes the cap
