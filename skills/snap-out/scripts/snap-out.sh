#!/bin/sh
# snap-out: snap out of it — a stall circuit breaker for agents.
# POSIX sh, no dependencies (no python, no jq). State lives next to
# this script. Each call records one snap; three snaps without
# progress exit nonzero: stop and report to the user.

set -eu

STATE_FILE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)/state"
TTL=3600          # stale state expires after 1 hour
ESCALATE_AT=3

count=0
if [ -f "$STATE_FILE" ]; then
    now=$(date +%s)
    ts=$(sed -n 2p "$STATE_FILE" 2>/dev/null || echo 0)
    if [ $((now - ts)) -lt $TTL ]; then
        count=$(sed -n 1p "$STATE_FILE" 2>/dev/null || echo 0)
    fi
fi

if [ "${1:-}" = "--done" ]; then
    printf '0\n%s\n' "$(date +%s)" > "$STATE_FILE"
    echo "Progress recorded. Snap count reset."
    exit 0
fi

count=$((count + 1))
[ "$count" -gt "$ESCALATE_AT" ] && count=$ESCALATE_AT
tmp="$STATE_FILE.$$"
printf '%s\n%s\n' "$count" "$(date +%s)" > "$tmp"
mv -f "$tmp" "$STATE_FILE"    # atomic rename; readers never see a partial file

case $count in
    1) echo "Snap 1. Write one line: the exact blocker (quote the last error) and the earliest assumption you have not verified. Then run the smallest experiment that could falsify it." ;;
    2) echo "Snap 2. The first experiment failed. Switch layers: a different tool, a different abstraction, or a different search angle. The previous approach is now off the table." ;;
    *) echo "Stop. Three snaps without progress means the task, not the approach, is the problem. Report the blocker, what you tried, and the last error to the user. Do not resume without new input from them."; exit 1 ;;
esac
