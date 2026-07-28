# RKM-001: Downstream Recommendation Consumer Walkthrough

## Status

DONE

## Objective

Provide a reproducible, provider-free walkthrough showing how a downstream
RKM consumer accepts a `rag-recommendation-report-v1` artifact emitted by the
RAG Engineering Lab, converts it through the existing RKM adapter, validates
the resulting envelope, and inspects the selected policy profiles.

## Priority and rationale

The RAG↔RKM exchange contract, strict reader, and adapter already exist, but
there is no committed consumer path that a new user can execute from a clean
checkout. Closing that gap directly addresses the RKM maturity report's next
milestone and tests interoperability without changing production routing,
ontology semantics, or repository boundaries.

## Scope

- Add one representative checked-in recommendation artifact fixture.
- Add one provider-free walkthrough command or script path using the existing
  adapter and schema contract.
- Document inputs, commands, output shape, provenance, compatibility limits,
  and fail-closed behavior for downstream consumers.
- Record deferred external-evidence and production-integration ideas in the
  governance backlog.

## Out of scope

- No merge of the RAG and RKM repositories.
- No RAG application-default or production-route changes.
- No live provider, network, database, graph-server, or paid-service calls.
- No new ontology entity type or relationship predicate.
- No contract version migration or mutation of the existing v1 schema.
- No commit, push, branch, tag, ref, remote, or history operation by Codex.

## Deliverables

- A checked-in v1 source artifact fixture under `examples/fixtures/`.
- A tested downstream adapter invocation exposed through the existing Make
  interface.
- A consumer walkthrough under `docs/maintenance/`.
- A backlog update for deferred work and task closure evidence.

## Acceptance criteria

- The fixture validates against the lab-owned v1 contract without requiring
  RAG runtime classes or external services.
- The adapter consumes the fixture and emits a deterministic RKM envelope.
- The envelope validates against
  `schema/rag-recommendation-artifact-adapter-v1.schema.json`.
- The walkthrough can be followed from the repository root with documented
  commands and explains how to inspect the selected profiles.
- Invalid contract version, artifact type, unknown fields, and malformed
  profile values remain rejected by the existing adapter tests.
- The walkthrough labels the fixture as compatibility evidence, not a live
  production recommendation or universal strategy ranking.
- `make validate` passes with no repository-local runtime artifacts left
  behind.

## Required validation

```bash
make rag-recommendation-adapter-test
make validate
git diff --check
```

## Stop conditions

Stop and report if completion requires changing the v1 contract, adding a
runtime dependency, accessing credentials or external services, altering RAG
production defaults, changing ontology semantics, or expanding into an
external-evidence review campaign.

## Handoff

The compatibility fixture, adapter invocation, schema validation command and
consumer limitations are documented in
`docs/maintenance/rag-recommendation-consumer-walkthrough.md`. The executable
walkthrough passed with envelope schema validation and the adapter self-test;
`make validate` passed after each task-file cycle and at final closure. No RAG
runtime, provider, network, database, canonical RKM data, or production route
was changed. Deferred persistence and external-evidence work is recorded as
GB-045 in `docs/maintenance/governance-backlog.md`.
