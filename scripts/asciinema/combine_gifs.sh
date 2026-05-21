#!/usr/bin/env bash
# Concatenates two GIFs (plays first then second) with optional resize.
# Install ffmpeg: brew install ffmpeg
#
# Usage:   ./combine_gifs.sh <gif1> <gif2> [output_name] [width]
# Example: ./combine_gifs.sh simple_flux.gif screen_demo.gif simple_flux_full 900
#
# Paths are relative to repo root if not absolute.
# [width]  resize BOTH GIFs to this width before combining (height auto-scales).
#          If omitted, gif2 is resized to match gif1's natural width.
#
# Env overrides: GIF_FPS, GIF_WIDTH

set -euo pipefail

ARG1="${1:?Usage: combine_gifs.sh <gif1> <gif2> [output_name] [width]}"
ARG2="${2:?Usage: combine_gifs.sh <gif1> <gif2> [output_name] [width]}"
OUTPUT_NAME="${3:-combined}"
CLI_WIDTH="${4:-}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

GIF_FPS="${GIF_FPS:-20}"
GIF_WIDTH="${GIF_WIDTH:-}"
[[ -n "$CLI_WIDTH" ]] && GIF_WIDTH="$CLI_WIDTH"

if ! command -v ffmpeg &>/dev/null; then
    echo "Error: 'ffmpeg' not found. Install with: brew install ffmpeg" >&2
    exit 1
fi

resolve_path() {
    local f="$1"
    [[ "$f" = /* ]] && echo "$f" || echo "$REPO_ROOT/$f"
}

GIF1=$(resolve_path "$ARG1")
GIF2=$(resolve_path "$ARG2")
OUTPUT_FILE="$REPO_ROOT/${OUTPUT_NAME}.gif"

for f in "$GIF1" "$GIF2"; do
    [[ -f "$f" ]] || { echo "Error: $f not found" >&2; exit 1; }
done

# Fast probe: read only the header, not every frame
probe_dim() {
    ffprobe -v error -probesize 5000000 -analyzeduration 0 \
        -select_streams v:0 -show_entries stream="$2" \
        -of default=noprint_wrappers=1:nokey=1 "$1" 2>/dev/null
}

# If no explicit width, use gif1's natural width so both match
if [[ -z "$GIF_WIDTH" ]]; then
    GIF_WIDTH=$(probe_dim "$GIF1" width)
    echo "No width specified — using gif1 natural width: ${GIF_WIDTH}px"
fi

WORKDIR=$(mktemp -d)
trap 'rm -rf "$WORKDIR"' EXIT
PALETTE="$WORKDIR/palette.png"

# Compute the scaled height of each input at the target width,
# then pad both to the taller of the two so concat dimensions match.
W1=$(probe_dim "$GIF1" width);  H1=$(probe_dim "$GIF1" height)
W2=$(probe_dim "$GIF2" width);  H2=$(probe_dim "$GIF2" height)
H1_SCALED=$(awk "BEGIN{printf \"%d\", int($H1 * $GIF_WIDTH / $W1)}")
H2_SCALED=$(awk "BEGIN{printf \"%d\", int($H2 * $GIF_WIDTH / $W2)}")
MAX_H=$(( H1_SCALED > H2_SCALED ? H1_SCALED : H2_SCALED ))

# scale to target width preserving AR, pad height to MAX_H (letterbox)
PAD_FILTER="scale=${GIF_WIDTH}:-1:flags=lanczos,pad=${GIF_WIDTH}:${MAX_H}:(ow-iw)/2:(oh-ih)/2"
CONCAT_FILTER="[0:v]${PAD_FILTER},fps=${GIF_FPS}[v0];[1:v]${PAD_FILTER},fps=${GIF_FPS}[v1];[v0][v1]concat=n=2:v=1:a=0[vcat]"

echo "GIF 1:  $GIF1"
echo "GIF 2:  $GIF2"
echo "Output: $OUTPUT_FILE"
echo "Width:  ${GIF_WIDTH}px  Heights: ${H1_SCALED}px / ${H2_SCALED}px → padded to ${MAX_H}px  FPS: ${GIF_FPS}"
echo ""

# Pass 1: build palette from the full concatenated stream
ffmpeg -y -nostdin -i "$GIF1" -i "$GIF2" \
    -filter_complex "${CONCAT_FILTER};[vcat]palettegen=stats_mode=diff[p]" \
    -map "[p]" "$PALETTE" -loglevel warning

# Pass 2: render combined GIF using palette
ffmpeg -y -nostdin -i "$GIF1" -i "$GIF2" -i "$PALETTE" \
    -filter_complex "${CONCAT_FILTER};[vcat][2:v]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle[out]" \
    -map "[out]" "$OUTPUT_FILE" -loglevel warning

echo "Done: $OUTPUT_FILE"
