#!/usr/bin/env bash

WRAPPER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

source "$WRAPPER_DIR/.venv/bin/activate"
python "$WRAPPER_DIR/main.py" "$@"
deactivate
