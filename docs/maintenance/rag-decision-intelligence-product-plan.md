# RAG Decision Intelligence Product Plan

Status: planning baseline for review  
Planning date: 2026-07-30  
Scope: the RAG Knowledge Model contribution to a usable corpus-to-decision
product and its staged path toward private-enterprise decision intelligence
with the RAG Engineering Lab  
Implementation authority: none; this document does not authorize schema,
canonical-data, registry, validator, automation, release, or production changes

## Executive decision

RKM should become the decision-intelligence layer for the RAG Engineering Lab,
but it should not attempt to become the execution runtime, a complete catalog
of the RAG ecosystem, or an autonomous production operator.

The repository has a broad conceptual model, strict schemas, deterministic
validation, graph exports, a small canonical seed dataset, and a validated
RAG recommendation evidence bridge. Its automation and governance are more
mature than its decision-critical knowledge content. The next program should
therefore prioritize the smallest body of reviewed knowledge needed to plan,
interpret, and explain real Lab experiments.

The target outcome is:

> Given a versioned corpus profile, user constraints, and the executable
> capability manifest of a RAG Lab installation, RKM proposes a bounded,
> evidence-linked experiment candidate set. After execution, RKM preserves the
> result as corpus-specific evidence and explains the quality/cost/latency
> tradeoffs without automatically promoting a production default.

## Relationship to the RAG Engineering Lab plan

The companion product plan is
`engineering/PRODUCT_STRATEGY.md` in the
`BuildingRAGAgentsWithLLMs` repository.

That plan is authoritative for:

- runtime execution;
- corpus inspection and fingerprinting;
- index preparation;
- pipeline capability discovery;
- experiment execution;
- measurements and traces;
- recommendation artifact production;
- the user-facing CLI or workbench;
- Spring AI implementation blueprints.

This document is authoritative for:

- technique knowledge and evidence;
- applicability and prerequisite reasoning;
- metric, benchmark, and dataset semantics;
- candidate-plan reasoning;
- cross-experiment evidence preservation;
- decision explanation and review lifecycle.

The repositories communicate through versioned artifacts. They do not share
implementation classes, databases, provider credentials, mutable runtime
state, or build systems.

## 2026-07-30 enterprise planning reconciliation

The approved product direction is a private-enterprise knowledge product, not
only a RAG technique comparison tool. RKM remains the decision-intelligence
layer: it models constraints, evidence, applicability, exclusions, and the
reasoning behind an experiment plan. It does not authenticate users, enforce
access control, retain source content, proxy models, or become the runtime
security boundary.

The initial product wedge remains a CLI-first financial-books pilot. It proves
the corpus-to-decision workflow on a real, rights-scoped corpus before the
project claims enterprise readiness. The companion Lab plan records the corpus
inventory and golden-set design in `engineering/FINANCIAL_BOOKS_PILOT.md`.

Before RKM ranks quality, latency, or cost, it must preserve the following
constraints as feasibility inputs:

- private installation and workspace isolation requirements;
- identity integration requirement and supported identity claims;
- authorization policy dimensions such as workspace, department,
  classification, ownership, and purpose;
- data residency, retention, audit, and egress constraints;
- whether local models are required or external providers are explicitly
  permitted for the workspace;
- read-only versus mutation authority for connected business systems.

RKM must treat an unmet constraint as `INAPPLICABLE` or `UNAVAILABLE`, not as
a lower-scoring candidate. It may explain the exclusion and propose a
compatible alternative. The Lab and deployment runtime remain responsible for
server-side enforcement along the complete information path:

```text
identity -> authorization -> source -> chunk -> index -> retrieval
         -> context -> answer -> citation -> audit
```

The enterprise track begins only after the measured decision-lab pilot. It
uses synthetic HR, business-intelligence, and billing-like content to prove
policy inheritance without exposing real company data.

## RKM north star

RKM should answer the following consumer queries:

1. Which techniques address the observed corpus and query failure modes?
2. What prerequisites does each technique require?
3. Which techniques can the connected Lab actually execute?
4. Which technique combinations are compatible?
5. What experiment can distinguish the candidates within the user's budget?
6. What external evidence supports or limits each candidate?
7. What local experimental evidence was observed on this exact corpus?
8. Which recommendation is economical, balanced, or maximum-quality?
9. How strong, fresh, and generalizable is the evidence?
10. What remains a human decision?

If a modeled field or entity does not help answer one of these questions or a
demonstrated downstream query, it is not a near-term product priority.

## Current-state reality check

| Dimension | Current evidence | Honest status | Product implication |
| --- | --- | --- | --- |
| Conceptual architecture | Broad models for techniques, pipelines, metrics, datasets, benchmarks, evidence, cost, policy, and workflows | Strong foundation | Reuse before adding concepts |
| Structural validation | JSON Schema, registries, semantic checks, graph integrity, deterministic exports, policy registry | Strong | Preserve; add validators only for demonstrated product failures |
| Canonical technique content | Six technique records: hybrid retrieval, query rewriting, reranking, and three chunking strategies | Narrow | Insufficient for broad planning |
| External technique evidence | Substantial primary evidence is present for hybrid retrieval and reranking; query rewriting and chunking records remain much thinner | Uneven | Deepen decision-critical techniques before adding breadth |
| Metric/benchmark/dataset content | Architecture and schemas exist; canonical seed coverage is limited | Missing decision core | GB-022, GB-023, and GB-024 are product-critical |
| RAG artifact bridge | Strict adapter, review-ready decision, external source bundle, human source review, projection, and consumer walkthrough | Strong bounded proof | Preserve as evidence transport, not automatic canonical truth |
| External corpus evidence | One small NASA-derived corpus package with internal-evaluation-only review | Useful smoke evidence | It proves provenance workflow, not general RAG applicability |
| Candidate planning | Lab validates a static RKM snapshot; RKM does not generate plans from corpus characteristics | Missing | This is the central future RKM capability |
| Cross-corpus learning | One recommendation decision is persisted as a fixture and projection | Missing | Accumulate comparable observations without universalizing them |
| Consumer experience | Validation, graph export, decision query, and walkthroughs exist | Partial | No direct "plan my corpus" workflow yet |
| Release maturity | Internal alpha documentation and validated repository | Foundation | A decision-intelligence release should follow a real pilot |
| Governance/automation | Rich and highly automated | Strong, possibly disproportionate | Freeze low-value automation expansion |

## Critical findings

### 1. RKM does not yet plan an experiment

The current bridge flows primarily from the Lab into RKM:

```text
Lab result
  -> recommendation artifact
  -> RKM adapter
  -> decision and evidence projection
```

The desired product needs a preceding direction:

```text
corpus profile + constraints + installed Lab capabilities
  -> RKM candidate reasoning
  -> bounded candidate plan
  -> Lab validation and execution
```

This planning function is currently conceptual. A static registry snapshot can
reject unknown technique IDs, but it does not explain applicability,
prerequisites, compatibility, expected cost, or why a technique should be
tested for a particular corpus.

### 2. Schema breadth exceeds populated decision knowledge

RKM has first-class models for many concepts, while the canonical populated
dataset remains intentionally small. The next maturity gain will not come from
adding more schema names. It will come from reviewed records and relationships
for:

- executable technique families;
- corpus and query characteristics;
- evaluation metrics;
- representative benchmarks and datasets;
- applicability, prerequisite, compatibility, limitation, and cost claims;
- local experiment observations.

### 3. The NASA evidence path proves provenance, not technique quality

The external evidence package validates source metadata, review scope,
content-addressed artifacts, recommendation lifecycle, and fail-closed
projection. It does not provide external research evidence for the comparative
quality of RAG techniques. These are different evidence domains and must remain
separate.

### 4. Technique records need operational applicability

The existing technique model describes stages, inputs, outputs, dependencies,
claims, evidence, and operational characteristics. The product path needs a
small machine-consumable applicability profile derived from those semantics.

It must be able to express:

- index-time, query-time, end-to-end, or control-flow impact;
- required corpus characteristics;
- target query archetypes or failure modes;
- required retriever, model, index, metadata, graph, or reranker capabilities;
- compatible and incompatible technique combinations;
- one-time and recurring cost dimensions;
- required evaluation metrics;
- external evidence strength and freshness;
- implementation availability in a specific Lab capability manifest.

This profile should reuse existing RKM concepts wherever possible. A new
first-class entity is justified only if existing technique, capability,
relationship, claim, evidence, policy, and pipeline structures cannot answer a
concrete consumer query.

### 5. A recommendation must combine, not confuse, evidence scopes

RKM should preserve at least three separate evidence scopes:

1. **External method evidence** — published findings about a technique under a
   named benchmark, dataset, implementation, and configuration.
2. **Local experiment evidence** — measurements for one corpus, dataset,
   index, pipeline, model, runtime, and policy.
3. **Human decision evidence** — review state, accepted tradeoff, deployment
   context, and explicit authorization.

External evidence can justify including a candidate. Local evidence can support
a corpus-specific recommendation. Human evidence can approve an operational
decision. None substitutes for another.

### 6. RKM should not recommend unavailable code

A technique can be:

- modeled by RKM;
- supported by external evidence;
- executable by the connected Lab;
- evaluated on the current corpus;
- recommended for the current constraints.

These are five distinct states. Candidate planning must intersect RKM knowledge
with the Lab's versioned capability manifest. Unknown or unavailable
implementations must be excluded or returned as research suggestions, never as
executable plan items.

### 7. The ontology should learn from experiments without becoming a result dump

Every run should not become a new universal technique claim. RKM needs a
structured observation boundary that preserves:

- corpus and dataset identity;
- query-archetype distribution;
- pipeline and index identity;
- metric definitions and values;
- operational measurements;
- environment and model versions;
- limitations and review state.

Aggregated conclusions require an explicit aggregation policy and comparable
evidence. Raw local results remain observations, not universal facts.

## Anti-cathedral product rules

RKM work is near-term product work only when it:

- supplies a field consumed by candidate planning;
- supplies evidence consumed by applicability or exclusion reasoning;
- defines a metric needed by the Lab report;
- preserves a real Lab result with complete provenance;
- answers a documented user or downstream query;
- is required for a versioned internal decision package.

RKM work should be deferred when it:

- adds a new entity type without a consumer query;
- expands providers or products unrelated to an executable pilot;
- models a technique with no target corpus or evaluation path;
- promotes projection fixtures into canonical data only to increase record
  count;
- adds automation without a demonstrated failure mode;
- attempts to encode an entire paper rather than bounded claims;
- treats popularity or framework support as quality evidence;
- introduces production routing or deployment behavior.

## Product contracts

The following contracts are proposed conceptually. They should be added only
in the phase that consumes them.

### Corpus profile

Produced by the Lab and consumed by RKM.

Minimum content:

- contract version;
- corpus ID, version, hash, size, language, and modality distribution;
- document length and structure distribution;
- metadata availability;
- identifier and exact-match signals;
- temporal/freshness characteristics;
- graph or hierarchy signals;
- table, code, OCR, and media characteristics;
- privacy and deployment constraints;
- workspace, authorization, egress, retention, and audit constraints;
- query-archetype distribution when known;
- profiler version and limitations.

The profile describes observable characteristics. It must not infer a
technique winner.

### Lab capability manifest

Produced by the Lab and consumed by RKM.

Minimum content:

- Lab version and source commit;
- installed implementation IDs and versions;
- mapped RKM technique IDs;
- affected stages and execution phase;
- supported configuration schema;
- required model and index capabilities;
- compatibility and exclusion constraints;
- thread-safety and isolation status;
- experimental or production eligibility;
- required metrics;
- supported authorization and provenance propagation guarantees;
- model-egress capabilities and explicit provider-policy requirements;
- capability-manifest hash.

### Candidate experiment plan

Produced by RKM and validated independently by the Lab.

Minimum content:

- source corpus-profile and capability-manifest identities;
- user objectives and constraints;
- hard feasibility constraints for identity, authorization, privacy, egress,
  deployment, retention, audit, and source-system mutation policy;
- baseline pipeline;
- bounded candidate pipelines and index profiles;
- technique and applicability evidence references;
- inclusion and exclusion rationale;
- estimated one-time and recurring cost classes;
- required metrics and minimum sample policy;
- maximum experiment budget;
- decision policy;
- RKM source commit and plan hash.

The default candidate plan should contain no more than six pipelines and three
index profiles. A larger plan requires an explicit rationale.

### Experiment evidence bundle

Produced by the Lab and consumed by RKM.

Minimum content:

- original plan identity;
- corpus, dataset, index, pipeline, model, and runtime provenance;
- per-case and aggregate metrics;
- per-archetype results;
- latency, token, storage, indexing, and cost observations;
- variance and sample counts;
- failures and limitations;
- recommendation artifact;
- immutable artifact hashes.

### Decision record

Produced by RKM after result validation.

Minimum content:

- selected or shortlisted candidates;
- Pareto frontier;
- dominated-candidate reasons;
- quality floors and critical-metric floors;
- evidence sufficiency;
- external and local evidence references;
- uncertainty;
- one-time and recurring cost;
- applicability and exclusion rationale;
- review state and lifecycle;
- explicit production-promotion state;
- implementation-blueprint reference.

## Decision reasoning model

RKM should use a conservative staged policy.

### Stage 0 — Policy feasibility

Before applicability or scoring, exclude a candidate when it requires an
unavailable identity, authorization, isolation, egress, residency, retention,
audit, or mutation capability. The plan must state the exact constraint and
the evidence used to evaluate it. A candidate never receives quality credit for
an execution that would violate the workspace policy.

### Stage 1 — Applicability

Exclude techniques whose prerequisites conflict with:

- corpus structure;
- query archetypes;
- privacy constraints;
- available metadata;
- available Lab capabilities;
- budget;
- unsupported index substrate.

### Stage 2 — Candidate value

Prioritize techniques that address an observed or expected failure mode:

- lexical identifiers suggest hybrid retrieval;
- noisy dense candidates suggest reranking;
- ambiguous or conversational queries suggest query transformation;
- long documents and lost local context suggest contextual indexing;
- global corpus questions suggest hierarchical or graph retrieval;
- mixed query complexity suggests adaptive routing.

These are candidate hypotheses, not recommendations. Each must link to
evidence and a measurable target.

### Stage 3 — Experiment economy

Prefer the smallest matrix that can falsify the hypotheses:

- one stable baseline;
- one change per diagnostic comparison where practical;
- query-time candidates before new indexes when they address the same failure;
- staged index construction;
- early elimination of dominated candidates.

### Stage 4 — Result interpretation

Interpret results using:

- critical-metric floors;
- per-archetype deltas;
- Pareto dominance;
- uncertainty and sample count;
- index and query costs;
- external-evidence consistency;
- limitations and review state.

### Stage 5 — Recommendation lifecycle

Valid outcomes include:

- `RECOMMENDED`;
- `SHORTLISTED`;
- `NOT_RECOMMENDED`;
- `INAPPLICABLE`;
- `UNAVAILABLE`;
- `INSUFFICIENT_EVIDENCE`;
- `REVIEW_REQUIRED`.

A policy must not force every experiment to produce a winner.

## Technique knowledge priorities

### Tier 1 — Complete the executable baseline

Prioritize reviewed knowledge for techniques the Lab already implements or can
measure with limited new infrastructure:

- dense naive retrieval;
- hybrid retrieval and rank fusion;
- reranking;
- query rewriting;
- HyDE;
- multi-query expansion;
- fixed-size, recursive, and semantic chunking.

For each technique, the minimum useful knowledge package is:

- bounded definition;
- stage and execution phase;
- prerequisites;
- target failure modes and query archetypes;
- compatible components;
- operational cost dimensions;
- at least one primary reference;
- conservative claims and limitations;
- required metrics;
- Lab capability mapping when implemented.

### Tier 2 — High-value index and retrieval candidates

Add only after the external pilot exposes a need:

- parent-child retrieval;
- contextual retrieval;
- late chunking;
- embedding and index variants;
- context compression;
- late-interaction retrieval.

### Tier 3 — Adaptive and corrective control flow

Model after routing and loop contracts exist:

- adaptive retrieval;
- no-retrieval routing;
- dynamic retrieval depth;
- iterative retrieval;
- corrective RAG;
- self-reflective RAG.

### Tier 4 — Structural and multimodal substrates

Model for execution planning only when a concrete corpus justifies:

- RAPTOR-like hierarchical retrieval;
- GraphRAG-like local/global search;
- knowledge-graph retrieval;
- true visual-document retrieval;
- audio or video segment retrieval;
- cross-modal retrieval.

Media-to-text ingestion alone does not satisfy this tier.

## External evidence refresh

RKM should maintain a bounded primary-source landscape rather than chase every
new paper.

Refresh cadence:

- quarterly for active technique families;
- before a planned minor release;
- when an upstream framework introduces a materially new execution primitive;
- when a pilot exposes an unsupported failure mode.

Each refresh should:

1. identify primary papers, official specifications, or authoritative
   implementation documentation;
2. extract only bounded claims relevant to product decisions;
3. record benchmark, dataset, metric, configuration, and limitations;
4. separate paper findings from maintainer inference;
5. record version and access date;
6. update freshness and review state;
7. avoid implementation commitment unless the product gate is met.

The current architectural watchlist includes:

- [Spring AI modular RAG](https://docs.spring.io/spring-ai/reference/api/retrieval-augmented-generation.html);
- [Adaptive-RAG](https://aclanthology.org/2024.naacl-long.389/);
- [Corrective RAG](https://arxiv.org/abs/2401.15884);
- [Self-RAG](https://openreview.net/forum?id=hSyW5go0v8);
- [RAPTOR](https://openreview.net/forum?id=GN921JHCRw);
- [GraphRAG](https://www.microsoft.com/en-us/research/publication/from-local-to-global-a-graph-rag-approach-to-query-focused-summarization/);
- [Late Chunking](https://arxiv.org/abs/2409.04701);
- [Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval);
- [ColBERTv2](https://aclanthology.org/2022.naacl-main.272/);
- [BRIGHT](https://arxiv.org/abs/2407.12883);
- [RAGChecker](https://arxiv.org/abs/2408.08067);
- [RAGAS](https://aclanthology.org/2024.eacl-demo.16/);
- [ARES](https://aclanthology.org/2024.naacl-long.20/);
- [GaRAGe](https://aclanthology.org/2025.findings-acl.875/).

These references are planning signals. They are not canonical RKM claims until
reviewed records, evidence, and references are added through the normal data
workflow.

## Coordinated implementation program

All items remain `PROPOSED`. Detailed task packets should be created only when
the preceding RAG product gate passes. This prevents a planning backlog from
becoming a substitute for product evidence.

### RKM-029 — Technique applicability profile

Objective:

- define the minimum machine-consumable applicability view for a RAG
  technique using existing RKM concepts wherever possible.

Depends on:

- GB-021 query transformation technique seed data;
- GB-027 external references pass;
- the Lab technique capability descriptor design from proposed RAG-046.

Acceptance gate:

- the view can answer stage, phase, prerequisites, failure modes, required
  metrics, cost dimensions, and evidence freshness for Tier 1 techniques;
- no new entity type is introduced without a failed concrete query.

### RKM-030 — Metric, benchmark, and dataset decision core

Objective:

- populate the minimum canonical knowledge needed to interpret retrieval,
  generation, citation, abstention, latency, cost, and dataset-sufficiency
  evidence.

Depends on:

- GB-022 evaluation metric seed data;
- GB-023 benchmark seed data;
- GB-024 dataset seed data;
- the Lab's proposed RAG-039 through RAG-041 measurement contracts.

Acceptance gate:

- every metric emitted by the first pilot resolves to a reviewed RKM record or
  an explicitly Lab-owned metric reference;
- benchmark and dataset scope cannot be confused with a universal claim.

### RKM-031 — Lab capability manifest consumer

Objective:

- validate a Lab capability manifest and expose the intersection of modeled,
  evidenced, and executable techniques.

Depends on:

- proposed RAG-042;
- RKM-029.

Acceptance gate:

- unknown implementations, unknown technique IDs, incompatible versions, and
  missing prerequisites fail closed;
- modeled-but-unavailable techniques remain distinguishable from executable
  candidates.

### RKM-032 — Corpus-profile candidate planner

Objective:

- produce a bounded, deterministic candidate experiment plan with explicit
  inclusion and exclusion rationale.

Depends on:

- proposed RAG-036, RAG-040, RAG-042, and RAG-043;
- RKM-029 through RKM-031.

Acceptance gate:

- identical semantic inputs produce byte-equivalent plans;
- the default bounds are six pipelines and three index profiles;
- every candidate is executable, evidence-linked, and tied to a measurable
  corpus hypothesis;
- unavailable or unsupported candidates cannot enter the executable plan.

### RKM-033 — Cross-experiment evidence memory

Objective:

- preserve comparable Lab observations without converting one local result
  into a universal technique claim.

Depends on:

- proposed RAG-044;
- existing recommendation decision and evidence projection contracts.

Acceptance gate:

- observations retain complete corpus, dataset, index, pipeline, model,
  metric, runtime, policy, and review provenance;
- aggregation requires explicit compatibility and policy;
- conflicting evidence remains visible.

### RKM-034 — Decision explanation

Objective:

- produce a human-readable and machine-readable explanation of applicability,
  evidence, Pareto position, cost, uncertainty, limitations, and lifecycle.

Depends on:

- proposed RAG-041, RAG-044, and RAG-045;
- RKM-032 and RKM-033.

Acceptance gate:

- a user can trace each recommendation or exclusion to external and local
  evidence;
- the report can return `INSUFFICIENT_EVIDENCE`;
- no production route or default is changed.

### RKM-035 — Internal decision-intelligence package

Objective:

- prepare the next internal package around a demonstrated corpus-to-decision
  workflow rather than schema count.

Depends on:

- GB-038 `v0.2.0` planning;
- GB-039 release readiness matrix;
- a successful RAG clean-checkout usability trial.

Acceptance gate:

- the package includes validated Tier 1 technique knowledge, metric semantics,
  capability and candidate-plan contracts, one replayable pilot decision, and
  consumer instructions;
- compatibility and migration expectations are explicit;
- publication and tagging remain human-authorized.

### RKM-036 — Enterprise constraint vocabulary and feasibility view

Objective:

- define the smallest reusable decision view for private installation,
  workspace policy, authorization dimensions, egress, retention, audit, and
  read-only connector constraints without duplicating runtime enforcement.

Depends on:

- ADR-0038 and the companion Lab RAG-052 contract;
- a concrete consumer query that existing RKM policy and relationship models
  cannot answer.

Acceptance gate:

- a candidate plan can identify a hard policy conflict and explain the
  exclusion deterministically;
- existing policy, capability, claim, and relationship concepts are reused
  unless a failed query demonstrates a missing first-class concept;
- no authentication credential, access-control list, source content, or
  runtime enforcement state is stored in RKM.

### RKM-037 — Policy-aware experiment and decision provenance

Objective:

- preserve the non-sensitive policy identity, egress decision, authorization
  evaluation status, and audit evidence required to interpret a Lab result.

Depends on:

- proposed RAG-053 through RAG-057;
- RKM-036.

Acceptance gate:

- an observation distinguishes a policy-permitted result from an unavailable
  or policy-blocked candidate;
- no result can be reused across incompatible workspace-policy contexts;
- artifacts retain only non-sensitive identifiers and evidence summaries.

### RKM-038 — Enterprise decision-intelligence package

Objective:

- package one policy-aware, private-installation decision workflow after the
  synthetic authorization pilot and human security review.

Depends on:

- proposed RAG-058;
- RKM-036 and RKM-037;
- a completed financial-books decision-lab pilot.

Acceptance gate:

- the package explains both RAG tradeoffs and policy exclusions;
- no automatic production promotion or mutation authority exists;
- a consumer can reproduce the decision with approved local artifacts and
  without exposing source content or credentials.

## Existing backlog alignment

The following existing backlog items are directly product-aligned:

| Backlog item | Product role | Timing |
| --- | --- | --- |
| GB-021 | Tier 1 query-transformation knowledge | Before RKM-029 completion |
| GB-022 | Metric semantics | RKM-030 |
| GB-023 | Benchmark context | RKM-030 |
| GB-024 | Dataset context | RKM-030 |
| GB-027 | Primary-source grounding | Continuous, starting with Tier 1 |
| GB-038 | Next release planning | After a successful pilot |
| GB-039 | Release readiness | RKM-035 |
| GB-045 | Existing external evidence and recommendation persistence | Close or re-scope after the current projection boundary is reviewed |

The following items are valid but not on the immediate product critical path:

- GB-015 through GB-017 governance-file refinements;
- GB-019 embedding model breadth;
- GB-025 broad provider modeling;
- GB-026 general agentic RAG workflow modeling;
- GB-032 through GB-037 additional automation and backlog tooling;
- GB-041 changelog validation;
- GB-044 adaptive Codex execution routing.

They should not preempt RKM-029 through RKM-038 without a demonstrated blocker.

RKM-036 through RKM-038 are intentionally post-pilot. They must not preempt
Tier 1 technique knowledge, the financial-books decision workflow, or the
companion Lab authorization contract. They ensure that enterprise policy becomes
an explicit decision input after the product can already produce one measured,
human-reviewed result.

## Consumer acceptance scenarios

RKM decision intelligence is useful only when these scenarios work.

### Scenario A — Identifier-heavy technical corpus

The corpus profile reports many exact identifiers and short support queries.
RKM should:

- include dense naive as the baseline;
- consider lexical+dense hybrid retrieval;
- consider reranking when candidate noise is expected;
- explain why graph or hierarchical indexing is not initially justified;
- request identifier-focused metrics and cases.

### Scenario B — Long narrative corpus with global questions

The corpus profile reports long documents and global thematic questions. RKM
should:

- include a conventional baseline;
- identify contextual or hierarchical indexing as research candidates when
  executable;
- identify GraphRAG-like retrieval only when the Lab capability manifest and
  budget allow it;
- explain index construction cost and evidence limitations.

### Scenario C — Mixed query complexity

The pilot evidence reports that simple queries perform well while multi-step
queries fail. RKM should:

- preserve the cheap baseline;
- propose adaptive routing only when simple/complex classification can be
  evaluated;
- require route accuracy, end-to-end quality, latency, and cost evidence;
- avoid forcing every query through the most expensive path.

### Scenario D — Insufficient evidence

The user supplies ten near-duplicate questions and no unanswerable cases. RKM
should:

- reject a decision-grade recommendation;
- identify missing query archetypes and evidence;
- allow a smoke run;
- return `INSUFFICIENT_EVIDENCE`;
- avoid production-promotion language.

### Scenario E — Private-enterprise workspace isolation

The organization operates separate HR, business-intelligence, and billing-like
workspaces. A proposed candidate requires an external reranker, but the
workspace denies external egress. RKM should:

- mark the external candidate `INAPPLICABLE` rather than merely expensive;
- preserve the egress constraint and its evidence source;
- propose only implementations declared executable under the local-model
  capability manifest;
- require the Lab to prove no unauthorized content entered retrieval, context,
  answer, citation, memory, cache, or audit output;
- keep enforcement, identity, and source policy outside RKM.

### Scenario F — Structured business data

The corpus profile contains invoices, account records, and operational tables.
RKM should:

- identify when an exact structured-data query is more appropriate than vector
  retrieval;
- require a read-only connector capability and a policy-compatible data scope;
- avoid treating an unsupported transactional update as a RAG action;
- return `UNAVAILABLE` when the connected Lab does not implement the required
  structured query capability.

## Success measures

RKM reaches the first decision-intelligence milestone when:

- all Tier 1 techniques used in the pilot have reviewed applicability and
  evidence profiles;
- all decision-critical pilot metrics have explicit semantics;
- a versioned Lab capability manifest is consumed fail-closed;
- a corpus profile produces a bounded candidate plan;
- every candidate has an executable implementation, hypothesis, evidence
  reference, metric target, and budget estimate;
- a Lab result round-trips into a decision record with complete provenance;
- the report can explain selection, exclusion, uncertainty, and insufficient
  evidence;
- one clean-checkout consumer can reproduce the decision without maintainer
  interpretation;
- no automatic production change occurs.

## Decisions required before implementation

1. **Pilot domain** — the first corpus is the rights-scoped English financial
   books pilot; its human-reviewed golden set will drive Tier 1 knowledge work.
2. **Applicability representation** — decide whether existing technique,
   capability, policy, claim, and relationship structures answer the required
   queries before proposing a new schema.
3. **Metric ownership** — decide which metric identities are canonical RKM
   knowledge and which remain Lab-owned implementation metrics.
4. **Evidence review owner** — identify the human reviewer for primary-source
   claims added to Tier 1 records.
5. **Aggregation policy** — decide when two experiment observations are
   comparable enough to support a cross-corpus conclusion.
6. **Enterprise policy representation** — after the Lab RAG-052 contract,
   decide whether existing RKM policy and capability structures can express the
   required feasibility view before proposing a new schema.
7. **Release scope** — decide whether the next internal package is a full RKM
   `v0.2.0` candidate or a narrower decision-intelligence preview.

These decisions should be taken after the RAG runtime/evaluation parity task
and before RKM-029 is promoted to `READY`.

## Recommended next action

Do not begin a new RKM modeling campaign yet.

First execute the proposed RAG-034 runtime/evaluation parity task, followed by
the CLI and financial-books corpus-workspace gates. During those tasks, RKM
remains stable except for clarifications required by an existing contract.
After the Lab exposes concrete capability and corpus-profile fields, create the
RKM-029 task packet using those fields rather than speculative ones. Enterprise
constraint modeling remains deferred until the measured decision-lab pilot and
the Lab authorization contract establish a real consumer query.
