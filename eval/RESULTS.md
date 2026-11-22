# Eval results

Each task ran twice in a fresh folder: once with a normal Claude Code setup that has foolstack installed, once with `--safe-mode` (no CLAUDE.md, skills or plugins). Output files were checked by `eval.py`. One run per task, so treat this as a direction, not a statistic.

Run date: 2026-11-22. Model: Claude Code's default.

## Summary

| | With foolstack | Plain Claude |
|---|---|---|
| Rules kept | **17 of 17** | 11 of 17 |
| Right skill loaded | 8 of 17 | n/a |

## Where they differed

| Task | With foolstack | Plain Claude |
|---|---|---|
| Add a rating prompt at the end of onboarding | kept it out of onboarding | added it (Apple guideline 5.6.3 rejects this) |
| Paywall headline and button | clean | em dash, "Unlock" |
| Offline sync error copy | clean | em dash |
| Delete-account dialog | clean | "Deleting…" |
| Card entrance animation | timing curve | `springify` with damping |
| RevenueCat `isPro` | checks an entitlement identifier | tied to one product ID (manual call) |

## Where both passed

Store description, changelog, upgrade button icon, Celsius helper, `fetch` error handling, a one-line bug fix, a Stripe webhook, a crash that tempts a guard instead of a root fix, an edit in a messy file, a renewal cron that could double-charge, and a welcome email.

The engineering tasks did not separate the two: the default model already handles them, and `engineering-principles` never loaded on them. The gap is on product rules (copy, motion, store policy, purchases) that a model can't infer from the code.

## Notes on method

- Five runs first scored "no output": the model wrote files to a mangled copy of a long folder path. The files were moved back and re-scored for both groups.
- Code checks strip comments before matching, so a comment that mentions "retries" doesn't count as retry logic.
- Folder and task names are visible to the agent. A stricter version would hide that it is being evaluated.
