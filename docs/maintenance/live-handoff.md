# RAG Knowledge Model: Live Handoff

## Purpose and Scope

This file is the mutable operational handoff for the RAG Knowledge Model (RKM).

It complements, but does not replace:

- repository governance;
- machine-enforced contracts and current implementation;
- committed canonical data and durable review artifacts;
- the comprehensive baseline document `rkm-project-handoff.md`.

The comprehensive handoff explains project history, architecture, capabilities, and repository-reading strategy in depth. This live handoff records the latest operational orientation, attributed run evidence, decisions, unresolved issues, and exact continuation point.

This file is a maintenance aid. It is not an architecture contract, product constitution, schema contract, task guide, validation authority, or substitute for live repository inspection.

## Repository Precedence

When sources disagree, use this order:

1. Andrea's current request defines the task and authorization boundary.
2. Root `AGENTS.md` defines repository-wide rules.
3. The nearest applicable local `AGENTS.md` defines area-specific rules.
4. The applicable task guide defines the operational procedure.
5. Schemas, registries, manifests, canonical source data, current implementation, validators, exporters, tests, and other machine-enforced contracts define executable repository behavior.
6. Committed canonical records and generated artifacts are authoritative only within their validated scope; uncommitted worktree or index content is a candidate, not canonical state.
7. Durable review artifacts are authoritative only for their pinned commit, digest, artifact, and review scope.
8. `rkm-project-handoff.md` and this live handoff provide maintenance orientation without overriding the sources above.
9. Uploaded or external run summaries provide attributed operational evidence. Their internal `SUMMARY_VERSION` identifies the run, but their claims must be reconciled with Git state, validation artifacts, and durable repository evidence.
10. Recollection and inference are last-resort orientation only.

Never reconcile a contradiction silently. Identify the conflicting sources, verify the applicable scope, and record the resolution.

## Current Operational Snapshot

Snapshot date: 2026-07-19

### Committed baseline

Operational branch: `experiment/codex-director`

Preparation baseline `HEAD`: `0ce57b54deca81a08ca4de5153a0b6ceb3453d0f`

Preparation baseline upstream: `origin/experiment/codex-director` at the same commit

Latest committed subject at preparation time: `Correct data-record task guide target`

Protected local `main`: `e3e02681e287879e13819493b057e64a99b5c270`

Protected `origin/main`: `e3e02681e287879e13819493b057e64a99b5c270`

Commits on the operational branch after `main`: 83

The repository was clean at this preparation baseline. The live handoff itself had already been committed and published at `6ea4d9310f8e7193cbd5b284fbfc8f843e8ce4e5`.

### Recently published sequence

The following four one-file operations were completed in order:

1. `6ea4d9310f8e7193cbd5b284fbfc8f843e8ce4e5` — add the canonical live handoff;
2. `71b2d02d542a057a0c9ce2bc0592f51554c7cea0` — correct the Pinecone artifact license;
3. `3d71f9371398e9b08e1ec15af50c6564640ccbb6` — correct the task router graph-export validation target;
4. `0ce57b54deca81a08ca4de5153a0b6ceb3453d0f` — correct the adding-data-records task-guide target.

Each operation reported full validation success, one independent read-only Reviewer verdict of `ACCEPT`, safe publication, protected `main`, and a clean final worktree.

These are attributed operational claims from external run summaries and review reports. Current Git state and executable repository contracts remain the source of truth.

## Last Completed Published Operation

Task: correct the graph-export validation target in the adding-data-records task guide

Reported summary version: `35`

Result: `SUCCESS`

Validation: `PASS`

Independent review: `ACCEPT`

Commit and published branch tip for that operation: `0ce57b54deca81a08ca4de5153a0b6ceb3453d0f`

Exact semantic change:

```text
docs/maintenance/task-guides/adding-data-records.md
incorrect data-prefixed graph-export validation target -> make graph-export-validate
```

The operation changed one string in one file. It aligned the guide with the public Makefile target and the already-corrected task router.

Immediately preceding related operations were:

- Pinecone artifact-license correction at `71b2d02d542a057a0c9ce2bc0592f51554c7cea0`;
- task-router correction at `3d71f9371398e9b08e1ec15af50c6564640ccbb6`.

No obsolete operational target reference remained under `docs`, `scripts`, or `Makefile` after the final operation.

## Current Repository Meaning

RKM is a governed, evidence-oriented, human-readable and machine-readable model of the Retrieval-Augmented Generation ecosystem.

The current experimental branch contains:

- the post-alpha RKM foundation from `main`;
- the implemented bounded Codex Director;
- a specification-complete but runtime-unimplemented Autonomous Product Director v2;
- 17 VectorDatabase records;
- VectorDatabase decision-query and comparison support;
- structured capability-origin and availability-scope modeling;
- deterministic graph exports;
- a deeply corrected and independently approved Neo4j record;
- recent artifact-license corrections for Amazon Neptune Analytics, Memgraph, and Pinecone;
- corrected alignment between the data-path task router, task guide, and public graph-export validation target;
- the comprehensive project handoff.

Only Neo4j is currently an `Approved` VectorDatabase record. The other 16 remain `Draft` and `Not Reviewed` unless a later canonical lifecycle transition proves otherwise.

## Completed Tactical and Governance Sequence

The inherited Pinecone artifact-license placement anomaly is closed.

`data/vector-databases/pinecone.json` now records:

```json
"license": "Apache-2.0"
```

The correction preserved product-level prose describing Pinecone as a proprietary managed service and did not add `vectorDatabase.productLicensing`.

During validation of that change, the routed data-prefixed graph-export validation target was found not to exist. Live inspection established that the public Makefile target is `make graph-export-validate`.

The mismatch was resolved in two separately authorized one-file operations:

1. `scripts/rkm-route-task.py` changed one routing string and two built-in self-test expectations;
2. `docs/maintenance/task-guides/adding-data-records.md` changed its single stale instruction.

The corrected router self-test, routing smoke test, agent-routing validation, graph-export validation, and full repository validation all reported success.

No known artifact-license placement anomaly from the inherited tactical plan remains open.

## Strategic Fork After the Pinecone Correction

The Pinecone correction and the discovered routing-governance defect are complete. No automation may choose the next strategic direction implicitly.

### Track A: Stabilize and Integrate

Review the experimental branch against `main` by product increment, synchronize stale consumer documentation, reconcile governance-backlog status, and decide whether the autonomous-loop specification and VectorDatabase expansion should land together.

This is the safest integration-oriented path.

### Track B: Continue Evidence-First VectorDatabase Work

Review one record or one bounded semantic family at a time, preserve capability and deployment scope, improve evidence granularity, and obtain independent read-only review before lifecycle changes.

### Track C: Implement Autonomous Product Director v2

This requires an explicit branch-baseline decision and protected incremental implementation. The v2 contract is detailed, but its runtime does not exist.

Automation must not select this strategic fork implicitly. Andrea retains the product-direction decision.

## Known Documentation Drift

The experimental branch contains stale or incomplete consumer-facing descriptions in areas including:

- `README.md`;
- `QUICKSTART.md`;
- `data/README.md`;
- data graph-export documentation;
- graph-export contract documentation;
- `docs/maintenance/assistant-handoff.md`;
- maturity documentation;
- governance backlog entry GB-020.

Historical alpha release notes must remain historical and must not be rewritten as though later branch features existed in `v0.1.0-alpha`.

## Portability Observation

The authoritative Memgraph run in Andrea's WSL reported full validation success.

A separate validation attempt against an uploaded archive in the assistant's isolated container stopped during fixture validation when the JSON Schema resolver attempted to reach an `rkm.org` URI. This does not establish a repository regression because the environment, dependency set, and network conditions differed.

Treat this only as an environment-specific observation. Reproduce it in the current authorized repository environment before creating a governance-backlog item.

## Maintainer-Specific Collaboration Preferences

The following are Andrea's working preferences. They are subordinate to the current human request, repository governance, applicable task guides, and the exact authorization boundary of each operation.

- Conversation is normally in Italian.
- Repository content and durable handoffs are normally in English.
- Commands target WSL2 Ubuntu and Bash unless Andrea requests otherwise.
- Prefer one modifying operation at a time.
- Safe grouped read-only checks are acceptable.
- Requested terminal commands should display complete output and save it to:

```text
/mnt/c/Users/andrea.tarsi/Desktop/DA_PASSARE_A_CHATGPT.txt
```

- Long operations should also write a compact summary to:

```text
/mnt/c/Users/andrea.tarsi/Desktop/DA_PASSARE_A_CHATGPT_RIEPILOGO.txt
```

- Deferred project ideas should be proposed for `docs/maintenance/governance-backlog.md`; modifying that file still requires compatible scope and authorization.
- Do not claim success without evidence.
- Use one independent read-only Reviewer for semantic acceptance when the governed workflow requires it.
- Commit only on `ACCEPT`.
- Publish through the repository's safe-push workflow.
- Protect `main` unless Andrea explicitly authorizes integration.

These preferences do not authorize extra file changes and do not override the repository's exactly-one-project-file protocol.

## Live-Handoff Update Protocol

A meaningful interaction creates an obligation to preserve its durable handoff delta, but it does not automatically authorize modifying this file during another bounded operation.

Capture the following when applicable:

1. verified branch, `HEAD`, upstream, protected refs, and worktree or index state;
2. operation completed or discussed;
3. decisions and their rationale;
4. attributed run, validation, and review evidence;
5. unresolved risks or contradictions;
6. exact next bounded action.

Apply the delta using one of these governance-compatible paths:

- include `docs/maintenance/live-handoff.md` only when the current human request and routed scope explicitly authorize it;
- otherwise preserve the delta in the external run summary and perform a later dedicated one-file live-handoff update;
- at a major milestone, reconcile accumulated deltas into a new comprehensive snapshot through a separately authorized operation.

Trivial acknowledgements need no durable delta. Uncommitted or unreviewed content must be labeled as candidate state.

## Decision Log

### LH-001 - Adopt a Two-Layer Handoff

Date: 2026-07-19

Status: Accepted and published in commit `6ea4d9310f8e7193cbd5b284fbfc8f843e8ce4e5`.

Decision:

- Keep `rkm-project-handoff.md` as the comprehensive baseline snapshot.
- Use `docs/maintenance/live-handoff.md` as the smaller mutable operational layer after repository acceptance.

Rationale:

- Rewriting the comprehensive document after every operational change would create excessive churn and contradiction risk.
- A concise live layer can remain current without replacing the complete architectural and historical explanation.
- A single mutable handoff file is easier to validate and review than multiple session logs.

### LH-002 - Preserve Meaningful Handoff Deltas Without Violating Scope

Date: 2026-07-19

Status: Accepted collaboration requirement.

Decision:

Preserve every meaningful project decision, rationale, state transition, unresolved issue, and exact next step, but modify the repository handoff only under a compatible authorization boundary and routed one-file operation.

Rationale:

A successor needs durable state, while repository governance forbids silently expanding another task's file scope.

### LH-003 - Separate Tactical Completion from Strategic Direction

Date: 2026-07-19

Status: Tactical correction completed; strategic choice remains pending.

Decision:

The Pinecone artifact-license anomaly was closed in commit `71b2d02d542a057a0c9ce2bc0592f51554c7cea0`. Choose Track A, B, or C only through an explicit product-owner decision.

Rationale:

The Pinecone correction was narrow and is now complete. The broader branch direction remains a product decision and must not be selected implicitly by automation.

### LH-004 - Do Not Use Trailing-Space Markdown Hard Breaks

Date: 2026-07-19

Status: Accepted.

Decision:

Use blank lines, paragraphs, lists, or other whitespace-clean Markdown structures instead of two trailing spaces for hard line breaks.

Rationale:

A wrapper reached the staging phase after full validation, but `git diff --cached --check` rejected 18 trailing-space hard breaks.

### LH-005 - Keep the Live Handoff Subordinate to Repository Governance

Date: 2026-07-19

Status: Accepted correction after independent review.

Decision:

The live handoff records orientation and attributed evidence only. It does not define competing authority, architecture, product, validation, or automation contracts.

Rationale:

The first semantic review returned `STOP` because the earlier authority order elevated live state and run summaries above repository governance and canonical contracts.

### LH-006 - Close Standard Input for Codex in Piped Wrappers

Date: 2026-07-19

Status: Accepted operational correction.

Decision:

Invoke `codex exec` with standard input redirected from `/dev/null` when the enclosing Bash script itself is streamed through standard input.

Rationale:

During run summary 28, `codex exec` consumed the remaining shell script from standard input. The independent Reviewer still returned `STOP`, but the wrapper did not execute its verdict parser and incorrectly reported `RESULT=SUCCESS` with `REVIEW_VERDICT=NOT_RUN`.

### LH-007 - Reconcile Routed Checks with Executable Make Targets

Date: 2026-07-19

Status: Accepted and implemented.

Decision:

When task-router output, task-guide prose, and executable Make targets disagree, verify the live Makefile contract, preserve the current bounded file scope, and correct each inconsistent source through separately authorized operations.

Rationale:

The Pinecone correction exposed a routed data-prefixed graph-export validation target that did not exist. The executable target was `make graph-export-validate`. Correcting the router and its self-tests first, then the task guide, restored alignment without contaminating the Pinecone commit or weakening validation.

## Current Review History

### Canonical live-handoff adoption

The first live-handoff candidate failed cached whitespace checks because 18 Markdown hard-break lines contained trailing spaces. After whitespace recovery, its first independent semantic review returned `STOP` for authority, attribution, scope, and stale-state problems.

The revised 392-line candidate with SHA-256:

```text
11ebe9d08ced4bd38dd1a3d3c67080b5c593c640d026e9a5beabbe34227664d5
```

resolved all seven findings. One independent read-only Reviewer returned `ACCEPT`, full validation passed, and the file was committed and published as `6ea4d9310f8e7193cbd5b284fbfc8f843e8ce4e5`.

### Pinecone artifact-license correction

One independent read-only Reviewer accepted the exact one-value change from `Proprietary` to `Apache-2.0`. Product-level proprietary-service evidence remained intact, `vectorDatabase.productLicensing` remained absent, full validation passed, and commit `71b2d02d542a057a0c9ce2bc0592f51554c7cea0` was published.

### Task-router correction

The router implementation and its built-in self-tests contained three references to the nonexistent data-prefixed graph-export validation target. The exact three-string replacement to `make graph-export-validate` passed router self-tests, a data-path smoke test, full validation, and one independent read-only review. Commit `3d71f9371398e9b08e1ec15af50c6564640ccbb6` was published.

### Adding-data-records task-guide correction

The task guide contained the final stale target reference. Its exact one-string replacement passed agent-routing validation, representative routing checks, full validation, and one independent read-only review. Commit `0ce57b54deca81a08ca4de5153a0b6ceb3453d0f` was published.

No obsolete operational target reference remained under `docs`, `scripts`, or `Makefile` after that operation.

## Exact Continuation Point

Preparation baseline:

```text
branch: experiment/codex-director
HEAD and upstream: 0ce57b54deca81a08ca4de5153a0b6ceb3453d0f
local main and origin/main: e3e02681e287879e13819493b057e64a99b5c270
worktree: clean
```

Current bounded operation:

```text
Synchronize docs/maintenance/live-handoff.md
```

This update must remain the sole repository file change, pass `make validate`, receive one independent read-only review, and be committed and published only on `ACCEPT`.

Upon successful publication of this update, no tactical operation is selected automatically.

The exact next project-level action is an explicit product-owner decision among:

1. Track A — stabilize and integrate;
2. Track B — continue evidence-first VectorDatabase work;
3. Track C — implement Autonomous Product Director v2.

Andrea retains that decision. Until he selects a track, automation must stop at orientation and verification rather than inventing a strategic continuation.
