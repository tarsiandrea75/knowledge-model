# GB-010 Graph Export Provenance Consistency

## Objective

Validate that every committed graph export node and edge points to existing
repository-local source and support artifacts.

## Scope

- Extend `scripts/validate-graph-exports.py` with provenance path checks.
- Cover fixture sources, data sources, manifests, schemas, relationship sets,
  target data files, and relationship-support sets.
- Preserve the existing graph schema and endpoint checks.

## Acceptance criteria

- Existing graph exports pass the strengthened validator.
- Missing provenance files, repository escapes, and malformed support path lists
  fail with actionable diagnostics.
- The validator self-test covers a missing provenance path.
- The rule coverage report and graph export contract describe the enforced rule.

## Validation

```bash
python3 scripts/validate-graph-exports.py --self-test
make graph-export-validate
bash scripts/validate-rkm.sh
```

## Handoff

Implemented locally on 2026-07-29. No graph data or schema files were changed.
