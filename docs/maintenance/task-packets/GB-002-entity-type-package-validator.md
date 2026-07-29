# GB-002: Entity Type Package Validator

## Status

DONE

## Objective

Detect incomplete support when a populated RKM entity type is introduced,
before isolated data, schema, registry, manifest, graph-export, or
documentation changes can appear complete.

## Scope

- Add a deterministic validator for entity types represented by populated data.
- Verify registry entry, declared ontology directory, operational data storage,
  declared schema, identity support, architecture documentation, manifest
  coverage, and data graph-export nodes.
- Add positive and negative self-tests with actionable missing-component errors.
- Expose the validator through `make entity-type-package-validate` and include
  it in `make validate`.
- Update guardrails, backlog, rule coverage, and live handoff.

## Out of scope

- Adding or modifying canonical entity records, schemas, registries, manifests,
  or graph-export artifacts.
- Requiring data records for registry-only abstract or planned entity types.
- Inferring semantic relationship quality or changing graph-export behavior.
- Automatic repair or deletion of incomplete packages.

## Acceptance criteria

- Every populated entity type has one registry entry with a declared directory,
  consistent manifest schema path, and records stored below `data/` in one
  storage directory.
- The registered type is supported by the identity schema, has an architecture
  model document, and is represented by graph-export nodes for every record.
- Missing components fail with the entity type and required path in the output.
- Self-tests cover a complete package, missing registry entry, schema mismatch,
  missing documentation, and missing graph-export coverage.
- `make validate` invokes the validator and passes on the current repository.

## Required validation

Run after each changed file:

```bash
bash scripts/validate-rkm.sh
```

Focused checks:

```bash
python3 scripts/validate-entity-type-packages.py --self-test
python3 scripts/validate-entity-type-packages.py
git diff --check
```

## Stop conditions

Stop if current repository conventions cannot distinguish populated packages
from registry-only types, if graph-export coverage is intentionally partial for
an existing populated type, or if implementation requires canonical data or
schema changes.

## Handoff

The validator, integration, documentation, and backlog evidence passed the
full RKM validation. The implementation respects the existing distinction
between registry ontology directories and operational data storage
directories. No push is part of this task.
