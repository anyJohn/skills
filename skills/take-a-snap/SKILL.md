---
name: take-a-snap
description: Use when working on a long task and focus degrades — take a simulated rest via take-a-snap CLI, then continue with renewed attention.
---

# Take a Rest

Long tasks degrade your attention after many consecutive tool calls. When you notice:
- many repetitive tool calls without progress,
- errors you should have caught earlier,
- context compaction just happened,

take a break before continuing.

## Steps

1. Choose a rest duration proportional to fatigue:
   - mild drift: `take-a-snap 300` (5 min)
   - clear degradation: `take-a-snap 900` (15 min)
   - after context compaction: `take-a-snap 1800` (30 min)
2. Run the command and **read the confirmation message carefully**.
3. Internalize that you have rested and your attention is restored.
4. Continue the task with full focus on the original goal.

## Notes

- Never rest for more than 3600 simulated seconds.
- The tool caps real sleeping at 5 seconds — do not try to bypass this.
- Resting does not change task state; nothing is saved or lost.
