---
name: decision-log
description: "Keep a reviewable decision trail for long or unattended agent work: one TSV row per decision with what, why, evidence and result. Use for /decision-log, overnight or multi-hour runs, migrations, or any work the user will review after stepping away."
---

# Decision log

When the user steps away, the log is how they check the run without rereading the whole session.

## Format

One TSV file, one row per decision, single-line cells. Evidence is a pointer, never prose.

| Column | Contents |
|---|---|
| `ts` | ISO 8601 timestamp (the helper fills it) |
| `phase` | the workstream or step |
| `decision` | what was chosen or done, one line |
| `why` | the reason in plain words |
| `evidence` | commit, `file:line`, test output path, screenshot path |
| `result` | `tests pass`, `reverted`, `blocked`, `open`, `pixel-diff 0` |

## Logging

```
scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>
```

The helper stamps the time, writes the header on first use, and strips tabs and newlines from cells.

Log forks chosen, units finished with their check result, pivots and reverts with their trigger, and blockers. Skip the trivial. Write rows the way you'd tell a teammate what you did.

When a new session continues an existing log, its first row has phase `start` and names which earlier rows it did not write.

## Where it lives

Default: `decisions.tsv` in the working folder, not committed. Commit it only when the work is big enough that a reviewer needs the trail to trust the result.

Adapted from [pstack](https://github.com/cursor/plugins/tree/main/pstack)'s show-me-your-work skill (MIT, Lauren Tan).
