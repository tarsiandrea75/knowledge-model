# RKM-014 Unavailable Recommendation Integrity

## Objective

Make the RKM recommendation adapter fail closed when an unavailable profile
still carries a pipeline identifier.

## Scope

- Validate the invariant in the adapter.
- Express the same invariant in the adapter JSON Schema.
- Add a deterministic self-test and document the contract boundary.

## Acceptance criteria

- [x] Available recommendations require a non-empty `pipelineId`.
- [x] Unavailable recommendations require an empty `pipelineId`.
- [x] The adapter rejects an unavailable recommendation that retains a
      pipeline identifier.
- [x] Existing available and cross-index review fixtures remain valid.
- [x] No persistence, routing, or production default is changed.

## Validation

```bash
make rag-recommendation-adapter-test
bash scripts/validate-rkm.sh
```

## Handoff

Implemented locally on 2026-07-29. This is a consumer-boundary integrity
check; it does not authorize production promotion.
