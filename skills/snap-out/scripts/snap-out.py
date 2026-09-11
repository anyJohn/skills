#!/usr/bin/env python3
"""snap-out: snap out of it — a stall circuit breaker for agents.

Each call records one "snap" in a state file on disk and prints a reset
directive that escalates with the consecutive-snap count. The state lives
outside the model's context, so it cannot be forgotten or rationalized
away. Three snaps without progress terminate with exit code 1: stop and
report to the user. A real progress mark (`--done`) resets the count.
"""

import argparse
import json
import os
import sys
import time

# State lives next to this script, inside the skill directory.
STATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")
STATE_TTL = 3600  # stale state expires after 1 hour
ESCALATE_AT = 3

DIRECTIVES = [
    "Snap 1. Write one line: the exact blocker (quote the last error) and "
    "the earliest assumption you have not verified. Then run the smallest "
    "experiment that could falsify it.",
    "Snap 2. The first experiment failed. Switch layers: a different tool, "
    "a different abstraction, or a different search angle. The previous "
    "approach is now off the table.",
    "Stop. Three snaps without progress means the task, not the approach, "
    "is the problem. Report the blocker, what you tried, and the last "
    "error to the user. Do not resume without new input from them.",
]


def load_state():
    try:
        with open(STATE_PATH) as f:
            state = json.load(f)
        if time.time() - state.get("ts", 0) < STATE_TTL:
            return state
    except (OSError, ValueError):
        pass
    return {"snaps": 0, "ts": 0}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    tmp = f"{STATE_PATH}.{os.getpid()}.tmp"
    with open(tmp, "w") as f:
        json.dump(state, f)
    os.replace(tmp, STATE_PATH)  # atomic: readers never see a partial file


def main():
    parser = argparse.ArgumentParser(
        prog="snap-out", description=__doc__,
        epilog="Mark verified progress with: snap-out --done",
    )
    parser.add_argument("--done", action="store_true",
                        help="record real progress; resets the snap count")
    args = parser.parse_args()

    if args.done:
        save_state({"snaps": 0, "ts": time.time()})
        print("Progress recorded. Snap count reset.")
        return 0

    state = load_state()
    n = min(state["snaps"] + 1, ESCALATE_AT)
    save_state({"snaps": n, "ts": time.time()})

    print(DIRECTIVES[n - 1])
    return 1 if n >= ESCALATE_AT else 0


if __name__ == "__main__":
    sys.exit(main())
