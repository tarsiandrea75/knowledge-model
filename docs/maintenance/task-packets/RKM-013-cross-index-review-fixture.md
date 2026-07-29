# RKM-013 Cross-Index Review Fixture

## Objective

Persist a reproducible adapter fixture for a multi-index recommendation that
requires explicit review.

## Acceptance criteria

- [x] The fixture conforms to `rag-recommendation-report-v1`.
- [x] Adapter self-test consumes the fixture.
- [x] All profiles remain unavailable and preserve the review reason.
- [x] Walkthrough documentation identifies the fixture and its limits.

## Validation

```bash
make rag-recommendation-adapter-test
bash scripts/validate-rkm.sh
```

## Handoff

Implemented locally on 2026-07-29. The fixture is evidence of consumer
behavior, not a production recommendation.
