# GB-011 Validation Weakening Detector

## Objective

Prevent silent removal of critical validators or their self-test and main
pipeline hooks.

## Scope

- Maintain a small inventory of critical validator scripts.
- Verify each script exists and is invoked by both self-test and main
  validation paths.
- Expose the check through Make and the standard validation pipeline.

## Acceptance criteria

- [x] Missing validator files fail the inventory check.
- [x] Missing self-test or main-pipeline hooks fail the inventory check.
- [x] The inventory has a self-test and is documented as a bounded guardrail.
- [x] The check does not claim semantic equivalence between arbitrary revisions.

## Validation

```bash
python3 scripts/validate-validation-inventory.py --self-test
make validation-inventory-validate
bash scripts/validate-rkm.sh
```

## Handoff

Implemented locally on 2026-07-29. The guardrail protects validator wiring;
semantic regression comparison remains a deferred capability.
