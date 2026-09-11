---
name: take-a-snap
description: Use when a task stalls — repeated tool calls with no progress, or the same fix tried twice. Take a real short nap, then resume with a different approach instead of retrying.
---

# take-a-snap

When you are going in circles, stop and actually pause:

```bash
take-a-snap 90    # seconds; 60–180 is a good range, hard cap 600
```

The command really sleeps that long. Do not use it as a no-op.

Before napping, write one line stating the assumption you will re-examine
afterwards. After waking, try a materially different approach — never the
same call with tweaked arguments. If a second nap doesn't unblock you,
report the blocker to the user instead of napping again.
