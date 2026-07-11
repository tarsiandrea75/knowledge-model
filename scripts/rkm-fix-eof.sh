#!/usr/bin/env bash
set -euo pipefail

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

find_python() {
  if command -v python3 >/dev/null 2>&1; then
    printf 'python3'
    return 0
  fi

  if command -v python >/dev/null 2>&1; then
    printf 'python'
    return 0
  fi

  fail "Required command not found: python3 or python"
}

if [[ "$#" -eq 0 ]]; then
  fail "At least one file path is required."
fi

for path in "$@"; do
  if [[ ! -e "$path" ]]; then
    fail "Path does not exist: $path"
  fi

  if [[ ! -f "$path" ]]; then
    fail "Path is not a regular file: $path"
  fi
done

PYTHON_BIN="$(find_python)"

"$PYTHON_BIN" - "$@" <<'PY'
from __future__ import annotations

import sys
from pathlib import Path


for raw_path in sys.argv[1:]:
    path = Path(raw_path)
    data = path.read_bytes()
    normalized = data.rstrip(b"\r\n") + b"\n"

    if normalized != data:
        path.write_bytes(normalized)

    print(raw_path)
PY
