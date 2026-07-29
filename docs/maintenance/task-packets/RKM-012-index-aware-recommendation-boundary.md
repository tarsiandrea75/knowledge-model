# RKM-012 Index-Aware Recommendation Boundary

## Objective

Ensure the RKM consumer preserves fail-closed recommendation decisions emitted
when standard profiles cannot compare different index profiles.

## Acceptance criteria

- [x] The adapter self-test covers an unavailable recommendation with
      `INDEX_PROFILE_REVIEW_REQUIRED`.
- [x] The adapter preserves the unavailable flag, empty pipeline ID, reason,
      and optional index profile identity.
- [x] Consumer documentation prohibits synthetic selection or promotion.

## Validation

```bash
make rag-recommendation-adapter-test
bash scripts/validate-rkm.sh
```

## Handoff

Implemented locally on 2026-07-29. No canonical RKM data or production route
was changed.
