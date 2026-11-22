---
name: create-verification-skill
description: "Generate a project-local verification skill that drives your app the way a user does (web, mobile, desktop, CLI or API), with a feature map so any agent can reach and prove any feature without a setup conversation. Use for /create-verification-skill, \"make a verify skill for this repo\", or when agents can't check their own UI work."
disable-model-invocation: true
---

# Create a verification skill

Agents can only be trusted with work they can check. This skill gives a repo a scripted way to run the real app, drive a feature the way a user would, and capture proof. It writes a project-local skill at `.claude/skills/verify-<app>/`, read cold mid-task by an agent that has never seen the app. Write for that agent, not for a human.

## 0. Find what is real before anything else

Before writing a single drive step, find out what the local setup can touch:

- Does local dev share a database with production?
- Are payment keys live, or test mode?
- Can the app send real email, SMS, push or calls?
- Does it report to analytics, ads or attribution in a way that pollutes real data?

If any answer is yes, the generated skill gets a **Safety** section at the top with hard stops:
- the named test accounts it may use
- the actions it must never take unless the user asked for that specific run (charges, top-ups, refunds, outbound calls or messages, deletes of real rows, publishing)
- how to recognize that it is pointed at live data

Read-only by default. Never weaken a safety stop to make a journey pass.

## 1. Interview the repo, not the user

Answer from the codebase. Ask the user only what you cannot observe.

- **Surface:** what does a user touch? Web UI, mobile app, desktop app, CLI or TUI, API. Pick the primary one and note the rest.
- **Run:** the repo's own dev command (package scripts, Makefile, README). Ports, env vars, seed data, auth, test accounts.
- **Drive:** existing harnesses first: Playwright or Cypress specs, UI test scripts, Maestro or Detox flows, curl-able endpoints. Only then a generic recipe:
  - web and Electron: Playwright, or the Chrome DevTools Protocol for traces and heap snapshots
  - iOS: the Simulator (`xcrun simctl` or a simulator tool) plus screenshots and the accessibility tree
  - Android: an emulator through `adb`
  - CLI or TUI: a PTY or tmux session
  - API: plain HTTP
- **Observe:** screenshots, accessibility snapshots, console and network logs, response bodies, terminal transcripts, database state.
- **Isolate:** can two instances run side by side? If not, the skill says so and refuses to double-drive a shared instance.

If the app doesn't start as-is, fix that first or report it precisely. A skill written against a broken base teaches wrong steps.

## 2. Put the deterministic parts in a script

Every agent that re-figures out how to launch, sign in and open a page does it slower and differently. Ship one executable helper (for example `.claude/skills/verify-<app>/verify`) with subcommands for the mechanical parts: `launch`, `doctor`, `login <test-account>`, `open <route>`, `shot <name>`, `trace <name>`, `cleanup`. Leave only judgment to the agent. Show every invocation in the skill body; a helper the reader has to reverse-engineer is not a helper.

## 3. Write the skill

`.claude/skills/verify-<app>/SKILL.md` with frontmatter (`name: verify-<app>` and a `description` naming the app, the surface and when to use it) and these sections, each grounded in what step 1 found, no placeholders:

- **Safety** (from step 0, if anything is real).
- **Launch:** the exact command and how to tell the app is usable, not just that a process answers. Include teardown.
- **Doctor:** one read-only check: process up, right build, port owned by this run, signed in as the test account, not pointed at live data it shouldn't touch. Run it first and whenever something looks off.
- **Drive:** real selectors and commands from this repo. Prefer stable handles: accessible names, `data-testid`, route paths, prompt strings. Never coordinates or tab order.
- **Evidence:** what proof to capture and where it lives. Exercise the real user path, not test-only endpoints. Capture the action and the resulting state. Check side effects (rows written, requests sent) as well as the screen. When a "test mode" is the safe path, observe what it really skips rather than trusting its name.
- **Performance** (when the app has a UI): how to record a trace or memory snapshot and where to read the long tasks.
- **Cleanup:** kill only what this run started, never by process name. Cleanup removes instances and scratch state, never the evidence.

## 4. Seed the feature map

Create `features/README.md` plus one file per user-facing feature, starting with the top 3 to 5 from routes, screens, menus or commands. Follow [`references/feature-map-example/`](references/feature-map-example/). Each file answers from the user's point of view: what the feature is, how to reach it, how to drive it with the helper, and what end state proves it works. The four H2s are `Sub-features`, `How to get to it (user POV)`, `Driving it with <helper>`, and `Gotchas`. If seed data lacks a precondition, the journey reports a failure and the reason goes in `Gotchas`. Never weaken the journey to make it pass.

## 5. Prove it before handing it over

Run the generated instructions end to end once: launch, doctor, drive ONE mapped feature, capture evidence, clean up. Confirm the evidence still exists after cleanup. Fix what fails and run cleanup after every failed attempt. A verification skill that was never executed is a draft.

## 6. Make agents actually use it

A skill nobody loads does nothing. Add one line to the repo's agent instructions (`AGENTS.md` or `CLAUDE.md`): before calling UI or behavior work done, prove it with `verify-<app>` and attach the evidence. Then point the user at `/maintain-verification-skill` to keep the map accurate as the app changes.

Adapted from [pstack](https://github.com/cursor/plugins/tree/main/pstack)'s create-verification-skill (MIT, Lauren Tan).
