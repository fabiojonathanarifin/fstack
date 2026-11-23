# foolstack

I'm Fabio. I build and run multiple apps Protos, Airlophone, ReadersGuild, etc.

Agents are great at code and bad at product. Mine wrote paywalls that said "Unlock premium" next to a sparkles icon. They checked the wrong RevenueCat ID, so people paid and stayed locked out. They reached for spring animations, em dashes and "seamless" in every headline. And Apple rejected one of my apps because a rule I'd written for my own agents told them to ask for a rating during onboarding.

foolstack is every one of those lessons written down so agents stop repeating them. Two things it does:

- **Product sense.** Copy that doesn't read as AI, design and motion that feel premium, and for mobile apps the onboarding, paywall, review-prompt and win-back rules that decide whether an app makes money.
- **Engineering discipline.** Fix root causes, touch only what you were asked to, prove the work in the running app, make retries safe, turn repeated mistakes into checks that fail.

Rules load themselves when the task needs them. You don't have to remember any commands to get the benefit.

It works on any stack. The core plugin is product and stack agnostic. The mobile plugin is opinionated about Expo, React Native and RevenueCat, because that's what I ship. Fork it and swap in yours.

## Install

In Claude Code:

```
/plugin marketplace add fabiojonathanarifin/fstack
/plugin install foolstack@foolstack
/plugin install foolstack-mobile@foolstack
```

Install `foolstack` for any project. Add `foolstack-mobile` if you build B2C mobile apps.

## Get started

1. **Install it.** That's most of it. From now on the rules load when the task needs them: copy rules when you write copy, design rules when you build a screen, engineering rules when you debug.
2. **In each project, run `/create-verification-skill` once.** It writes a project skill so agents can launch your app, sign in a test account, reach any feature and show you screenshots as proof. This is the single biggest step toward trusting what agents hand back.

New here? The [one-page guide](GUIDE.md) walks through a normal day.

## Examples

```
/in-your-own-words add team invites with a seat limit
```
The agent restates your goal, the smallest change that meets it, and what it's assuming. Then it waits. Use it before anything big or fuzzy.

```
write the paywall for my habit tracker
```
No command needed. The copy rules load: no em dashes, no "unlock", lead with what the user gets.

```
/correct
```
Finds the mistakes agents keep making in this repo, including from your past sessions, and turns each one into a lint rule, type or check whose error message names the fix.

```
what could this break? I changed how refunds are calculated
```
`blast-radius` loads, finds the one fact the change is safe because of, and proves it by running real code.

## What's inside

**`foolstack`**: any codebase.

| Skill | Loads when you are |
|---|---|
| `engineering-principles` | planning, debugging, refactoring or reviewing code |
| `design-standards` | designing any screen, flow or interaction |
| `copywriting-rules` | writing anything a user reads |
| `blast-radius` | about to ship a risky change: payments, login, user data, database migrations |
| `perf-investigation` | fixing anything slow: measure, change one thing, re-measure |
| `decision-log` | running long or unattended work you'll review later |
| `/in-your-own-words` | typing it, to check the agent understood your goal |
| `/create-verification-skill` | setting up a repo so agents can drive and prove the real app (web or mobile) |
| `/maintain-verification-skill` | keeping that app's feature map accurate as it changes |
| `/correct` | tired of correcting the same agent mistake |
| `/reflect` | ending a session; turns its lessons into skill edits you approve |
| `/review-comments` | committing agent-written code; strips comments that don't earn their place |

**`foolstack-mobile`**: B2C mobile apps (Expo, React Native, RevenueCat).

| Skill | Loads when you are |
|---|---|
| `mobile-onboarding-paywall` | building onboarding, a paywall, or a review prompt |
| `in-app-premium-gating` | adding a locked feature or upgrade prompt |
| `subscription-winback` | building a cancel flow or retention offer |
| `expo-react-native` | working in an Expo or React Native app |

Rules load themselves. Commands (the ones with a `/`) wait for you.


## Always-on rules (optional)

Skills load on demand. If you want the core rules in every session, paste this into your `CLAUDE.md`:

```markdown
- Design for the scale the product implies, not the toy example in front of you.
- Touch only what the task needs. Don't tidy nearby code on the way past.
- Define the check before coding, and show its output when reporting done.
- When two fixes that share one assumption fail, test the assumption before a third.
- Fix where the system first went wrong. A guard on a state that should never exist hides the bug.
- No em dashes, en dashes or ellipses in user-facing copy.
- Never use a sparkles icon.
```

## Make it yours

These are my rules. Some of them are strong opinions: hard paywalls, no springs, comments only when they explain a why. Fork it, delete what you disagree with, and add the lessons your own agents taught you. `/reflect` and `/correct` help you write those down.

## Credits

The verification, correct, reflect, blast-radius and decision-log skills, and several engineering principles, are adapted from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan (MIT). If foolstack makes your agents build better products, pstack makes them better engineers. They work well together. The `copywriting-rules` skill pairs well with [humanizer](https://github.com/blader/humanizer).

## License

MIT
