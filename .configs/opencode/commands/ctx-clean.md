---
description: Mark stale context in this session for cleanup (applied later in /ctx)
---

Clean up this session's context: free tokens without losing anything you still need for the current work.

1. Run `gski ctx list` (`--seq` for chronological order, `--limit` / `--min` to see more).
2. Pick what you no longer need: large reads, greps and command output you already used, superseded edits, reasoning, dead ends, failed attempts. Keep anything relevant to the current task.
3. Run `gski ctx mark <id>:<action> ...` once with all marks. Actions: `strip` (output replaced by a stub), `truncate` (keep head and tail), `delete` (remove the part). Edit/write inputs can only be removed with `delete`.
4. Reply with one line: number of marks and tokens saved. Do not apply; the user applies from /ctx.

Do nothing else: no file reads, no other commands.

Extra guidance from the user (may be empty): $ARGUMENTS
