#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

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

PYTHON_BIN="$(find_python)"
export PYTHONDONTWRITEBYTECODE=1

printf '==> Resolving repository root\n'
printf 'Repository root: %s\n' "$ROOT_DIR"

printf '==> Checking top-level shell script syntax\n'
shopt -s nullglob
shell_scripts=(scripts/*.sh)
shopt -u nullglob

if [[ "${#shell_scripts[@]}" -eq 0 ]]; then
  fail "No top-level shell scripts found in scripts"
fi

for script in "${shell_scripts[@]}"; do
  printf 'Checking %s\n' "$script"
  bash -n "$script"
done

printf '==> Running rkm-review-verdict self-test\n'
"$PYTHON_BIN" scripts/rkm-review-verdict.py --self-test

printf '==> Running validate-doc-relationships self-test\n'
"$PYTHON_BIN" scripts/validate-doc-relationships.py --self-test

printf 'SUCCESS: RKM unit tests passed.\n'
