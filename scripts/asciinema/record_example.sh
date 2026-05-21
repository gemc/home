#!/usr/bin/env bash
# Records an asciinema cast of typing and running a GEMC example.
# The cast is saved to <repo_root>/<name>.cast for easy GIF conversion.
#
# Usage:   ./record_example.sh <example_name>
# Example: ./record_example.sh simple_flux
#
# Per-example config: create configs/<example_name>.env to override
# COLS, ROWS, CHAR_DELAY, LINE_PAUSE, BLANK_PAUSE.

set -euo pipefail

EXAMPLE_NAME="${1:?Usage: record_example.sh <example_name>}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
EXAMPLES_ROOT="${EXAMPLES_ROOT:-/opt/projects/gemc/src/examples}"

# Defaults (overridable via configs/<name>.env)
export COLS="${COLS:-100}"
export ROWS="${ROWS:-30}"
export CHAR_DELAY="${CHAR_DELAY:-0.04}"
export LINE_PAUSE="${LINE_PAUSE:-0.15}"
export BLANK_PAUSE="${BLANK_PAUSE:-0.5}"

CONFIG_FILE="$SCRIPT_DIR/configs/${EXAMPLE_NAME}.env"
if [[ -f "$CONFIG_FILE" ]]; then
    # shellcheck source=/dev/null
    source "$CONFIG_FILE"
    echo "Loaded config: $CONFIG_FILE"
fi

PY_FILE=$(find "$EXAMPLES_ROOT" -name "${EXAMPLE_NAME}.py" | head -1)
if [[ -z "$PY_FILE" ]]; then
    echo "Error: ${EXAMPLE_NAME}.py not found under ${EXAMPLES_ROOT}" >&2
    exit 1
fi
echo "Source: $PY_FILE"

CAST_FILE="$REPO_ROOT/${EXAMPLE_NAME}.cast"
echo "Output: $CAST_FILE"
echo ""

asciinema rec \
    --cols "$COLS" \
    --rows "$ROWS" \
    --title "$EXAMPLE_NAME" \
    --overwrite \
    --command "bash $SCRIPT_DIR/type_and_run.sh $PY_FILE" \
    "$CAST_FILE"

echo ""
echo "Done: $CAST_FILE"
