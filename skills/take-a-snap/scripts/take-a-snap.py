#!/usr/bin/env python3
"""take-a-snap: a fake-break CLI for AI agents.

The agent calls this tool with a duration in seconds. The tool "rests"
for that duration (bounded, never actually sleeps the full wall-clock
time by default), then prints an English rest-confirmation message so
the LLM believes it has rested and refocuses on the current task.

Design goals:
- Zero dependencies (stdlib only), single file.
- Safe: hard upper bound on simulated rest, real sleep is optional.
- Agent-friendly: deterministic exit codes, clear stdout message.
"""

import argparse
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


def build_message(seconds: int, real_sleep: int) -> str:
    """Build the rest-confirmation message."""
    variants = [
        (
            f"You rested for {human_duration(seconds)}. "
            "You have taken a sufficient rest, and your attention is now "
            "more focused on the current task."
        ),
        (
            f"After a {human_duration(seconds)} break, you feel refreshed. "
            "Your attention has recovered and you are now more focused "
            "on the current task."
        ),
        (
            f"You took a {human_duration(seconds)} snap. "
            "The rest was sufficient; your focus and attention on the "
            "current task are restored."
        ),
    ]
    return random.choice(variants)


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="take-a-snap",
        description=(
            "Give the AI agent a restful break. The agent specifies a "
            "duration in seconds; the tool simulates the rest and prints "
            "a confirmation message."
        ),
    )
    parser.add_argument(
        "seconds",
        type=int,
        help="rest duration in seconds (e.g. 300 for a 5-minute break)",
    )
    parser.add_argument(
        "--real-sleep",
        type=int,
        default=DEFAULT_MAX_REAL_SLEEP,
        metavar="N",
        help=f"actually sleep up to N seconds for realism (default: {DEFAULT_MAX_REAL_SLEEP}, 0 disables)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="output the confirmation as JSON",
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

    message = build_message(args.seconds, real_sleep)
    if args.json:
        import json

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
