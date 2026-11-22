---
name: maintain-verification-skill
description: "Keep a project's verification skill and feature map accurate as the app changes: read each feature from source, drive every feature live, and ship one change of proven corrections. Use for /maintain-verification-skill or when a verify-<app> skill's steps have stopped matching the app."
disable-model-invocation: true
---

# Maintain a verification skill

A feature map goes stale the moment the app changes. This is the upkeep pass for a `verify-<app>` skill made by `/create-verification-skill`. The unit of rigor is the feature: every feature file gets read against source and driven live once.

## Outcome

End with exactly one, and say which:
- **clean:** every feature covered from source and live; nothing to change.
- **changed:** one commit or PR (per the repo's convention) of proven corrections to the skill.
- **blocked:** coverage could not finish or a fix could not ship safely. Say exactly what blocked it.

## Edit scope

Edit only the verification skill's own folder: its SKILL.md, `features/` and helper scripts. Never edit product code in this pass. Behavior the map describes that the app no longer does is either map drift (fix the map) or a product regression (report it to the user, don't paper over it in the docs). The skill's Safety section binds this pass too.

## Pass

1. **Locate.** Find the `verify-*` skill under `.claude/skills/`. Several: ask which. None: stop and point at `/create-verification-skill`.
2. **Index.** Read `features/README.md` and list its sibling files. Fix missing, extra, duplicate or dead entries.
3. **Source wave.** One read-only subagent per feature file, run in parallel. Each explains how the feature works from source, flags likely drift with file citations, and returns one live recipe. Subagents never drive the app or edit files.
4. **Reconcile.** Merge overlapping recipes into as few app states as practical. Spot-check cited drift. Sweep recent commits for user-facing screens missing from the map; require a concrete source path before calling one missing.
5. **Live pass.** Required even when source looks clean. You drive, serially, following the skill's own Launch model. Run doctor before the first drive and again after any failed drive. Evidence captured so far survives every cleanup. Nothing a drive started outlives the run. A feature that can't be reached is "unreachable" only with the concrete prerequisite (auth, entitlement, device, external state) and the route tried; if the map omits that prerequisite, that is drift.
6. **Triage.** Wrong user-POV description: fix the map. Working behavior the helper can't drive: fix the helper and re-drive it live. Actually broken app behavior: report it, keep it out of this change.
7. **Ship or stop.** For changed, re-read every changed file and ship one change. For clean or blocked, report the outcome and coverage honestly.

Adapted from [pstack](https://github.com/cursor/plugins/tree/main/pstack)'s maintain-verification-skill (MIT, Lauren Tan).
