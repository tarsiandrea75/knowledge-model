# RKM-016 Review-Ready RAG Decision Record

## Objective

Persist recommendation provenance and lifecycle state in a strict RKM-owned
decision record without introducing a new ontology entity or authorizing
production promotion.

## Scope

- Define the versioned decision-record schema.
- Add a deterministic adapter-to-decision persistence script.
- Preserve source artifact, corpus, dataset, index, policy and profile data.
- Keep the record Draft and Not Reviewed by default.

## Acceptance criteria

- [x] The decision record requires source artifact and evaluation provenance.
- [x] Lifecycle state is fail-closed: Draft, Not Reviewed, promotion false.
- [x] Available and unavailable recommendation invariants are preserved.
- [x] A checked-in decision fixture validates through the fixture manifest.
- [x] No canonical data mutation, ontology entity or production route is added.

## Validation

```bash
python3 scripts/persist-rag-recommendation-decision.py --self-test
make validate
```

## Handoff

Implemented locally on 2026-07-29. This record is review-ready evidence, not a
production policy decision.
