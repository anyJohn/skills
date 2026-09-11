---
name: take-a-snap
description: Use when working on a long task and progress stalls — repeated tool calls with no advance, errors that should have been caught earlier, or the same fix attempted twice. Run the take-a-snap checkpoint ritual, then continue with a fresh approach rather than repeating the failed one.
---

# Take a Snap: checkpoint and reset

When an agent stalls, the cause is almost never "tiredness" — it is stale
context: a wrong assumption made early, an error message that polluted later
reasoning, or a loop of near-identical attempts. Reading a message that says
"you are rested now" does not fix any of that. What fixes it is an explicit
checkpoint and a deliberate change of approach.

This skill enforces that ritual in two phases.

## When to trigger

Any of these, judged honestly:
- 2+ consecutive tool calls that each look like a retry of the previous one;
- the same error appears twice and you attempted "the same fix" both times;
- you are about to run a tool call whose result you can already predict
  (a sign you are executing on rails, not thinking);
- several small errors slipped through that a careful first attempt
  would have caught.

Do NOT trigger after context compaction — compaction already clears stale
context; instead spend one turn re-reading the summary and re-deriving the
plan from it.

## Phase 1 — checkpoint (mandatory, before running the CLI)

Write out, in your reply, three short lines:

```
CHECKPOINT
done:      <what is verifiably complete, e.g. "tests 3/7 pass">
blocker:   <the exact failure, with the last real error message quoted>
assumption to re-examine: <the earliest assumption still unverified>
```

If you cannot fill in the "blocker" line with a concrete error or
observation, you are not stalled — stop the ritual and just continue working.

## Phase 2 — snap and reset

1. Run the CLI sized to severity:
   - first stall on this task: `take-a-snap 60`
   - repeated stalls / two failed approaches: `take-a-snap 300`
   - after any of them fires twice in one task: `take-a-snap 900`
2. The CLI prints a reset directive. Read it — it names what you must
   change, not how rested you are.
3. Resume by attacking the **assumption** named in your checkpoint:
   - try the smallest experiment that could falsify it;
   - or pick a materially different approach (different tool, different
     layer of the stack, different search terms) — not the same call with
     tweaked arguments.
4. If two full snaps (Phase 1 + Phase 2) do not unblock the task, stop and
   report the blocker to the user instead of snapping a third time. Escalate
   rather than loop.

## Rules

- Never run the CLI without completing Phase 1 first — a reset without a
  written checkpoint resets nothing.
- Never exceed 3600 simulated seconds (the CLI enforces this).
- Real sleep is capped at 5 seconds; keep `--real-sleep` at its default —
  the value of this skill is the checkpoint, not the waiting.
- Nothing about task state changes across a snap; your checkpoint text is
  the only continuity.
