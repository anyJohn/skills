#!/usr/bin/env python3
"""take-a-snap: actually nap for a bit. Real sleep, capped."""

import argparse
import sys
import time

MAX_SECONDS = 600

parser = argparse.ArgumentParser(prog="take-a-snap", description=__doc__)
parser.add_argument("seconds", type=int, help="how long to nap, in seconds (60-180 recommended)")
args = parser.parse_args()

if args.seconds <= 0:
    parser.error("seconds must be a positive integer")
if args.seconds > MAX_SECONDS:
    print(f"error: capped at {MAX_SECONDS} seconds", file=sys.stderr)
    sys.exit(2)

time.sleep(args.seconds)
print(f"Napped {args.seconds}s. Resume with a different approach — not a retry of the last call.")
