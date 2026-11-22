---
name: blast-radius
description: "Find what a change could break outside its own diff before it ships, and prove the one fact it's safe because of by running real code instead of writing it up. Use for /blast-radius, \"what could this break\", or before shipping a change to money, auth, data, migrations or anything shared."
---

# Blast radius

Listing callers is not the job; grep does that in a second. The job is the breakage grep won't show.

## Don't trust your own writeup

A writeup that sounds right reads exactly the same whether or not it's true. Find the one or two facts the change's safety depends on and push each as far down this ladder as is cheap. Say where it stopped.

1. You said so. Worthless on its own.
2. You pointed at the line: a real `file:line`, or the library's own source.
3. You walked the failure step by step and showed it can't reach.
4. You ran it: a small script or test that calls the real code and fails loudly if you're wrong.
5. You reproduced it in the running app (use the repo's `verify-<app>` skill if it has one).

## Steps

1. **Read the change.** The diff, the symbols it adds, changes and deletes, and what it now does differently, including what the diff doesn't spell out.
2. **Find the one fact it's safe because of.** Most risky-looking changes are safe because of a single fact ("this only drops cache entries that are already dead"). Spend your time here, not on a long list of maybes.
3. **Look where grep stops.** The source of the library you call, at its pinned version. When things run: async ordering, teardown, retries, cron overlap, webhook redelivery. What a symbol search misses: JSON an API returns, a database column, a wire format, a feature flag, another service reading the same rows, a cached page.
4. **Be honest about each risk.** Real chance, real cost. Keep confirmed risks; list checked-and-cleared ones separately. Cite real lines. "Searched and found nothing" is an answer. Never invent a caller or an API.
5. **Prove the one fact.** Write the script or test, run it, paste what happened.

## Hand back

- **What it does,** including the part that isn't obvious.
- **The one fact it's safe because of,** the ladder step reached, and the proof, or "unproven".
- **Risks:** how it breaks, `file:line`, likelihood and cost, how to check.
- **Cleared:** what you checked and why it's fine.
- **Before you ship:** the cheapest test or repro that would catch the real bug, including the script you wrote.

Adapted from [pstack](https://github.com/cursor/plugins/tree/main/pstack)'s blast-radius skill (MIT, Lauren Tan).
