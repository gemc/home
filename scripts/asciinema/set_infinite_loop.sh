#!/usr/bin/env bash
# Sets a GIF to loop infinitely. Modifies the file in-place (no re-encode).
# Install gifsicle: brew install gifsicle
#
# Usage:   ./set_infinite_loop.sh <gif_name>
# Example: ./set_infinite_loop.sh simple_flux_full
#
# Accepts bare name (simple_flux_full), name with extension (.gif),
# or an absolute path.

set -euo pipefail

GIF_NAME="${1:?Usage: set_infinite_loop.sh <gif_name>}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

if ! command -v gifsicle &>/dev/null; then
    echo "Error: 'gifsicle' not found. Install with: brew install gifsicle" >&2
    exit 1
fi

if [[ "$GIF_NAME" = /* ]]; then
    GIF_FILE="$GIF_NAME"
elif [[ "$GIF_NAME" == *.gif ]]; then
    GIF_FILE="$REPO_ROOT/$GIF_NAME"
else
    GIF_FILE="$REPO_ROOT/${GIF_NAME}.gif"
fi

[[ -f "$GIF_FILE" ]] || { echo "Error: $GIF_FILE not found" >&2; exit 1; }

TMPFILE=$(mktemp "${GIF_FILE}.XXXXXX")
trap 'rm -f "$TMPFILE"' EXIT

echo "Input:  $GIF_FILE"
gifsicle --loopcount=0 "$GIF_FILE" -o "$TMPFILE"
mv "$TMPFILE" "$GIF_FILE"
echo "Done: infinite loop set."
