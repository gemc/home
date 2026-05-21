#!/usr/bin/env bash
# Trims a GIF to a maximum duration using ffmpeg two-pass palette.
# Install ffmpeg: brew install ffmpeg
#
# Usage:   ./trim_gif.sh <gif_name> <seconds> [output_name]
# Example: ./trim_gif.sh simple_flux_full 10 simple_flux_trimmed
#
# If output_name is omitted the input file is overwritten.

set -euo pipefail

GIF_NAME="${1:?Usage: trim_gif.sh <gif_name> <seconds> [output_name]}"
SECONDS_MAX="${2:?Usage: trim_gif.sh <gif_name> <seconds> [output_name]}"
OUTPUT_NAME="${3:-}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

GIF_FPS="${GIF_FPS:-20}"

if ! command -v ffmpeg &>/dev/null; then
    echo "Error: 'ffmpeg' not found. Install with: brew install ffmpeg" >&2
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

if [[ -z "$OUTPUT_NAME" ]]; then
    OUTPUT_FILE="$GIF_FILE"
else
    OUTPUT_FILE="$REPO_ROOT/${OUTPUT_NAME}.gif"
fi

WORKDIR=$(mktemp -d)
trap 'rm -rf "$WORKDIR"' EXIT
PALETTE="$WORKDIR/palette.png"
TMPOUT="$WORKDIR/trimmed.gif"

echo "Input:    $GIF_FILE"
echo "Trim to:  ${SECONDS_MAX}s"
echo "Output:   $OUTPUT_FILE"
echo ""

# Pass 1: palette from the trimmed stream
ffmpeg -y -nostdin -i "$GIF_FILE" -t "$SECONDS_MAX" \
    -vf "fps=${GIF_FPS},palettegen=stats_mode=diff" \
    "$PALETTE" -loglevel warning

# Pass 2: render trimmed GIF with palette
ffmpeg -y -nostdin -i "$GIF_FILE" -i "$PALETTE" -t "$SECONDS_MAX" \
    -lavfi "fps=${GIF_FPS}[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle" \
    "$TMPOUT" -loglevel warning

mv "$TMPOUT" "$OUTPUT_FILE"
echo "Done: $OUTPUT_FILE"
