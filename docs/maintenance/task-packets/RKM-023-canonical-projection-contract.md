# RKM-023 — Canonical RAG Evidence Projection Contract

## Objective

Define a strict versioned envelope for a read-only projection of the reviewed
external RAG evidence bundle and its human source-review record.

## Scope

This task adds the JSON Schema contract for projection lifecycle, source and
review bindings, projected entity records, projected relationships, and
limitations. The contract is deliberately separate from canonical `data/**`
records so that projection work cannot silently change production knowledge or
recommendation policy.

## Contract rules

- The projection is limited to `INTERNAL_EVALUATION_ONLY`.
- The lifecycle is `Reviewed` and `Human Reviewed`, while
  `productionPromotionAllowed` is always `false`.
- Bundle and review identifiers, SHA-256 values, reviewer and review date are
  mandatory provenance fields on the envelope and every projected record.
- Projected entity types are limited to `Reference`, `Evidence`, `Dataset`,
  `Artifact`, and `Benchmark`.
- Projected relationship types are limited to the existing `REFERENCES`,
  `VALIDATES`, and `EVALUATES` vocabulary.
- Unsupported types, missing provenance, altered lifecycle values, and
  malformed identifiers fail schema validation.

## Dependencies

- RKM-019 external RAG evidence package
- RKM-020 external evidence review gate
- RKM-021 source freshness review readiness
- RKM-022 human source-review record

## Acceptance criteria

- `schema/rkm-canonical-rag-evidence-projection-v1.schema.json` validates as a
  JSON Schema Draft 2020-12 contract.
- Existing evidence, source-review, and recommendation contracts remain
  unchanged.
- The contract contains no production route, application-default, provider,
  licensing, or automatic-promotion behavior.
- The standard RKM validation gate passes.

## Validation

```bash
bash scripts/validate-rkm.sh
```

## Write scope

- `schema/rkm-canonical-rag-evidence-projection-v1.schema.json`
- `docs/maintenance/task-packets/RKM-023-canonical-projection-contract.md`

## Deferred work

The deterministic builder, projection fixtures, integrity gate, downstream
walkthrough, and release-readiness report belong to RKM-024 through RKM-028.
