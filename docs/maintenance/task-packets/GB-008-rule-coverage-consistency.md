# GB-008 Rule Coverage Consistency Validator

- Status: Implemented
- Priority: Medium
- Area: Governance

## Objective

Ensure that coverage rows claiming automated enforcement reference existing
scripts and Make targets.

## Implementation

`scripts/validate-rule-coverage.py` validates `Validated` and
`Partially Validated` rows in `docs/maintenance/rule-coverage-report.md`.
It is exposed through `make rule-coverage-validate` and runs as part of
`make validate`.

## Validation

```bash
python3 scripts/validate-rule-coverage.py --self-test
make validate
```

## Acceptance criteria

- [x] Missing scripts and Make targets are reported.
- [x] Valid command references pass.
- [x] Self-test coverage is included in the standard unit-test step.
- [x] The complete RKM validation pipeline passes.
