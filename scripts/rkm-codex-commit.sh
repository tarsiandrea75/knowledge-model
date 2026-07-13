#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

TAIL_LINES="${TAIL_LINES:-80}"
PROMPT_FILE=""
COMMIT_MESSAGE=""
CODEX_OUTPUT=""
SELF_TEST=false
EXPECTED_FILES=()

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

usage() {
  printf 'Usage: %s --prompt-file PATH (--file PATH | --files "PATHS") --message TEXT\n' "${0##*/}" >&2
}

require_command() {
  local command_name="$1"
  command -v "$command_name" >/dev/null 2>&1 || fail "Required command not found: $command_name"
}

print_codex_output_tail() {
  if [[ -n "$CODEX_OUTPUT" && -f "$CODEX_OUTPUT" ]]; then
    printf '\nCodex output tail (%s lines):\n' "$TAIL_LINES" >&2
    tail -n "$TAIL_LINES" "$CODEX_OUTPUT" >&2
  fi
}

append_expected_file() {
  local file_path="$1"
  [[ -n "$file_path" ]] || return 0
  EXPECTED_FILES+=("$file_path")
}

append_expected_files_string() {
  local files_string="$1"
  local file_path
  for file_path in $files_string; do
    append_expected_file "$file_path"
  done
}

unique_list() {
  local existing
  local item
  local seen
  local unique=()

  for item in "$@"; do
    seen=false
    for existing in "${unique[@]}"; do
      if [[ "$existing" == "$item" ]]; then
        seen=true
        break
      fi
    done

    if [[ "$seen" == false ]]; then
      unique+=("$item")
    fi
  done

  if [[ "${#unique[@]}" -gt 0 ]]; then
    printf '%s\n' "${unique[@]}"
  fi
}

contains_item() {
  local needle="$1"
  shift
  local item

  for item in "$@"; do
    if [[ "$item" == "$needle" ]]; then
      return 0
    fi
  done

  return 1
}

print_list() {
  local label="$1"
  shift

  printf '%s:\n' "$label"
  if [[ "$#" -eq 0 ]]; then
    printf '  (none)\n'
    return 0
  fi

  local item
  for item in "$@"; do
    printf '  %s\n' "$item"
  done
}

collect_changed_files() {
  {
    git diff --name-only
    git diff --cached --name-only
    git ls-files --others --exclude-standard
  } | awk 'NF && !seen[$0]++'
}

run_self_test() {
  local -a normalized
  EXPECTED_FILES=()
  append_expected_file "scripts/a.sh"
  append_expected_files_string "Makefile scripts/a.sh scripts/b.py"
  append_expected_file "Makefile"
  mapfile -t normalized < <(unique_list "${EXPECTED_FILES[@]}")

  [[ "${#normalized[@]}" -eq 3 ]] || fail "Self-test failed: expected 3 normalized files."
  [[ "${normalized[0]}" == "scripts/a.sh" ]] || fail "Self-test failed: first file mismatch."
  [[ "${normalized[1]}" == "Makefile" ]] || fail "Self-test failed: second file mismatch."
  [[ "${normalized[2]}" == "scripts/b.py" ]] || fail "Self-test failed: third file mismatch."

  print_list "Self-test normalized files" "${normalized[@]}"
  printf 'Self-test passed.\n'
}

on_error() {
  local exit_code="$?"
  print_codex_output_tail
  exit "$exit_code"
}

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --prompt-file)
      [[ "$#" -ge 2 ]] || fail "Missing value for --prompt-file."
      PROMPT_FILE="$2"
      shift 2
      ;;
    --file)
      [[ "$#" -ge 2 ]] || fail "Missing value for --file."
      append_expected_file "$2"
      shift 2
      ;;
    --files)
      [[ "$#" -ge 2 ]] || fail "Missing value for --files."
      append_expected_files_string "$2"
      shift 2
      ;;
    --message)
      [[ "$#" -ge 2 ]] || fail "Missing value for --message."
      COMMIT_MESSAGE="$2"
      shift 2
      ;;
    --self-test)
      SELF_TEST=true
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      usage
      fail "Unknown argument: $1"
      ;;
  esac
done

if [[ "$SELF_TEST" == true ]]; then
  run_self_test
  exit 0
fi

mapfile -t EXPECTED_FILES < <(unique_list "${EXPECTED_FILES[@]}")

if [[ -z "$PROMPT_FILE" ]]; then
  usage
  fail "Missing required argument: --prompt-file."
fi

if [[ "${#EXPECTED_FILES[@]}" -eq 0 ]]; then
  usage
  fail "At least one --file or --files path is required."
fi

if [[ -z "$COMMIT_MESSAGE" ]]; then
  usage
  fail "Missing required argument: --message."
fi

if [[ ! -f "$PROMPT_FILE" ]]; then
  fail "Prompt file does not exist: $PROMPT_FILE"
fi

require_command codex
require_command git
require_command make
require_command mktemp
require_command tail

CODEX_OUTPUT="$(mktemp /tmp/rkm-codex-commit.XXXXXXXX)"
trap on_error ERR

prompt_content="$(cat "$PROMPT_FILE")"

set +e
codex exec --sandbox workspace-write "$prompt_content" >"$CODEX_OUTPUT" 2>&1
codex_status="$?"
set -e

if [[ "$codex_status" -ne 0 ]]; then
  print_codex_output_tail
  exit "$codex_status"
fi

printf '\nCodex output tail (%s lines):\n' "$TAIL_LINES"
tail -n "$TAIL_LINES" "$CODEX_OUTPUT"

mapfile -t CHANGED_FILES < <(collect_changed_files)
CHANGED_EXPECTED_FILES=()
UNCHANGED_EXPECTED_FILES=()
UNEXPECTED_FILES=()

for expected_file in "${EXPECTED_FILES[@]}"; do
  if contains_item "$expected_file" "${CHANGED_FILES[@]}"; then
    CHANGED_EXPECTED_FILES+=("$expected_file")
  else
    UNCHANGED_EXPECTED_FILES+=("$expected_file")
  fi
done

for changed_file in "${CHANGED_FILES[@]}"; do
  if ! contains_item "$changed_file" "${EXPECTED_FILES[@]}"; then
    UNEXPECTED_FILES+=("$changed_file")
  fi
done

print_list "Expected files" "${EXPECTED_FILES[@]}"
print_list "Changed expected files" "${CHANGED_EXPECTED_FILES[@]}"
print_list "Unchanged expected files" "${UNCHANGED_EXPECTED_FILES[@]}"
print_list "Unexpected changed files" "${UNEXPECTED_FILES[@]}"

if [[ "${#UNEXPECTED_FILES[@]}" -gt 0 ]]; then
  printf '\nFinal git status:\n'
  git status --short
  fail "Unexpected files changed; refusing to commit."
fi

if [[ "${#CHANGED_EXPECTED_FILES[@]}" -eq 0 ]]; then
  printf '\nFinal git status:\n'
  git status --short
  fail "No expected files changed; refusing to commit."
fi

make validate
git add -- "${CHANGED_EXPECTED_FILES[@]}"
git diff --cached --check
git commit -m "$COMMIT_MESSAGE"
printf '\nFinal git status:\n'
git status --short
