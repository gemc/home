#!/usr/bin/env bash
# Types a Python file character-by-character then runs it.
# Intended to be called by record_example.sh via asciinema --command.
#
# Usage: type_and_run.sh <python_file>
# Env overrides: CHAR_DELAY, LINE_PAUSE, BLANK_PAUSE

set -euo pipefail

PYTHON_FILE="${1:?Usage: type_and_run.sh <python_file>}"
CHAR_DELAY="${CHAR_DELAY:-0.04}"
LINE_PAUSE="${LINE_PAUSE:-0.15}"
BLANK_PAUSE="${BLANK_PAUSE:-0.5}"

type_line() {
    local line="$1"
    for (( i=0; i<${#line}; i++ )); do
        printf '%s' "${line:$i:1}"
        # small random jitter per character
        sleep "$(awk 'BEGIN{srand(); printf "%.3f", '"$CHAR_DELAY"' + rand() * 0.02}')"
    done
    printf '\n'
    sleep "$LINE_PAUSE"
}

clear
sleep 0.8

while IFS= read -r line; do
    if [[ -z "$line" ]]; then
        echo ""
        sleep "$BLANK_PAUSE"
    else
        type_line "$line"
    fi
done < "$PYTHON_FILE"

sleep 0.8
echo ""
echo "# --- running ---"
sleep 0.5

cd "$(dirname "$PYTHON_FILE")"
python3 "$(basename "$PYTHON_FILE")"
sleep 1.5
