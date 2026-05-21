#!/usr/bin/env bash
# Converts a .mov (or any video) to a GIF using ffmpeg two-pass palette.
# Install ffmpeg: brew install ffmpeg
#
# Usage:   ./mov_to_gif.sh <input.mov> [output_name] [width]
# Example: ./mov_to_gif.sh screen_demo.mov screen_demo 800
#
# [output_name]  basename without extension (default: input basename)
# [width]        resize width in pixels, height auto-scales (default: original size)
#
# Env overrides: GIF_FPS, GIF_WIDTH

set -euo pipefail

MOV_FILE="${1:?Usage: mov_to_gif.sh <input.mov> [output_name] [width]}"
OUTPUT_NAME="${2:-$(basename "${MOV_FILE%.*}")}"
CLI_WIDTH="${3:-}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

GIF_FPS="${GIF_FPS:-20}"
GIF_WIDTH="${GIF_WIDTH:-}"
[[ -n "$CLI_WIDTH" ]] && GIF_WIDTH="$CLI_WIDTH"

if ! command -v ffmpeg &>/dev/null; then
    echo "Error: 'ffmpeg' not found. Install with: brew install ffmpeg" >&2
    exit 1
fi

if [[ ! -f "$MOV_FILE" ]]; then
    echo "Error: $MOV_FILE not found" >&2
    exit 1
fi

GIF_FILE="$REPO_ROOT/${OUTPUT_NAME}.gif"
WORKDIR=$(mktemp -d)
trap 'rm -rf "$WORKDIR"' EXIT
PALETTE="$WORKDIR/palette.png"

SCALE=""
[[ -n "$GIF_WIDTH" ]] && SCALE="scale=${GIF_WIDTH}:-1:flags=lanczos,"

echo "Input:  $MOV_FILE"
echo "Output: $GIF_FILE"
[[ -n "$GIF_WIDTH" ]] && echo "Width:  ${GIF_WIDTH}px"
echo "FPS:    ${GIF_FPS}"
echo ""

# Pass 1: build palette from all frames
ffmpeg -y -i "$MOV_FILE" \
    -vf "${SCALE}fps=${GIF_FPS},palettegen=stats_mode=diff" \
    "$PALETTE" -loglevel warning

# Pass 2: render GIF using palette
ffmpeg -y -i "$MOV_FILE" -i "$PALETTE" \
    -lavfi "${SCALE}fps=${GIF_FPS}[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle" \
    "$GIF_FILE" -loglevel warning

echo "Done: $GIF_FILE"
