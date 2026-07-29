# External RAG Evidence Report

## Executive decision

For the versioned `space-exploration-v1` corpus and its
`space-exploration-golden-v1` dataset, the provider-free walkthrough selected
the `naive` pipeline on `offline-fixture-index-v1` for the economical,
balanced, and maximum-quality profiles.

This is a bounded recommendation for one corpus and one deterministic
experiment. It is not a universal ranking of RAG strategies. The decision is
`Draft`, `Not Reviewed`, and explicitly not eligible for production promotion.

## Evidence chain

| Evidence | Identity | SHA-256 or revision |
| --- | --- | --- |
| RAG Engineering Lab source commit | `c72cf50b70c145f922e2e07e3e0c3a9c9ed8bd06` | Git SHA-1 |
| Corpus | `space-exploration-v1` 1.0.0 | `3c5be7b94065f4e6e2ecdfbafde926f57b2b912741f2de61bcac42ba8db30d4b` |
| Golden dataset | `space-exploration-golden-v1` 1.0.0 | `7c7c59829502a9c087f31c5c637a4aa88b81c952be35482ee706542bb0945d03` |
| Generated recommendation artifact | `offline-rag-e2e-walkthrough` 1.0.0 | `3f8a2e8e9296546b57aeda8904f9bf0db61127ce7bd09a17484f91089824927f` |
| RKM decision record | `offline-rag-e2e-walkthrough-decision` 1.0.0 | `f91f59006e668b02fac97e1443c7ed07db03ced2daf337db6332a22520f87d39` |

The machine-readable source of this table is
`examples/fixtures/rkm-external-rag-evidence-bundle-v1.json`.

## Source basis

The corpus contains five NASA source records covering text, image, audio, and
video material. Each record preserves its canonical URL, title, media kind,
retrieval date, attribution, rights statement, and source identity hash. The
corpus stores bounded derived text and provenance metadata; it does not claim
that downloaded media payloads are redistributed by RKM.

The source records are:

- NASA Science, [Our Sun: Facts](https://science.nasa.gov/sun/facts/);
- NASA Science, [Solar System Facts](https://science.nasa.gov/solar-system/solar-system-facts/);
- NASA, [Artemis I Media Resources](https://www.nasa.gov/general/artemis-i-media-resources/);
- NASA, [Artemis Audio Library](https://www.nasa.gov/artemisaudio/);
- NASA, [Artemis Media Resources](https://www.nasa.gov/humans-in-space/artemis-media-resources/).

The source URLs and rights statements are preserved as evidence metadata. A
human rights review remains required before redistribution or commercial use.

## Measured comparison

The recommendation artifact reports the following bounded result for the
selected pipeline:

- quality score: `1.0000`;
- P95 latency: `10 ms`;
- estimated cost: `0.001 LOCAL` units;
- recommendation: `naive` on `offline-fixture-index-v1`.

The local cost value is an experiment accounting value, not provider billing,
an invoice, or a cloud price. The provider-free walkthrough measures the
retrieval/evaluation contract and does not measure live language-model answer
quality.

## Review and lifecycle boundary

The evidence bundle and decision record are review-ready projections. They do
not write canonical RKM production data, alter application defaults, change a
routing bean, or authorize automatic promotion. The required review state is:

```text
status: Draft
reviewState: Not Reviewed
productionPromotionAllowed: false
```

## Limitations and next review

- Source identity hashes identify canonical URLs, not downloaded payload bytes.
- The evidence covers one small, openly sourced corpus and one deterministic
  dataset; it does not generalize to legal, medical, enterprise, or customer
  corpora.
- Live provider quality, provider billing, and production load behavior remain
  unmeasured here.
- Any future promotion requires independent human review, stronger evidence,
  and a separate compatibility decision.

Validation entry point:

```bash
make validate
```
