# Review mode: bring an existing surface to the bar

Use when a surface exists and does not clear the bar ("polish this", "feels templated", "AI slop", "design pass", "audit the animations"). **Craft is diagnosed, not applied:** a surface misses the bar for a specific, nameable reason at a specific line. Find it, then fix it. Starting with a redesign skips the only step that makes the result better rather than merely different.

## Phase 0: load the bar

Same as build Step 0 in `SKILL.md`: confirm the ICP (ask if the docs do not say), read the house style from brand files and real tokens, and state in four lines who it is for plus the accent, type and motion rules. If you cannot, you have not read enough to grade anything.

## Phase 1: audit one surface

Scope to one screen, flow or component family. A whole-app request gets split and run one surface at a time.

Read the surface's real code end to end plus every component it renders. Walk `rubric.md` in full: ICP calibration, brand conformance, the premium bar, Norman's three levels, slop tells, state coverage, per-surface checks. Grade what the code does, not what component names imply.

Then build the **interaction map**: every interactive element on the surface, one row each.

```
| Element | File:Line | Press | Hover/focus (web) | Haptic (mobile) | Transition | Verdict |
```

Verdicts: `GOOD`, `DEAD` (zero feedback), `MISSING_PRESS`, `MISSING_HOVER_FOCUS`, `MISSING_HAPTIC`, `MISSING_ANIMATION` (hard cut on a state change), `WRONG_WEIGHT` (feedback weight does not match the action's importance), `VIOLATION` (spring, linear easing, hardcoded color, legacy touchable). Count them: "31 of 44 elements have full feedback" is a finding, "feels good" is not.

Every finding uses this shape; a finding missing a field is not yet a finding:

```
### [P0] Activating a list row gives no feedback for 400ms
- Where: components/ResultsList.jsx:88
- Level: behavioral, gulf of evaluation
- User experiences: taps a row, the screen sits still, taps again, two navigations queue
- Fix: wrap the row in the shared press-feedback primitive; navigation already fires on activate
- Primitive: <the project's real token, component or util, or NEW with why nothing existing covers it>
```

- **User experiences** is an observable symptom, not a design term.
- **Findings that depend on the ICP say so,** so they are arguable on merit, not taste.
- **Severity:** P0 ship-blocker (banned pattern, dead interaction, a missing state a real user will hit, copy-rule violation, hardcoded value where a token exists). P1 reads templated or the core moment does not land; this is most of a pass. P2 a refinement a designer notices and a user only feels.

Order P0 first. If the surface is already at the bar, say so; an invented finding is worse than none.

## Phase 2: spec

Write findings to `docs/design-pass/<surface>-<YYYY-MM-DD>.md` (or the project's existing report convention), with one line at the top naming the one thing this surface is for. More than 10 findings, or any finding that needs a product decision: settle scope with the user before touching code. Otherwise fix P0 and P1, list P2.

## Phase 3: fix

- Implement in the project's idiom; reuse the primitive each finding names; extend shared components rather than forking.
- No new raw color, size or spacing literal where a token exists.
- **Every change traces to a numbered finding.** Anything else is a new finding to approve, or left alone.
- **A design pass changes how a surface feels, not what it does.** Product changes (merging sections, changing defaults, rewriting what copy claims) need the user's approval before the diff, not a mention after.
- Reuse before rewrite; a full rewrite needs agreement first.

## Phase 4: verify

Run the project's build, typecheck and relevant tests; re-read each fixed surface against its finding. Report what was fixed, what was deferred and why, and **what could not be verified without running it** (motion, haptics, hover and focus, screen readers, theme rendering on real hardware). Never call those verified from the diff.

## Review rationalizations to reject

| Thought | Reality |
|---|---|
| "It needs a redesign, let me rewrite the screen" | You cannot name what was wrong, so nobody can tell whether the rewrite is better. Audit first. |
| "While I'm in here I'll also fix this behavior" | A cosmetic request becomes an unreviewed behavior change. One finding, one change. |
| "I'll mention the behavior change in my summary" | After the diff is not consent. Flag it before, as a finding. |
| "The findings are the deliverable" | The pass ends in shipped, verified code. |
| "The brand file is stale, I'll use my judgment" | Read the real tokens, say the file is stale, fix the file in the same pass. |
