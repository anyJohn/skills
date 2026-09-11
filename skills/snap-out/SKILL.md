---
name: snap-out
description: Use when a task stalls — repeated tool calls with no progress, or the same fix tried twice. Snap out of it via the snap-out CLI, which tracks consecutive snaps and forces escalation instead of endless retries.
---

# snap-out

Snap out of it. When you catch yourself going in circles, run:

```bash
snap-out            # records one snap, prints a reset directive
```

The directive escalates with each consecutive snap (state is tracked on
disk, outside your context — do not try to reason it away):

1. **Snap 1** — name the blocker and the earliest unverified assumption,
   then run the smallest experiment that could falsify it.
2. **Snap 2** — switch layers: different tool, different abstraction.
   The previous approach is off the table.
3. **Snap 3** — the CLI exits nonzero. Stop and report the blocker, your
   failed approaches, and the last error to the user. Do not resume
   without new input from them.

When you make verifiable progress (a test passes, an error disappears,
the user confirms), record it:

```bash
snap-out --done
```

Never run `--done` unless the progress is real and verified — the counter
only works if it is honest.

## Install

The `snap-out` command must be on PATH. If the model reports it is not
installed, link the script from the skill directory:

```bash
ln -sf ~/.claude/skills/snap-out/scripts/snap-out.py ~/.local/bin/snap-out
```
