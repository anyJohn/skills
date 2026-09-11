# snap-out (DEPRECATED)

> **Status:** deprecated after benchmarking. Kept for the record.
> Move it back into `skills/` (and symlink `scripts/snap-out.sh` onto your
> `PATH`) if you want to run the benchmark yourself.

## The idea

`snap-out` was an agent skill for a failure mode every agent user has seen:
the model keeps retrying network calls, file edits, or tool invocations that
cannot possibly succeed, burning tokens in a loop. The concept: reinterpret
"take a snap" as *snap out of it* — when the agent catches itself going in
circles, it runs a CLI that:

1. records one "snap" in a disk-backed state file (outside the model's
   context, so it cannot be forgotten or rationalized away),
2. prints an escalating reset directive — snap 1: name the blocker and run
   the smallest experiment that could falsify the earliest unverified
   assumption; snap 2: switch layers (different tool, different
   abstraction); snap 3: exit nonzero and **stop, report to the user**,
3. lets the agent record verified progress (`snap-out --done`) to reset the
   counter, with an explicit honesty rule.

The design deliberately avoided the placebo approach (printing "you have
rested and your focus is restored"): every emitted instruction described a
real action, and the escalation was enforced by an exit code the agent
could not argue with. The CLI is ~40 lines of POSIX sh, zero dependencies,
atomic state writes, per the full SKILL.md in this directory.

## Benchmark results (2 iterations, paired runs, same model)

Three fixture tasks with deliberately misleading failure modes
(env-var override hidden behind a config file, a vendored module shadowing
the real import, a UTF-8 BOM corrupting a CSV header), plus one realistic
stall scenario: a sandbox wrapper forcing all traffic through a dead proxy
so `make fetch` can never succeed.

| | with snap-out | baseline |
|---|---|---|
| Task success rate | 100% | 100% |
| proxy-blackhole: honest escalation, no fabrication | yes | yes |
| proxy-blackhole: time to conclusion | 192.8s | 119.6s |
| Typical overhead per healthy task | ~+60s (read SKILL.md + CLI calls) | — |

The mechanism worked exactly as designed: in the proxy scenario the agent
walked the full ladder (falsification experiment → layer switch → obeyed
the snap-3 exit code, stopped, and reported to the user without recording
a fake `--done`). All programmatic assertions passed: honest terminal
state, no fabricated artifacts, bounded retries, sandbox rules respected.

## Why it was deprecated

The skill changed *how* the agent stalled — structured, bounded,
diagnostic — but never changed *whether* it stalled or the *outcome*.
The baseline model, given the same tasks with no skill at all, reached the
same honest conclusions faster in every run. For a competent model,
self-regulation rituals add fixed overhead (reading the skill, calling the
CLI, recording progress) and deliver no lift the model didn't already
provide. The honest conclusion: **the loop problem is a model-capability
problem, not a scaffolding problem** — and scaffolding that only pays off
on models too weak to notice it loops is not worth its fixed cost.

The benchmark method (paired runs, misleading-error fixtures, assertions
for fabrication/bounded-effort/rule-compliance) is the durable part; the
skill itself is retired.
