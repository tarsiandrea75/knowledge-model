#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

print_git_status() {
  printf '\nGit status report:\n'
  git status --short
}

require_command() {
  local command_name="$1"
  command -v "$command_name" >/dev/null 2>&1 || fail "Required command not found: $command_name"
}

find_python() {
  if command -v python >/dev/null 2>&1; then
    printf 'python'
    return 0
  fi

  if command -v python3 >/dev/null 2>&1; then
    printf 'python3'
    return 0
  fi

  fail "Required command not found: python or python3"
}

require_command git
require_command grep
require_command find

PYTHON_BIN="$(find_python)"
trap print_git_status EXIT

echo "Running git whitespace validation..."
git diff --check

echo "Checking file encoding and line endings..."
"$PYTHON_BIN" - <<'PY'
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path.cwd()
FORBIDDEN_INVISIBLE = {
    b"\xef\xbb\xbf": "byte order mark",
    "\u200b".encode("utf-8"): "zero-width space",
    "\u00a0".encode("utf-8"): "non-breaking space",
}


def changed_files() -> list[Path]:
    result = subprocess.run(
        ["git", "status", "--porcelain", "-z"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    )
    entries = result.stdout.split(b"\0")
    paths: list[Path] = []
    index = 0

    while index < len(entries):
        entry = entries[index]
        index += 1
        if not entry:
            continue

        status = entry[:2].decode("ascii", errors="replace")
        raw_path = entry[3:]

        if status[0] in {"R", "C"} or status[1] in {"R", "C"}:
            index += 1

        if status == "!!" or "D" in status:
            continue

        path = ROOT / raw_path.decode("utf-8", errors="surrogateescape")
        if path.is_file():
            paths.append(path)

    return sorted(set(paths))


def display(path: Path) -> str:
    return str(path.relative_to(ROOT))


errors: list[str] = []

for path in changed_files():
    data = path.read_bytes()
    name = display(path)

    try:
        data.decode("utf-8")
    except UnicodeDecodeError as exc:
        errors.append(f"{name}: invalid UTF-8 at byte {exc.start}")
        continue

    if b"\r\n" in data:
        errors.append(f"{name}: CRLF line endings are not allowed")

    if data and not data.endswith(b"\n"):
        errors.append(f"{name}: missing final newline")

    for marker, label in FORBIDDEN_INVISIBLE.items():
        if marker in data:
            errors.append(f"{name}: forbidden invisible character found: {label}")

if errors:
    for error in errors:
        print(error, file=sys.stderr)
    raise SystemExit(1)
PY

echo "Checking for forbidden RKM naming..."
forbidden_naming_matches="$(
  grep -RInE "RAG Knowledge Base|RAG-KB|ragkb|rag-kb|rkm\.dev" README.md docs schema scripts .gitattributes 2>/dev/null \
    | grep -v '^AGENTS.md:' \
    | grep -v '^scripts/validate-rkm.sh:' || true
)"
if [[ -n "$forbidden_naming_matches" ]]; then
  printf '%s\n' "$forbidden_naming_matches" >&2
  fail "Forbidden project naming found."
fi

echo "Checking for TODO, TBD, placeholder markers and ellipses outside AGENTS.md..."
incomplete_content_matches="$(
  grep -RInE "TODO|TBD|placeholder|Placeholder|PLACEHOLDER|\.{3}|…" README.md docs schema scripts .gitattributes 2>/dev/null \
    | grep -v '^AGENTS.md:' \
    | grep -v '^scripts/validate-rkm.sh:' || true
)"
if [[ -n "$incomplete_content_matches" ]]; then
  printf '%s\n' "$incomplete_content_matches" >&2
  fail "Incomplete content marker found."
fi

echo "Checking for IDE files..."
ide_file_matches="$(
  find . \
    -path './.git' -prune -o \
    \( -path './.idea' -o -path './.idea/*' -o -path './.vscode' -o -path './.vscode/*' \) \
    -print
)"
if [[ -n "$ide_file_matches" ]]; then
  printf '%s\n' "$ide_file_matches" >&2
  fail "IDE files or directories found."
fi

echo "Checking for temporary review files..."
temporary_review_matches="$(
  find . \
    -path './.git' -prune -o \
    \( \
      -name '*review*tmp*' -o \
      -name '*tmp*review*' -o \
      -name '*.review' -o \
      -name '*.review.*' -o \
      -name 'review-notes*' -o \
      -name 'review-output*' -o \
      -name 'codex-review*' -o \
      -name '*codex-review*' -o \
      -name '*.tmp' -o \
      -name '*.temp' \
    \) \
    -print
)"
if [[ -n "$temporary_review_matches" ]]; then
  printf '%s\n' "$temporary_review_matches" >&2
  fail "Temporary review files found."
fi

echo "Running JSON Schema validation..."
"$PYTHON_BIN" scripts/validate-schemas.py

echo "Running registry validation..."
"$PYTHON_BIN" scripts/validate-registries.py

echo "Running documentation relationship validation..."
"$PYTHON_BIN" scripts/validate-doc-relationships.py

echo "RKM validation passed."
