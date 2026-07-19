# Graph Plus Vector Independent Review Adjudication

## Historical adjudication and current-state notice

> **Historical scope.** This historical, commit-bound adjudication is bound to
> commit `2979527681323a0704396b69afcdeed2c43e61ad` and to the historical Neo4j
> content identified by Git blob `24082b87e8ae4aafe17aa7abd6d00a101c25e828`
> and SHA-256 `8f59da948793cf956c78d1c5754608b4d38983b9d82b14d7640f17d12ccc85b7`.
> Its `Not Reviewed`, `Changes Requested`, `REVISION REQUIRED`, and “must not
> become `Approved` before re-review” language describes that historical review
> and remediation stage. Those statements, together with the original findings,
> review-state transitions, blocking requirements, correction plan, approval
> preconditions, and conclusions below, remain authoritative historical evidence
> and must not be interpreted as Neo4j's present lifecycle state. This
> adjudication remains authoritative for its pinned baseline and is not erroneous
> merely because later commits satisfied its conditions.
>
> **Current Neo4j state.** The required corrections and independent re-review
> were subsequently completed. Neo4j is currently version `1.5.1` with review
> state `Approved`. The canonical JSON record,
> [data/vector-databases/neo4j.json](../../../data/vector-databases/neo4j.json),
> is the authority for the current lifecycle state. That current record is bound
> to SHA-256 `6ea8eb9ac34d995c3759a71ce7cf43e7c8ee6445947720bbb71354b3bb473e55`,
> Git blob `c98ac1e352e216b712ccd2f3cdd84d9f9b986d82`, and approval commit
> `a617864fff7f56b25f3a37ab259d727275648de4`.
>
> **Acceptance provenance and related snapshot.**
> [docs/reviews/vector-databases/neo4j-1.5.1-independent-acceptance.md](neo4j-1.5.1-independent-acceptance.md)
> records the durable independent acceptance, findings disposition, and approval
> chain; this adjudication itself does not constitute that later acceptance.
> The related historical Reviewer Pack,
> [docs/reviews/vector-databases/independent-reviewer-pack.md](independent-reviewer-pack.md),
> is likewise a historical, pinned comparison snapshot.
>
> **Approval scope.** Neo4j's current approval implies no approval for the other
> sixteen `VectorDatabase` records.

## Purpose

This document adjudicates three independently produced review reports for the
RKM Graph plus vector batch.

It does not replace the original reports, perform a fourth product review, or
authorize immediate mutation of the canonical records. Its purpose is to decide:

- which review conclusions are accepted;
- which conclusions are accepted only with semantic reframing;
- which conclusions require further direct verification;
- which proposed corrections are not adopted;
- which changes must precede record-level corrections.

## Repository baseline

- Branch: `experiment/dataset-expansion`
- Adjudication baseline commit:
  `2979527681323a0704396b69afcdeed2c43e61ad`
- Records under review:
  - `data/vector-databases/neo4j.json`
  - `data/vector-databases/amazon-neptune-analytics.json`
  - `data/vector-databases/memgraph.json`
- Record status at review time: `Draft`
- Review state at review time: `Not Reviewed`
- Review date: July 17, 2026

## Source review reports

Three externally produced Markdown reports were supplied for adjudication:

1. A detailed 551-line review containing a source register, finding-level
   analysis, four additional findings, record verdicts, and a batch verdict.
2. A 332-line review covering RV-001 through RV-019, two additional findings,
   record verdicts, and a batch verdict.
3. A 295-line review covering RV-001 through RV-019, record verdicts, and a
   batch verdict.

The original reports must be preserved unchanged in the review audit trail.

## Adjudication method

The three reports are not treated as interchangeable votes.

A conclusion receives greater weight when it:

- identifies the exact product subsystem and capability origin;
- distinguishes product core, edition, managed service, first-party package,
  embedded component, cloud platform, host infrastructure, and application
  orchestration;
- cites a canonical or primary source;
- preserves version, deployment, plan, region, and preview qualifiers;
- distinguishes a hard factual contradiction from a schema or vocabulary
  defect;
- retains uncertainty where the public evidence is incomplete;
- proposes a correction narrower than the evidence.

Agreement among all three reports is strong corroboration, but numerical
majority does not override a more precise source-backed analysis.

The two shorter reports have materially overlapping structures, conclusions,
and corrective recommendations. They are valuable corroborating inputs, but
their agreement is not treated as two fully independent votes when they
conflict with the more granular source analysis.

## Global adjudication verdict

- **Graph plus vector batch:** `REVISION REQUIRED`
- **Neo4j:** `REVISION REQUIRED`
- **Amazon Neptune Analytics:** `REVISION REQUIRED`
- **Memgraph:** `REVISION REQUIRED`

The three records must remain `Draft`.

After the adjudication and original review reports are accepted into the audit
trail, their review state may change from `Not Reviewed` to
`Changes Requested`.

None may change to `Approved` until blocking corrections have been applied and
a new independent review has accepted the corrected records.

## Finding adjudication

### RV-001 — Supported Modalities

- **Decision:** `ACCEPTED WITH REFRAMING`
- **Reason:** All reviewers agree that the recorded modality list conflates
  numeric embeddings with native source-media processing.
- **Accepted conclusion:** The databases index numeric vectors whose source
  modality is determined primarily by an external embedding and ingestion
  pipeline.
- **Not adopted:** Replacing the list mechanically with only `Text`.
- **Required next decision:** Define whether the field means:
  - embedding-source provenance;
  - common workload usage;
  - native ingestion and processing;
  - or separate explicit properties for each concept.
- **Record mutation status:** Blocked until the semantic definition is chosen.

### RV-002 — Pre-filter Support

- **Decision:** `ACCEPTED WITH QUALIFICATION`
- **Reason:** Neo4j and Neptune document query-time candidate restriction;
  Memgraph does not document equivalent arbitrary dynamic pre-filtering.
- **Required qualification:**
  - distinguish dynamic query-time filtering from static index scope;
  - record the applicable API;
  - record supported predicates;
  - record index-definition requirements;
  - record minimum version or language level.
- **Not adopted:** Treating the current booleans as fully equivalent across
  products.

### RV-003 — Post-filter Support

- **Decision:** `ACCEPTED WITH QUALIFICATION`
- **Reason:** All three products can compose filtering after vector retrieval,
  but the stage and implementation boundary differ.
- **Required qualification:**
  - database-side versus application-side;
  - filtering stage;
  - candidate over-fetch behavior;
  - risk of returning fewer than the requested top-k results.
- **Not adopted:** Treating all three `true` values as proof of identical
  vector-index functionality.

### RV-004 — Hybrid Search Support

- **Decision:** `ACCEPTED AS A SEMANTIC MODEL DEFECT`
- **Reason:** The current representation merges:
  - dense plus sparse or lexical fusion;
  - vector plus full-text fusion;
  - vector plus graph traversal;
  - graph expansion after vector retrieval;
  - first-party package orchestration;
  - application-side composition.
- **Required correction:** Separate method and capability origin.
- **Preferred taxonomy direction:**
  - `denseSparseFusion`;
  - `vectorLexicalFusion`;
  - `vectorGraphComposition`;
  - `graphAugmentedRetrieval`;
  - `applicationOrchestratedFusion`.
- **Record mutation status:** Blocked until canonical terminology is resolved.

### RV-005 — Score Normalization

- **Decision:** `DEFERRED PENDING CAPABILITY-BOUNDARY DECISION`
- **Reason:** The reports disagree because they apply different scopes.
- **Accepted evidence:** Neo4j first-party GraphRAG material documents score
  normalization in a hybrid retriever.
- **Accepted limitation:** This does not establish a DBMS-core query-planner
  normalization primitive.
- **Required decision:** Determine whether RKM product capabilities include:
  - DBMS core only;
  - optional first-party packages;
  - or any vendor-supported workflow.
- **Not adopted:**
  - unqualified confirmation of `false`;
  - unqualified replacement with `true`.

### RV-006 — Horizontal Scaling

- **Decision:** `ACCEPTED`
- **Hard correction:** Neptune Analytics `High` is not supported by the
  documented m-NCU resizing and replica model.
- **Additional semantic problem:** `High`, `Medium`, and `Variable` lack
  measurable product-neutral criteria.
- **Required correction:**
  - separate read scaling, write scaling, data sharding, replicas, vertical
    resizing, and maximum documented topology;
  - scope Neo4j sharded scale-out to the applicable edition or offering;
  - replace Memgraph editorial ranking with explicit facts.
- **Not adopted:** Blindly replacing Neptune with `Medium` before the scale
  rubric is defined.

### RV-007 — Sharding Support

- **Decision:** `ACCEPTED WITH QUALIFICATION`
- **Accepted conclusion:**
  - Neo4j sharding is edition or offering specific;
  - no documented product-level sharding was established for one Neptune
    Analytics graph;
  - no documented product-level sharding was established for Memgraph.
- **Required correction:** Neo4j must not expose an unqualified product-wide
  `true`.
- **Additional requirement:** Verify vector-index behavior within the applicable
  Neo4j sharded topology.

### RV-008 — Replication Support

- **Decision:** `ACCEPTED WITH QUALIFICATION`
- **Accepted conclusion:** All three expose a replica or replication concept.
- **Semantic problem:** The current booleans erase:
  - synchronous versus asynchronous behavior;
  - read and write roles;
  - provider-managed versus customer-controlled topology;
  - edition availability;
  - routing and failover behavior;
  - vector-index replication semantics.
- **Required correction:** Preserve positive support only with explicit scope.

### RV-009 — Disk-backed Indexing

- **Decision:** `DEFERRED AS AN UNDEFINED FIELD`
- **Reason:** The current boolean may mean persistence, direct disk search,
  memory mapping, rebuildability, spill, or provider-managed durability.
- **Required correction:** Define separate properties for:
  - persistence across restart;
  - full-memory residency requirement;
  - direct on-disk or memory-mapped ANN;
  - rebuild source;
  - provider-managed physical architecture;
  - documented memory constraints.
- **Not adopted:** Treating opaque managed-service internals as conclusively
  `false`.

### RV-010 — Consistency Model

- **Decision:** `ACCEPTED AS A SEMANTIC MODEL DEFECT`
- **Reason:** One aggregate `Configurable` value merges different subsystems.
- **Required correction:** Model at least:
  - graph mutation isolation;
  - vector-index update visibility;
  - same-transaction visibility;
  - read-your-writes behavior;
  - replica consistency;
  - causal or session guarantees;
  - text-index visibility when relevant.
- **Not adopted:** Confirmation of `Configurable` based only on general
  deployment or routing choices.

### RV-011 — Transaction Support

- **Decision:** `ACCEPTED WITH REFRAMING`
- **Accepted conclusion:** Neo4j `Full ACID` is too broad when used as a single
  description of graph mutations and vector-index visibility.
- **Also accepted:**
  - Neptune vector changes have explicitly limited atomicity and isolation;
  - Memgraph vector-index isolation differs from ordinary graph transactions.
- **Required correction:** Separate:
  - graph/property transaction support;
  - vector-index transaction support;
  - same-transaction visibility;
  - rollback and durability behavior.
- **Not adopted:** Automatically changing Neo4j to aggregate `Limited` before
  the schema distinguishes the two scopes.

### RV-012 — Access Control

- **Decision:** `ACCEPTED AS A RUBRIC DEFECT`
- **Reason:** `High` and `Variable` are not reproducible without a scoring
  standard.
- **Required correction:** Record explicit capabilities:
  - authentication;
  - cloud-resource IAM;
  - database roles;
  - graph, label, property, or subgraph authorization;
  - federation or SSO;
  - service accounts;
  - edition and deployment scope.
- **Not adopted:** Treating AWS IAM as automatically equivalent to fine-grained
  database-native authorization.

### RV-013 — Encryption

- **Decision:** `ACCEPTED AS A FACTUAL AND RUBRIC DEFECT`
- **Reason:** The identical `High` value conflates:
  - encryption in transit;
  - encryption at rest;
  - host-volume encryption;
  - provider-managed encryption;
  - customer-managed keys;
  - backup encryption;
  - default behavior;
  - operator responsibility.
- **Required correction:** Decompose the capability and add direct
  product-specific evidence.
- **Specific caution:** Memgraph transport encryption evidence must not be
  treated as proof of universal native at-rest encryption.
- **Not adopted:** Blanket confirmation that all three provide equivalent
  robust at-rest encryption.

### RV-014 — Backup and Restore

- **Decision:** `ACCEPTED AS A RUBRIC DEFECT`
- **Reason:** All three have recovery mechanisms, but managed snapshots,
  online enterprise backup, offline dump/load, WAL, and externally orchestrated
  backup are not equivalent.
- **Required correction:** Record:
  - backup type;
  - online or offline behavior;
  - point-in-time recovery;
  - retention;
  - restore target;
  - edition or plan;
  - operator responsibility;
  - vector-index inclusion or rebuild behavior.

### RV-015 — Observability

- **Decision:** `ACCEPTED AS A RUBRIC DEFECT`
- **Reason:** Metrics, logs, tracing, profiling, audit events, dashboards,
  alarms, and provider integrations are collapsed into one undefined level.
- **Required correction:** Decompose observability and identify defaults,
  edition restrictions, and vector-index-specific telemetry.
- **Not adopted:** Blanket confirmation of equivalent `High` observability.

### RV-016 — Multi-tenancy

- **Decision:** `ACCEPTED AS A RUBRIC DEFECT`
- **Reason:** `Variable` provides no decision-grade information.
- **Required correction:** Record:
  - isolation unit;
  - namespace model;
  - authorization boundary;
  - resource quotas;
  - noisy-neighbor controls;
  - administrative boundary;
  - product-native versus infrastructure-enforced isolation;
  - edition or plan.

### RV-017 — Claim Count

- **Decision:** `ACCEPTED`
- **Reason:** Five claims per record are mechanically uniform despite materially
  different products and evidence boundaries.
- **Required correction:** Split compound claims into independently falsifiable
  propositions and allow counts to vary naturally.
- **Important qualification:** Claim count itself is not a quality metric.

### RV-018 — Evidence Count

- **Decision:** `ACCEPTED`
- **Reason:** The one-evidence-object-per-claim pattern is mechanically uniform
  and encourages broad evidence summaries over compound claims.
- **Required correction:**
  - permit multiple evidence objects per claim;
  - permit narrowly scoped evidence;
  - include contrary and limiting evidence;
  - map each source to the proposition it supports.
- **Important qualification:** Evidence count itself is not a quality metric.

### RV-019 — Residual Limitation Count

- **Decision:** `ACCEPTED WITH CORRECTION`
- **Accepted conclusion:** The repeated total of ten reflects a templated
  evidence-level pattern.
- **Correction to the shorter reports:** The Reviewer Pack count is reproducible
  as five evidence objects with two residual limitations each. It is not the
  top-level `vectorDatabase.limitations` array count.
- **Actual top-level limitation counts:**
  - Neo4j: eight;
  - Neptune Analytics: eight;
  - Memgraph: nine.
- **Required correction:** Rename or define the compared metric so readers know
  which limitation collection is counted. Remove fixed per-evidence quotas.
- **Not adopted:** Treating the Reviewer Pack count as a simple factual error.

## Additional finding adjudication

### ADD-001 — Reviewer Pack baseline mismatch

- **Decision:** `ACCEPTED AS A PROVENANCE DEFECT`
- **Observed identifiers:**
  - comparison baseline inside the pack:
    `74ca2d05ff02e051fafab189e0fcbc07892d3596`;
  - commit containing the added Reviewer Pack:
    `2979527681323a0704396b69afcdeed2c43e61ad`.
- **Known repository history:** The later commit added the Reviewer Pack after
  the comparison feature commit.
- **Required correction:** State explicitly:
  - the commit from which comparison data were generated;
  - the commit that introduced the review artifact;
  - immutable hashes of the three reviewed JSON files.
- **Classification:** Provenance defect, not yet evidence that the three record
  contents changed between the commits.

### ADD-002 — Hybrid-retrieval vocabulary conflict

- **Decision:** `ACCEPTED`
- **Reason:** Dense plus sparse fusion and vector plus graph traversal are
  distinct retrieval architectures.
- **Required correction:** Resolve the canonical vocabulary before modifying
  the records.

### ADD-003 — Neptune Analytics distance-metric conflation

- **Decision:** `ACCEPTED`
- **Reason:** Indexed top-k ANN ranking and pairwise vector-distance procedures
  have different roles and must not share one undifferentiated metric list.
- **Required correction:** Separate:
  - ANN index ranking metrics;
  - exact or pairwise vector functions.
- **Record priority:** High.

### ADD-004 — Mutable source provenance

- **Decision:** `ACCEPTED`
- **Reason:** `current`, `latest`, and GitHub `main` URLs cannot reproduce
  version-sensitive claims indefinitely.
- **Required correction:** Prefer:
  - version-pinned documentation;
  - release-note anchors;
  - tags or source commits;
  - captured evidence hashes or archived evidence artifacts when immutable
    managed-service documentation is unavailable.

### ADD-005 — Neo4j license designation

- **Decision:** `REQUIRES DIRECT VERIFICATION`
- **Reported concern:** The Neo4j record may contain `Apache-2.0` while product
  editions use materially different licensing terms.
- **Required verification before adoption:**
  - inspect the exact canonical field and its intended semantic scope;
  - inspect current official licensing documentation;
  - confirm which schema values or composite expressions are allowed;
  - distinguish Community, Enterprise, Aura, drivers, and first-party packages.
- **Not adopted:** Automatically replacing the field with a proposed composite
  string without schema and product-scope verification.

### ADD-006 — Neptune vector-index provisioning constraint

- **Decision:** `ACCEPTED`
- **Reason:** The reviewed documentation indicates a constrained index lifecycle,
  including creation-time vector configuration and one vector index per graph.
- **Required correction:** Add the provisioning and migration consequences as
  explicit limitations or indexing considerations.

## Record-level adjudication

### Neo4j

- **Adjudicated verdict:** `REVISION REQUIRED`
- **Review state after audit-trail acceptance:** `Changes Requested`
- **Highest-priority corrections:**
  1. separate graph transactions from vector-index visibility;
  2. separate DBMS-core capabilities from GraphRAG package capabilities;
  3. scope sharding and horizontal scale by edition or offering;
  4. resolve score-normalization scope;
  5. qualify pre-filter support by version and index definition;
  6. replace aggregate operational ratings;
  7. verify licensing metadata;
  8. rebuild compound claims and evidence mappings.
- **Must not become:** `Approved` before re-review.

### Amazon Neptune Analytics

- **Adjudicated verdict:** `REVISION REQUIRED`
- **Review state after audit-trail acceptance:** `Changes Requested`
- **Highest-priority corrections:**
  1. remove unsupported `High` horizontal-scaling classification;
  2. separate ANN ranking metrics from pairwise vector functions;
  3. represent graph and vector consistency separately;
  4. qualify IAM, encryption, replicas, and observability;
  5. record vector-index provisioning constraints;
  6. classify physical disk backing as unknown when not publicly documented;
  7. rebuild compound claims and evidence mappings.
- **Must not become:** `Approved` before re-review.

### Memgraph

- **Adjudicated verdict:** `REVISION REQUIRED`
- **Review state after audit-trail acceptance:** `Changes Requested`
- **Highest-priority corrections:**
  1. distinguish static index scope from dynamic pre-filtering;
  2. separate graph transaction isolation from vector-index isolation;
  3. remove or qualify unsupported aggregate encryption claims;
  4. replace horizontal-scaling ranking with explicit replication and HA facts;
  5. separate vector-index memory behavior from graph durability and storage
     modes;
  6. qualify security, backup, audit, and multi-tenancy by edition;
  7. rebuild compound claims and evidence mappings.
- **Must not become:** `Approved` before re-review.

## Decisions that precede record mutation

The following shared semantic decisions must be made before editing the three
records:

1. Meaning of `supportedModalities`.
2. Canonical definition and subtypes of hybrid retrieval.
3. Capability-origin model:
   - core product;
   - edition;
   - managed plan;
   - first-party package;
   - embedded component;
   - cloud platform;
   - host infrastructure;
   - application logic.
4. Separation of graph consistency from vector-index visibility.
5. Separation of graph transactions from vector-index transactions.
6. Definition of disk-backed ANN indexing.
7. Replacement or calibration of `High`, `Medium`, `Low`, `Variable`, and
   `Unknown`.
8. Evidence granularity and non-mechanical claim/evidence mapping.
9. Version-pinned or hash-bound evidence provenance.

## Minimal implementation sequence

1. Preserve the three original reviewer reports unchanged.
2. Commit this adjudication as a separate audit artifact.
3. Correct Reviewer Pack provenance and bind the reviewed record hashes.
4. Decide and document shared semantic definitions.
5. Update schema or canonical documentation only where necessary and through a
   separate high-risk change.
6. Correct Neo4j first because it exposes the widest capability-origin boundary.
7. Correct Neptune Analytics next because its hard factual corrections are
   comparatively discrete.
8. Correct Memgraph using the same subsystem, edition, and operational criteria.
9. Regenerate comparisons and graph exports where affected.
10. Run full repository validation.
11. Perform a second independent factual and semantic review.
12. Change records to `Approved` only if the second review accepts all blocking
    corrections.

## Stop rule

This adjudication does not authorize immediate broad rewriting.

Do not:

- modify all three records in one unreviewed bulk operation;
- convert every disputed boolean mechanically;
- change lifecycle state to `Approved`;
- treat Reviewer agreement as proof without checking scope;
- alter high-risk schemas before the shared semantic decisions are explicit;
- discard contrary findings from the original reports.

The next repository change after this adjudication should address provenance or
one explicitly selected semantic definition, not all record corrections at once.
