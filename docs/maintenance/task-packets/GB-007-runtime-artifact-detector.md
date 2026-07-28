# GB-007: Runtime Artifact Detector

## Status

DONE

## Objective

Add deterministic validation that rejects repository-local runtime logs,
transcripts, scratch files, and temporary run directories before they can
pollute Git status, recovery decisions, or operational handoffs.

## Scope

- Add a focused validator with a self-test covering allowed and rejected paths.
- Expose the validator through `make runtime-artifacts-validate`.
- Include the validator in the standard `make validate` pipeline.
- Document the enforced artifact classes and the remediation path.
- Update the governance backlog and rule-coverage report with the implemented
  enforcement.

## Out of scope

- Changes to schemas, canonical data, graph exports, or runtime application
  behavior.
- Deletion of existing files or modification of Git metadata.
- Inspection of developer secrets, environment files, or credential stores.
- Automatic cleanup of detected artifacts.

## Acceptance criteria

- The validator fails closed when known repository-local runtime artifact paths
  are present.
- The validator ignores `.git` and ordinary project files.
- Failure output identifies each offending path and the remediation rule.
- Self-tests cover positive detections, allowed files, nested paths, and the
  `.git` exclusion.
- `make validate` invokes the validator and passes on the clean repository.
- Governance documentation records GB-007 as implemented without overstating
  coverage beyond the detector's declared patterns.

## Required validation

Run after each changed file:

```bash
bash scripts/validate-rkm.sh
```

Focused checks:

```bash
python3 scripts/validate-runtime-artifacts.py --self-test
python3 scripts/validate-runtime-artifacts.py
git diff --check
```

## Stop conditions

Stop if the detector requires broad filename heuristics that create false
positives, if existing legitimate repository artifacts cannot be classified
without a policy decision, or if implementation requires changing unrelated
validation, schema, data, or Git behavior.

## Handoff

The validator, integration, documentation, and backlog evidence are complete.
The clean-repository self-test and full validation passed before the local
commit. No push is part of this task.
