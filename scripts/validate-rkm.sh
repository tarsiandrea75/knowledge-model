#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
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

echo "Running git whitespace validation..."
git diff --check

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

echo "RKM validation passed."
