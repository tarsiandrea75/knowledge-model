# RKM-017 Fail-Closed Decision Persistence

## Objective

Prove that persistence preserves unavailable cross-index recommendations as
unavailable and never grants production promotion.

## Acceptance criteria

- [x] The persistence self-test covers `INDEX_PROFILE_REVIEW_REQUIRED`.
- [x] Unavailable profiles retain an empty `pipelineId`.
- [x] Lifecycle remains Draft and Not Reviewed.
- [x] `productionPromotionAllowed` remains false.

## Validation

```bash
python3 scripts/persist-rag-recommendation-decision.py --self-test
make validate
```

## Handoff

Implemented locally on 2026-07-29. Persistence remains a review boundary and
does not authorize production routing.
