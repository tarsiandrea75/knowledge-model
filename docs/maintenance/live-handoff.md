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

Committed `HEAD`: `3b3036f3158dcebbe242cde8b278ae99dd301e5c`

Upstream: `origin/experiment/codex-director` at the same commit

Latest committed subject: `Add comprehensive RKM project handoff`

Protected local `main`: `e3e02681e287879e13819493b057e64a99b5c270`

Protected `origin/main`: `e3e02681e287879e13819493b057e64a99b5c270`

Commits on the operational branch after `main`: 79

The comprehensive handoff reports 78 commits after `main` because it was written before its own commit. Commit `3b3036f` adds the seventy-ninth branch commit.

### Uncommitted candidate state

The repository is not currently clean.

Sole staged path:

```text
A  docs/maintenance/live-handoff.md
```

The path does not exist in committed `HEAD`. It is an uncommitted candidate undergoing semantic review and must not be treated as canonical until accepted, committed, validated, and published.

The exact whole-file SHA-256 of each candidate is recorded in its external run summary and independent-review baseline. A file cannot stably embed its own whole-file digest without changing that digest.

### Reported recovery and validation state

The last committed cockpit state before this candidate was reported as `NO_RECOVERY_NEEDED`.

For the live-handoff candidate, run summary 28 reports:

- exact one-file staged scope;
- identical worktree and index bytes;
- cached whitespace check success;
- full `make validate` success;
- candidate SHA-256 `31f03440185dc773ba1ec4d7183c330be81af866e8ed7d61852611ad2209c445`;
- 269 lines.

Those are attributed run claims, not substitutes for current read-only verification.

## Last Completed Published Operation

Task: Memgraph artifact-license correction

Reported summary version: `24`

Result: `SUCCESS`

Validation: `PASS`

Independent review: `ACCEPT`

Commit and published branch tip for that operation: `913e04fb41dc645e1eae3942b26a222bf54f50cd`

Exact semantic change:

```text
data/vector-databases/memgraph.json
metadata.license:
LicenseRef-Memgraph-Edition-Dependent -> Apache-2.0
```

The operation did not invent `vectorDatabase.productLicensing`. All other JSON values and formatting were reported preserved.

The current repository still records Memgraph as `Draft` and `Not Reviewed`. The artifact-license correction did not approve the entire product record.

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
- recent artifact-license corrections for Amazon Neptune Analytics and Memgraph;
- the comprehensive project handoff.

Only Neo4j is currently an `Approved` VectorDatabase record. The other 16 remain `Draft` and `Not Reviewed` unless a later canonical lifecycle transition proves otherwise.

## Open Tactical Issue

`data/vector-databases/pinecone.json` currently records:

```json
"license": "Proprietary"
```

The inherited release-readiness plan identifies this as the remaining artifact-license placement anomaly.

The proposed bounded correction is:

```text
metadata.license:
Proprietary -> Apache-2.0
```

This must preserve product-level prose describing Pinecone as a proprietary managed service. It must not add `vectorDatabase.productLicensing` without a separate evidence-backed task.

This is the next proposed tactical operation only after the live-handoff addition is accepted, committed, and published.

## Strategic Fork After the Pinecone Correction

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

Status: Accepted collaboration decision; repository adoption remains pending until commit and publication.

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

Status: Accepted.

Decision:

Close the known Pinecone artifact-license anomaly as the proposed next tactical correction after this handoff is adopted. Choose Track A, B, or C only through an explicit product-owner decision.

Rationale:

The Pinecone correction is defined and narrow. The broader branch direction is a product decision and must not be selected implicitly by automation.

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

## Current Review History

### Formatting wrapper failure

An earlier wrapper created and validated the candidate, then stopped at `git diff --cached --check` because 18 Markdown hard-break lines contained trailing spaces.

Whitespace recovery is complete:

- the 18 trailing spaces were removed;
- worktree and index were identical;
- `git diff --cached --check` passed;
- run summary 28 reported `make validate` passed.

### Independent semantic review

Exactly one independent read-only Reviewer reviewed candidate SHA-256:

```text
31f03440185dc773ba1ec4d7183c330be81af866e8ed7d61852611ad2209c445
```

The Reviewer returned `STOP`.

The blocking findings were:

- unsafe and incomplete authority precedence;
- external run summaries ranked above canonical repository contracts;
- maintainer-specific conventions presented too globally;
- update protocol incompatible with the one-file rule;
- stale claim that the current worktree was clean;
- incomplete attribution of run and validation evidence;
- obsolete continuation instructions after whitespace recovery.

This revision addresses those findings. It has not yet received an independent verdict.

## Exact Continuation Point

Current bounded operation:

```text
Add docs/maintenance/live-handoff.md
```

Current state:

- the file is the sole staged path;
- it is not present in committed `HEAD`;
- the preceding candidate received independent `STOP`;
- this revised candidate addresses all seven required corrections;
- no commit or push is authorized yet.

Exact next action:

1. verify the revised one-file candidate and protected refs;
2. run `git diff --cached --check`;
3. run full repository validation;
4. obtain one independent read-only review of the revised candidate;
5. commit and publish only if the verdict is `ACCEPT`.

After successful adoption of the live handoff, the proposed next bounded repository operation is the Pinecone artifact-license correction.
