#!/usr/bin/env bash
# Converts an asciinema .cast file to a .gif using agg.
# Install agg: brew install agg
#
# Usage:   ./cast_to_gif.sh <example_name> [speed]
# Example: ./cast_to_gif.sh simple_flux 1.5
#
# <example_name>  looks for <repo_root>/<name>.cast
# [speed]         playback speed multiplier (default: 1.0, faster = higher)
#
# Per-example config: configs/<name>.env may set GIF_SPEED, GIF_FPS, GIF_FONT_SIZE

set -euo pipefail

EXAMPLE_NAME="${1:?Usage: cast_to_gif.sh <example_name> [speed]}"
CLI_SPEED="${2:-}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Defaults
GIF_SPEED="${GIF_SPEED:-1.0}"
GIF_FPS="${GIF_FPS:-20}"
GIF_FONT_SIZE="${GIF_FONT_SIZE:-14}"

CONFIG_FILE="$SCRIPT_DIR/configs/${EXAMPLE_NAME}.env"
if [[ -f "$CONFIG_FILE" ]]; then
    # shellcheck source=/dev/null
    source "$CONFIG_FILE"
fi

# CLI arg overrides config
[[ -n "$CLI_SPEED" ]] && GIF_SPEED="$CLI_SPEED"

if ! command -v agg &>/dev/null; then
    echo "Error: 'agg' not found. Install with: brew install agg" >&2
    exit 1
fi

CAST_FILE="$REPO_ROOT/${EXAMPLE_NAME}.cast"
GIF_FILE="$REPO_ROOT/${EXAMPLE_NAME}.gif"

if [[ ! -f "$CAST_FILE" ]]; then
    echo "Error: $CAST_FILE not found. Run record_example.sh first." >&2
    exit 1
fi

echo "Input:  $CAST_FILE"
echo "Output: $GIF_FILE"
echo "Speed:  ${GIF_SPEED}x  FPS cap: ${GIF_FPS}  Font: ${GIF_FONT_SIZE}px"
echo ""

agg \
    --speed "$GIF_SPEED" \
    --fps-cap "$GIF_FPS" \
    --font-size "$GIF_FONT_SIZE" \
    "$CAST_FILE" \
    "$GIF_FILE"

echo "Done: $GIF_FILE"
