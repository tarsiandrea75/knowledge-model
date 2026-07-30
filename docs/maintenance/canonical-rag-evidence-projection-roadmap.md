# Canonical RAG Evidence Projection Roadmap

## Decision

RKM will retain the external evidence bundle and human source-review record as
immutable audit artifacts. A later read-only projection will expose selected
source, evidence, dataset, artifact, and review concepts through canonical RKM
entities and relationships. The projection will never replace the source
bundle, infer unsupported claims, approve a RAG recommendation, or change a
production route.

## Boundary

The projection is derived from reviewed evidence and remains scoped to
`INTERNAL_EVALUATION_ONLY` until a separate policy decision changes that
scope. Every projected record must preserve the source bundle identifier,
bundle SHA-256, review-record identifier, review date, reviewer, source URL,
source identity hash, and lifecycle state.

The following remain outside this roadmap:

- automatic production promotion;
- application-default or routing changes;
- provider calls or network fetching;
- commercial or redistribution licensing decisions;
- microservices or distributed persistence;
- automatic creation of unsupported claims or relationships.

## Task sequence

### RKM-023 — Canonical projection contract

Define the versioned schema for a derived projection envelope. Specify the
allowed entity types, relationship types, lifecycle states, review scope,
provenance requirements, stable identifiers, and rejection rules.

Acceptance criteria:

- the contract is strict and versioned;
- source bundle and review-record hashes are mandatory;
- projection scope is explicit and non-promotable;
- unsupported entity or relationship types fail closed;
- existing evidence and decision contracts remain unchanged.

### RKM-024 — Deterministic projection builder

Implement a provider-free builder that reads the evidence bundle and human
review record and emits a canonical projection outside `data/` by default.
The builder must be deterministic, idempotent, and read-only with respect to
canonical data.

Acceptance criteria:

- identical inputs produce byte-equivalent output;
- source identity and review identity are stable;
- no network access or model call is made;
- missing or mismatched hashes fail closed;
- output remains scoped to internal evaluation.

### RKM-025 — Canonical entity and relationship fixtures

Create minimal, validated fixtures for references, evidence, datasets,
artifacts, and their provenance relationships using existing RKM contracts.
Do not add speculative ontology concepts when an existing entity type is
sufficient.

Acceptance criteria:

- fixtures validate through the standard manifest;
- every relationship has an existing registry predicate;
- evidence and references remain traceable to the source bundle;
- no production policy or recommendation entity is created implicitly.

### RKM-026 — Projection integrity and idempotence gate

Add validation that recomputes projection identities, checks source/review
hashes, rejects duplicate canonical identities, and proves repeatability in
two independent processes.

Acceptance criteria:

- tampered inputs fail with actionable diagnostics;
- repeated builds are byte-equivalent;
- duplicate or conflicting identities fail closed;
- the original bundle and review record remain unchanged.

### RKM-027 — Downstream query walkthrough

Document and test a consumer that loads the projection, follows provenance,
filters by internal-review scope, and distinguishes source review from RAG
recommendation lifecycle.

Acceptance criteria:

- a consumer can query source, evidence, artifact, and review links;
- the walkthrough displays scope and lifecycle explicitly;
- unavailable or non-reviewed recommendations cannot be promoted;
- the walkthrough uses no provider or production service.

### RKM-028 — Review and release boundary

Add a release-readiness report that summarizes projection coverage, unresolved
limitations, provenance completeness, and explicit non-goals. Decide whether
the projection is suitable for the next internal package without changing
production defaults.

Acceptance criteria:

- the report distinguishes technical validation from human policy approval;
- all hashes and lifecycle values are present;
- unresolved limitations are listed;
- publication remains a separate human-authorized action.

## Dependencies and gates

The order is deliberately sequential:

```text
RKM-023 -> RKM-024 -> RKM-025 -> RKM-026 -> RKM-027 -> RKM-028
```

RKM-023 is the first implementation task. No later task may weaken the
fail-closed lifecycle, bypass source provenance, or promote the RAG decision.
Each task requires `make validate` and a separate local protected commit.
Push and hosted verification remain human-controlled and occur only after a
completed bounded batch.

## Current human decision

The five NASA sources are approved for `INTERNAL_EVALUATION_ONLY` in
`rkm-external-rag-source-review-v1`. That decision is sufficient to begin
RKM-023, but it is not approval for redistribution, commercial use, canonical
production policy, or automatic RAG promotion.
