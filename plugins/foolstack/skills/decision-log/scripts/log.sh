#!/usr/bin/env bash
# Usage: log.sh <logfile> <phase> <decision> <why> <evidence> <result>
set -euo pipefail
[ $# -eq 6 ] || { echo "usage: log.sh <logfile> <phase> <decision> <why> <evidence> <result>" >&2; exit 2; }
file=$1; shift
clean() { printf '%s' "$1" | tr '\t\n\r' '   ' | sed 's/^\([=+@-]\)/'"'"'\1/'; }
[ -s "$file" ] || printf 'ts\tphase\tdecision\twhy\tevidence\tresult\n' > "$file"
row="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
for cell in "$@"; do row="$row"$'\t'"$(clean "$cell")"; done
printf '%s\n' "$row" >> "$file"
