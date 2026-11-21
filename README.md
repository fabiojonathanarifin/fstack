# fstack

Skills for Claude Code from a solo founder shipping B2C apps. Built while running EchoForge, maker of Protos, Airlophone and ReadersGuild. Each rule came from a real launch, a rejection, or a bug that cost a day.

## What's inside

| Skill | Loads when you are |
|---|---|
| `engineering-principles` | planning, debugging, refactoring or reviewing code |
| `design-standards` | designing any screen, flow or interaction |
| `copywriting-rules` | writing anything a user reads |
| `mobile-onboarding-paywall` | building onboarding, a paywall, or a review prompt |
| `in-app-premium-gating` | adding a locked feature or upgrade prompt |
| `subscription-winback` | building a cancel flow or retention offer |
| `expo-react-native` | working in an Expo or React Native app |
| `in-your-own-words` | typing `/in-your-own-words` to check the agent understood your goal |

Skills load only when the task calls for them, so they cost nothing the rest of the time.

## Install

```
/plugin marketplace add fabiojonathanarifin/fstack
/plugin install fstack@fstack
```

## A few rules worth knowing

- Apple rejects apps that ask for a rating during onboarding (guideline 5.6.3). Ask after the first real win, at least 8 hours after install.
- RevenueCat checks entitlements by the entitlement ID, not the product ID. A mismatch makes every purchase succeed while access stays locked.
- When two fixes built on the same assumption both fail, test the assumption before writing a third.
- A win-back offer should be a StoreKit promotional offer, not a cheaper public product that undercuts full-price sales.

## Optional: always-on rules

Skills load on demand. If you want the core principles in every session, paste this into your `CLAUDE.md`:

```markdown
- Design for the scale the product implies, not the toy example in front of you.
- When two fixes that share one assumption fail, write the assumption down and test it before a third fix.
- Before trusting a number, name what limits it and rule out that it measured something else.
- Fix where the system first went wrong. A guard on a state that should never exist hides the bug.
- No em dashes, en dashes or ellipses in user-facing copy.
- Never use a sparkles icon.
```

## Credits

Several engineering principles are adapted from [pstack](https://github.com/cursor/plugins/tree/main/pstack). The `copywriting-rules` skill works best alongside [humanizer](https://github.com/blader/humanizer).

## License

MIT
