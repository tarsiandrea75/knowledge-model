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

printf '==> Running validate-agent-routing self-test\n'
"$PYTHON_BIN" scripts/validate-agent-routing.py --self-test

printf '==> Running validate-rule-coverage self-test\n'
"$PYTHON_BIN" scripts/validate-rule-coverage.py --self-test

printf '==> Running validate-markdown-json self-test\n'
"$PYTHON_BIN" scripts/validate-markdown-json.py --self-test

printf '==> Running validation inventory self-test\n'
"$PYTHON_BIN" scripts/validate-validation-inventory.py --self-test

printf '==> Running validate-schema-prerequisites self-test\n'
"$PYTHON_BIN" scripts/validate-schema-prerequisites.py --self-test

printf '==> Running validate-schema-contracts self-test\n'
"$PYTHON_BIN" scripts/validate-schema-contracts.py --self-test

printf '==> Running validate-schema-duplicate-contracts self-test\n'
"$PYTHON_BIN" scripts/validate-schema-duplicate-contracts.py --self-test

printf '==> Running validate-fixtures self-test\n'
"$PYTHON_BIN" scripts/validate-fixtures.py --self-test

printf '==> Running validate-data semantic self-test, including retriever and reranker relationship endpoints\n'
"$PYTHON_BIN" scripts/validate-data.py --self-test

printf '==> Running relationship support data validation\n'
"$PYTHON_BIN" scripts/validate-data.py

printf '==> Running data validation\n'
"$PYTHON_BIN" scripts/validate-data.py

printf '==> Running export-fixtures-graph self-test\n'
"$PYTHON_BIN" scripts/export-fixtures-graph.py --self-test

printf '==> Running export-data-graph self-test, including retriever and reranker nodes and supported specialization edges\n'
"$PYTHON_BIN" scripts/export-data-graph.py --self-test

printf '==> Running validate-graph-exports self-test\n'
"$PYTHON_BIN" scripts/validate-graph-exports.py --self-test

printf '==> Running rkm-release-check self-test\n'
"$PYTHON_BIN" scripts/rkm-release-check.py --self-test

printf '==> Running rkm-route-task self-test\n'
"$PYTHON_BIN" scripts/rkm-route-task.py --self-test

printf '==> Running execution-profile selector self-test\n'
"$PYTHON_BIN" -B scripts/rkm-select-execution-profile.py --self-test

printf '==> Running Codex profile renderer self-test\n'
"$PYTHON_BIN" -B scripts/rkm-render-codex-profiles.py --self-test

printf '==> Running adaptive Codex execution wrapper self-test\n'
"$PYTHON_BIN" -B scripts/rkm-codex-exec.py --self-test

printf '==> Running compact evidence bundle self-test\n'
"$PYTHON_BIN" -B scripts/rkm-build-evidence-bundle.py --self-test

printf '==> Running rkm-decision-query self-test\n'
"$PYTHON_BIN" scripts/rkm-decision-query.py --self-test

printf '==> Running external RAG evidence verifier self-test\n'
"$PYTHON_BIN" scripts/verify-external-rag-evidence.py --self-test

printf '==> Running canonical RAG evidence projection self-test\n'
"$PYTHON_BIN" scripts/build-canonical-rag-evidence-projection.py --self-test

printf '==> Running canonical RAG evidence projection integrity self-test\n'
"$PYTHON_BIN" scripts/validate-canonical-rag-evidence-projection.py --self-test

printf '==> Running canonical RAG evidence projection query self-test\n'
"$PYTHON_BIN" scripts/query-canonical-rag-evidence-projection.py --self-test

printf '==> Running Creator prompt semantic duplication guardrail self-test\n'
creator_prompt_scripts=(scripts/rkm-cycle.sh scripts/rkm-discover.sh)
creator_prompt_guardrails=(
  "Do not infer that an architecture document is missing solely from a schema name, file name, or one-to-one schema-to-document comparison."
  "Before creating a new architecture document, inspect existing architecture documents for semantic coverage of the proposed concept."
  "Treat an existing canonical document as authoritative when it already covers the concept, even when its file name is not an exact match for a schema name."
  "Do not create a parallel document by inventing distinctions such as concept model versus document-level contract unless that distinction is explicitly established in existing repository architecture or governance."
  "Ground the selected work in a concrete repository need such as the governance backlog, rule coverage report, task guides, an explicit architectural gap, or a demonstrably uncovered schema contract."
  "When a candidate is already covered semantically, reject that candidate and choose another genuinely missing item."
  "Prefer no change over creating a speculative or duplicate architecture contract when no safe candidate can be demonstrated."
)
for script in "${creator_prompt_scripts[@]}"; do
  if ! grep -q 'CREATOR_PROMPT=' "$script"; then
    fail "Creator prompt guardrail check could not find CREATOR_PROMPT in $script"
  fi
  for guardrail in "${creator_prompt_guardrails[@]}"; do
    if ! grep -Fq "$guardrail" "$script"; then
      fail "Creator prompt in $script is missing semantic duplication guardrail: $guardrail"
    fi
  done
done

printf '==> Running autocycle timeout validation self-test\n'
if RKM_PER_CYCLE_TIMEOUT_SECONDS=0 bash scripts/rkm-autocycle.sh --validate-timeout-only >/tmp/rkm-autocycle-timeout-invalid.out 2>/tmp/rkm-autocycle-timeout-invalid.err; then
  fail "Invalid RKM_PER_CYCLE_TIMEOUT_SECONDS value was accepted"
fi
if ! grep -q 'RKM_PER_CYCLE_TIMEOUT_SECONDS must be a positive integer' /tmp/rkm-autocycle-timeout-invalid.err; then
  fail "Invalid RKM_PER_CYCLE_TIMEOUT_SECONDS error message was not actionable"
fi
RKM_PER_CYCLE_TIMEOUT_SECONDS=1800 bash scripts/rkm-autocycle.sh --validate-timeout-only >/tmp/rkm-autocycle-timeout-valid.out 2>/tmp/rkm-autocycle-timeout-valid.err
if RKM_PER_CYCLE_TIMEOUT_SECONDS=invalid "$PYTHON_BIN" scripts/rkm-autopilot.py --target 1 --dry-run >/tmp/rkm-autopilot-timeout-invalid.out 2>/tmp/rkm-autopilot-timeout-invalid.err; then
  fail "Invalid autopilot RKM_PER_CYCLE_TIMEOUT_SECONDS value was accepted"
fi
if ! grep -q 'RKM_PER_CYCLE_TIMEOUT_SECONDS must be a positive integer' /tmp/rkm-autopilot-timeout-invalid.err; then
  fail "Invalid autopilot RKM_PER_CYCLE_TIMEOUT_SECONDS error message was not actionable"
fi

printf 'SUCCESS: RKM unit tests passed.\n'
