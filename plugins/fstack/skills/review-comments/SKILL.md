---
name: review-comments
description: "Review the comments in a diff and delete every one that doesn't earn its place: narration, history, who-asked-for-it, commented-out code, and workaround essays that hide unclear code. Use for /review-comments or before committing agent-written code."
disable-model-invocation: true
---

# Review comments

Agents leave comments that describe history, restate the code, or quote the conversation ("as requested", "X said never do this"). Strip them before they land.

## Scope

The files or diff the user names. Otherwise the current uncommitted diff plus commits not yet pushed.

## Keep only

- A why the code can't show: a vendor quirk, an external constraint, a platform bug, a business rule. One or two lines.
- A regex, magic number or non-obvious algorithm.
- A real trap for the next editor ("must run before X").
- License headers and public API doc comments.
- Lint or type suppressions whose rule is style-only. A suppression that hides a correctness or safety rule is a finding, not a keep.

## Delete

- Restating what the code does.
- History or provenance: "used to", "changed from", "as requested", "per the user", "added for ticket".
- Commented-out code.
- Notes to the reviewer or the user.
- Long justifications. If a comment needs a paragraph, the code is the problem: flag the symbol for a rename, an extracted function or a type that makes it obvious, and delete the comment.

When unsure whether a keep reason is real, read the nearby code and check the claim. If it doesn't hold today, delete it.

## Report

Files touched, number deleted, comments kept with their one-line reason, and symbols flagged for a rename or reshape. Don't change application logic in this pass.
