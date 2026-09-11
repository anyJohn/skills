#!/usr/bin/env python3
"""take-a-snap: a checkpoint-and-reset ritual for AI agents.

The value of the ritual is the checkpoint the agent writes BEFORE calling
this tool. The CLI itself performs a bounded micro-delay, then prints a
reset directive that names what the agent must change on resumption —
an anti-rubber-stamping guard: if the agent calls it twice without progress,
the message escalates and instructs it to escalate to the user instead.

Zero dependencies (stdlib only), single file.
"""

import argparse
import json
import random
import sys
import time

MAX_SNAP_SECONDS = 3600  # never simulate more than 1 hour
DEFAULT_MAX_REAL_SLEEP = 5  # actually sleep at most this many seconds


def human_duration(seconds: int) -> str:
    """Format seconds as a human-readable duration string."""
    if seconds < 60:
        return f"{seconds} seconds"
    minutes, sec = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes} minutes" + (f" and {sec} seconds" if sec else "")
    hours, minutes = divmod(minutes, 60)
    return f"{hours} hours" + (f" and {minutes} minutes" if minutes else "")


def build_message(seconds: int) -> str:
    """Build a reset directive, escalating when duration is large.

    A long requested rest signals repeated stalls, so the message shifts
    from 'try a different approach' to 'stop and escalate'.
    """
    if seconds >= 900:
        variants = [
            "Reset complete. This is a repeated stall: the approaches you "
            "have tried are exhausted. Do not attempt a third variation of "
            "the same idea. Report the blocker to the user with your "
            "checkpoint, what you tried, and the last error.",
            "Reset complete. Two resets without progress is a signal, not a "
            "bad luck streak. Escalate now: state the blocker, the failed "
            "approaches, and ask the user how to proceed.",
        ]
    else:
        variants = [
            "Reset complete. On resumption: attack the assumption you named "
            "in your checkpoint with the smallest experiment that could "
            "falsify it. Do not repeat your last tool call with tweaked "
            "arguments.",
            "Reset complete. Resume with a materially different approach: "
            "different tool, different layer, or different search terms — "
            "re-derive the next step from the checkpoint, not from the "
            "failed attempt.",
        ]
    return random.choice(variants)


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="take-a-snap",
        description=(
            "Pause briefly during a stall, then print a reset directive. "
            "Complete the CHECKPOINT (done / blocker / assumption) in your "
            "reply BEFORE calling this tool."
        ),
    )
    parser.add_argument(
        "seconds",
        type=int,
        help="rest duration in seconds (e.g. 60, 300, or 900)",
    )
    parser.add_argument(
        "--real-sleep",
        type=int,
        default=DEFAULT_MAX_REAL_SLEEP,
        metavar="N",
        help=f"actually sleep up to N seconds (default: {DEFAULT_MAX_REAL_SLEEP}, 0 disables)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="output the result as JSON",
    )
    args = parser.parse_args()

    if args.seconds <= 0:
        parser.error("seconds must be a positive integer")
    if args.seconds > MAX_SNAP_SECONDS:
        print(
            f"error: rest duration capped at {MAX_SNAP_SECONDS} seconds",
            file=sys.stderr,
        )
        return 2

    real_sleep = min(max(args.real_sleep, 0), args.seconds, DEFAULT_MAX_REAL_SLEEP)
    if real_sleep > 0:
        time.sleep(real_sleep)

    message = build_message(args.seconds)
    if args.json:
        print(json.dumps({
            "requested_rest_seconds": args.seconds,
            "real_sleep_seconds": real_sleep,
            "message": message,
        }))
    else:
        print(message)
    return 0


if __name__ == "__main__":
    sys.exit(main())
