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

now_seconds() {
  date +%s
}

elapsed_seconds() {
  local started_at="$1"
  local finished_at
  finished_at="$(now_seconds)"
  printf '%s' "$((finished_at - started_at))"
}

start_step() {
  STEP_NAME="$1"
  STEP_STARTED_AT="$(now_seconds)"
  printf '\n==> %s\n' "$STEP_NAME"
}

pass_step() {
  printf 'PASS: %s (%ss)\n' "$STEP_NAME" "$(elapsed_seconds "$STEP_STARTED_AT")"
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
TOTAL_STARTED_AT="$(now_seconds)"
STEP_NAME=""
STEP_STARTED_AT="$TOTAL_STARTED_AT"

start_step "Running git whitespace validation..."
git diff --check
pass_step

start_step "Checking file encoding and line endings..."
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
pass_step

start_step "Checking for forbidden RKM naming..."
forbidden_naming_matches="$(
  grep -RInE "RAG Knowledge Base|RAG-KB|ragkb|rag-kb|rkm\.dev" README.md docs schema scripts .gitattributes 2>/dev/null \
    | grep -v '^AGENTS.md:' \
    | grep -v '^scripts/validate-rkm.sh:' || true
)"
if [[ -n "$forbidden_naming_matches" ]]; then
  printf '%s\n' "$forbidden_naming_matches" >&2
  fail "Forbidden project naming found."
fi
pass_step

start_step "Checking for TODO, TBD, placeholder markers and ellipses outside AGENTS.md..."
incomplete_content_matches="$(
  grep -RInE "TODO|TBD|placeholder|Placeholder|PLACEHOLDER|\.{3}|…" README.md docs schema scripts .gitattributes 2>/dev/null \
    | grep -v '^AGENTS.md:' \
    | grep -v '^scripts/validate-rkm.sh:' || true
)"
if [[ -n "$incomplete_content_matches" ]]; then
  printf '%s\n' "$incomplete_content_matches" >&2
  fail "Incomplete content marker found."
fi
pass_step

start_step "Checking for IDE files..."
ide_file_matches="$(
  find . \
    -path './.git' -prune -o \
    \( -path './.idea' -o -path './.idea/*' -o -path './.vscode' -o -path './.vscode/*' \) \
    -print \
    | while IFS= read -r path; do
        if git check-ignore -q -- "$path" && ! git ls-files --error-unmatch -- "$path" >/dev/null 2>&1; then
          continue
        fi
        printf '%s\n' "$path"
      done
)"
if [[ -n "$ide_file_matches" ]]; then
  printf '%s\n' "$ide_file_matches" >&2
  fail "IDE files or directories found."
fi
pass_step

start_step "Checking for temporary review files..."
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
pass_step

start_step "Checking for repository-local runtime artifacts..."
"$PYTHON_BIN" scripts/validate-runtime-artifacts.py --self-test
"$PYTHON_BIN" scripts/validate-runtime-artifacts.py
pass_step

start_step "Checking populated entity type packages..."
"$PYTHON_BIN" scripts/validate-entity-type-packages.py --self-test
"$PYTHON_BIN" scripts/validate-entity-type-packages.py
pass_step

start_step "Running JSON Schema validation..."
"$PYTHON_BIN" scripts/validate-schemas.py
pass_step

start_step "Running schema prerequisite validation..."
"$PYTHON_BIN" scripts/validate-schema-prerequisites.py
pass_step

start_step "Running schema contract validation..."
"$PYTHON_BIN" scripts/validate-schema-contracts.py
pass_step

start_step "Running schema duplicate contract validation"
"$PYTHON_BIN" scripts/validate-schema-duplicate-contracts.py
pass_step

start_step "Running registry validation..."
"$PYTHON_BIN" scripts/validate-registries.py
pass_step

start_step "Running fixture instance validation..."
"$PYTHON_BIN" scripts/validate-fixtures.py
pass_step

start_step "Running data instance validation..."
"$PYTHON_BIN" scripts/validate-data.py
pass_step

start_step "Running fixture graph export validation..."
"$PYTHON_BIN" scripts/export-fixtures-graph.py --check
pass_step
printf 'Fixture graph export validation passed.\n'

start_step "Running data graph export validation..."
"$PYTHON_BIN" scripts/export-data-graph.py --check
pass_step
printf 'Data graph export validation passed.\n'

start_step "Running graph export schema validation..."
"$PYTHON_BIN" scripts/validate-graph-exports.py
pass_step
printf 'Graph export schema validation passed.\n'

start_step "Running RKM unit tests..."
bash scripts/rkm-unit-tests.sh
pass_step

start_step "Running documentation relationship validation..."
"$PYTHON_BIN" scripts/validate-doc-relationships.py
pass_step

start_step "Running agent rule routing validation"
"$PYTHON_BIN" scripts/validate-agent-routing.py
pass_step

start_step "Running rule coverage consistency validation"
"$PYTHON_BIN" scripts/validate-rule-coverage.py
pass_step

printf '\nRKM validation passed. Total elapsed: %ss\n' "$(elapsed_seconds "$TOTAL_STARTED_AT")"
