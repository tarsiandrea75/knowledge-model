# RKM-019 External RAG Evidence Package

## Objective

Add a review-ready evidence package that connects the openly sourced NASA
space-exploration corpus, its golden dataset, the generated RAG recommendation
artifact, and the persisted RKM decision record. The package must remain
provider-free, reproducible, and unable to promote a production route.

## Scope

- Add a versioned external-evidence bundle contract and fixture.
- Record canonical source URLs, attribution, rights, retrieval date, source
  identity hashes, corpus and dataset hashes, and recommendation provenance.
- Add a concise user-readable decision report describing quality, latency,
  estimated local cost, recommendation, and limitations.
- Keep lifecycle state `Draft` / `Not Reviewed` and production promotion
  disabled.

## Acceptance criteria

- [x] The bundle validates against a strict JSON Schema contract.
- [x] Every source records canonical URL, attribution, rights, retrieval date,
  media kind, and a lowercase SHA-256 source identity.
- [x] Corpus, golden dataset, generated artifact, and persisted decision are
  linked by identifiers and SHA-256 hashes.
- [x] The report distinguishes measured retrieval evidence from invoice-grade
  provider billing and does not claim live model generation.
- [x] The fixture is provider-free, deterministic, and included in standard
  RKM validation.
- [x] No production configuration, default route, canonical promotion, or
  external service is changed.

## Required validation

```bash
make validate
```

## Boundary

This task closes the real-corpus evidence packaging gap. It does not authorize
automatic production promotion, application-default changes, microservices,
new providers, or unmeasured RAG strategies.

## Handoff

Completed locally on 2026-07-29. The package is review-ready but remains
non-promotable until a human reviews source rights and freshness.
