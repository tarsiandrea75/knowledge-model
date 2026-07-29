# GB-004 Hard Dependency Predicate Justification

## Objective

Prevent hard dependency relationships from entering validated data without an
explicit justification.

## Scope

- Enforce a minimum structured justification for `REQUIRES` relationships.
- Add a deterministic validator self-test for the missing-justification case.
- Update the governance backlog and rule coverage report.

## Acceptance criteria

- [x] A `REQUIRES` relationship without `properties.justification` fails.
- [x] A justification shorter than 10 characters fails.
- [x] Existing data validation remains green.
- [x] The guardrail does not claim to judge semantic correctness.

## Validation

```bash
python3 scripts/validate-data.py --self-test
bash scripts/validate-rkm.sh
```

## Handoff

Implemented locally on 2026-07-29. Existing canonical data required no
migration because it currently contains no `REQUIRES` relationship instances.
