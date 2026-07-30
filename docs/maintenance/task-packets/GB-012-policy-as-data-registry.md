# GB-012 — Policy-as-Data Registry

## Status

Implemented together with GB-013 Stable Rule IDs and GB-014 Rule-to-Validator
Links.

## Objective

Create a versioned, machine-readable governance registry that connects stable
rule identifiers to their source files, enforcement level, validators,
executable commands, and review owner.

## Delivered contract

- Registry: `registries/governance-policy-registry.json`.
- Schema: `schema/governance-policy-registry-v1.schema.json`.
- Stable IDs: `RKM-GOV-001` through `RKM-GOV-007`.
- Verifier: `scripts/validate-governance-policy-registry.py`.
- Make target: `make governance-policy-registry-validate`.
- Standard unit self-test: `scripts/rkm-unit-tests.sh`.

## Safety boundary

The registry describes existing governance and validation behavior. It does
not grant authority, create new permissions, or convert advisory semantic
review into automatic acceptance. `RKM-GOV-007` remains explicitly
`Partially Validated` because predicate equivalence and justification require
human judgment.

## Acceptance criteria

- Stable IDs are unique and match the versioned schema.
- Every declared source file and validator exists inside the repository.
- Every declared Make command resolves to an existing target.
- Validated rules have at least one validator and executable command.
- Missing files, missing targets, duplicate IDs, and schema violations fail
  closed with actionable diagnostics.

## Validation

```bash
make governance-policy-registry-validate
bash scripts/validate-rkm.sh
```

## Deferred work

The registry currently covers seven core rules. Expanding it to every prose
row in the coverage report requires a separate inventory review; unverified
rules must not be marked `Validated` merely because they are documented.
