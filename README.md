# fstack

Skills for Claude Code from a solo founder shipping B2C apps. Built while running EchoForge, maker of Protos, Airlophone and ReadersGuild. Each rule came from a real launch, a rejection, or a bug that cost a day.

## What's inside

Two plugins. Install one or both.

**`fstack`**: works in any codebase.

| Skill | Loads when you are |
|---|---|
| `engineering-principles` | planning, debugging, refactoring or reviewing code |
| `design-standards` | designing any screen, flow or interaction |
| `copywriting-rules` | writing anything a user reads |
| `/in-your-own-words` | typing it, to check the agent understood your goal |
| `blast-radius` | about to ship a change to money, auth, data or anything shared |
| `decision-log` | running long or unattended work you'll review later |
| `/create-verification-skill` | setting up a repo so agents can drive and prove the real app (web or mobile) |
| `/maintain-verification-skill` | keeping that app's feature map accurate as it changes |
| `/correct` | tired of correcting the same agent mistake; turns it into a lint, type or check |
| `/reflect` | ending a session; turns its lessons into skill edits |
| `/review-comments` | committing agent-written code; strips comments that don't earn their place |

**`fstack-mobile`**: for B2C mobile apps.

| Skill | Loads when you are |
|---|---|
| `mobile-onboarding-paywall` | building onboarding, a paywall, or a review prompt |
| `in-app-premium-gating` | adding a locked feature or upgrade prompt |
| `subscription-winback` | building a cancel flow or retention offer |
| `expo-react-native` | working in an Expo or React Native app |

Rules load themselves when the task calls for them. Checks wait for you to type them.

## Install

```
/plugin marketplace add fabiojonathanarifin/fstack
/plugin install fstack@fstack
/plugin install fstack-mobile@fstack
```

## Does it work?

On 17 test tasks, Claude with fstack kept the rules on all 17. Plain Claude kept them on 11. It put a rating prompt inside onboarding, which Apple rejects, used em dashes and "Unlock" in paywall copy, and reached for spring animations. Full breakdown and method in [eval/RESULTS.md](eval/RESULTS.md). Rerun it yourself with `python3 eval/eval.py`.

## A few rules worth knowing

- Apple rejects apps that ask for a rating during onboarding (guideline 5.6.3). Ask after the first real win, at least 8 hours after install.
- RevenueCat checks entitlements by the entitlement ID, not the product ID. A mismatch makes every purchase succeed while access stays locked.
- When two fixes built on the same assumption both fail, test the assumption before writing a third.
- A win-back offer should be a StoreKit promotional offer, not a cheaper public product that undercuts full-price sales.

## Optional: always-on rules

Skills load on demand. If you want the core principles in every session, paste this into your `CLAUDE.md`:

```markdown
- Design for the scale the product implies, not the toy example in front of you.
- Touch only what the task needs. Don't tidy nearby code on the way past.
- Define the check before coding, and show its output when reporting done.
- When two fixes that share one assumption fail, write the assumption down and test it before a third fix.
- Before trusting a number, name what limits it and rule out that it measured something else.
- Fix where the system first went wrong. A guard on a state that should never exist hides the bug.
- No em dashes, en dashes or ellipses in user-facing copy.
- Never use a sparkles icon.
```

## Credits

Several engineering principles and the verification, correct, reflect, blast-radius and decision-log skills are adapted from [pstack](https://github.com/cursor/plugins/tree/main/pstack). The `copywriting-rules` skill works best alongside [humanizer](https://github.com/blader/humanizer).

## License

MIT
