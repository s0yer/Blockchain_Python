#!/usr/bin/env bash
set -euo pipefail
LAUCHER_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export PYINSTALLER_CONFIG_DIR="$LAUCHER_DIR/build/cache"
python3 -m venv "$LAUCHER_DIR/build/venv-linux"
"$LAUCHER_DIR/build/venv-linux/bin/python" -m pip install -r "$LAUCHER_DIR/requirements-build.txt"
"$LAUCHER_DIR/build/venv-linux/bin/python" "$LAUCHER_DIR/gerar.py"
