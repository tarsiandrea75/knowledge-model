# RKM Autonomous Product Director Loop Contract

## Status and Authority

This document defines the machine-oriented runtime contract for the RKM
Autonomous Product Director.

It operationalizes the principles established by
`docs/maintenance/rkm-autonomous-product-director.md`.

The constitution defines why the autonomous system exists and what values,
boundaries, and responsibilities govern it.

This loop contract defines:

- runtime states;
- legal state transitions;
- structured handoff artifacts;
- required fields and value constraints;
- artifact ownership;
- immutability rules;
- scope enforcement;
- revision and replan counters;
- recovery behavior;
- terminal outcomes;
- finalization invariants;
- responsibilities of the future state validator.

Repository rules remain authoritative when they are stricter than this
contract.

## Contract Version

Every structured runtime artifact except `FINAL_REPORT.md` must include:

```text
contractVersion
```

The required value for the first implementation is:

```text
rkm-autonomous-loop/v1
```

A runtime artifact with another value must be rejected unless a later
repository change explicitly introduces and validates a compatible contract
version.

## Runtime Location

Every session must use a unique runtime directory below:

```text
/tmp/rkm-runs/
```

The session directory name must use this form:

```text
autonomous-product-director-<UTC timestamp>-<process identifier>
```

The timestamp must use:

```text
YYYYMMDDTHHMMSSZ
```

Runtime artifacts must never be written inside the repository.

The session directory must be created before the Product Director begins
observation.

The session directory must not be reused by another run.

## Required Runtime Artifacts

A complete successful session contains:

| Artifact | Owner | Created | Mutability |
| --- | --- | --- | --- |
| `RUN_STATE.json` | Launcher and Product Director | At initialization | Replaced atomically after each state transition |
| `OBSERVATION.json` | Product Director | During observation | Immutable after option generation begins |
| `OPTIONS.json` | Product Director | After diagnosis | Immutable after experiment selection |
| `DIRECTOR_DECISION.json` | Product Director | Before implementation | Immutable during corrective revisions |
| `WORKER_ASSIGNMENT.json` | Product Director | Before every Worker pass | One immutable file per Worker pass |
| `WORKER_RESULT.json` | Worker result recorder | After every Worker pass | One immutable file per Worker pass |
| `REVIEW_VERDICT.json` | Reviewer result recorder | After every review | One immutable file per review |
| `EXTERNAL_VERIFICATION.json` | Product Director | After publication | Immutable after finalization begins |
| `FINAL_REPORT.md` | Product Director | During finalization | Immutable after session completion |

Revision and replan runs must preserve previous handoff files.

When more than one Worker or Reviewer pass occurs, use numbered names:

```text
WORKER_ASSIGNMENT-01.json
WORKER_RESULT-01.json
REVIEW_VERDICT-01.json
WORKER_ASSIGNMENT-02.json
WORKER_RESULT-02.json
REVIEW_VERDICT-02.json
```

The unnumbered names are prohibited once a second pass exists.

## JSON Encoding Rules

Every JSON artifact must:

- be valid UTF-8;
- contain one top-level JSON object;
- use two-space indentation;
- end with one newline;
- contain no duplicate object keys;
- contain no comments;
- use ISO 8601 UTC timestamps ending in `Z`;
- use forward-slash repository-relative paths;
- use explicit empty arrays instead of omitted required arrays;
- use explicit `null` only where this contract permits it;
- contain no credentials, access tokens, passwords, private keys, or secrets.

Artifact updates must be atomic.

The writer must:

1. write the complete object to a temporary file in the same runtime directory;
2. validate the temporary JSON;
3. replace the destination using an atomic rename.

Partially written artifacts must never be treated as valid state.

## Shared Artifact Fields

Every JSON artifact must contain:

| Field | Type | Constraint |
| --- | --- | --- |
| `contractVersion` | string | Must equal `rkm-autonomous-loop/v1` |
| `sessionId` | string | Must equal the session identifier in `RUN_STATE.json` |
| `artifactType` | string | Must match the artifact being represented |
| `createdAtUtc` | string | Valid ISO 8601 UTC timestamp |
| `createdBy` | string | One of the permitted owners for that artifact |
| `baselineCommit` | string | Forty-character lowercase Git object identifier |
| `branch` | string | Must equal `experiment/autonomous-product-director` |

The permitted `createdBy` values are:

```text
launcher
product-director
worker-recorder
reviewer-recorder
external-verifier
```

## Runtime States

The first implementation recognizes these non-terminal states:

```text
INITIALIZING
OBSERVING
DIAGNOSING
GENERATING_OPTIONS
SELECTING_EXPERIMENT
DEFINING_ACCEPTANCE
IMPLEMENTING
INSPECTING_WORK
REVIEWING
REVISING
REPLANNING
VALIDATING
COMMITTING
PUBLISHING
VERIFYING_EXTERNALLY
FINALIZING
```

The first implementation recognizes these terminal states:

```text
COMPLETED
ESCALATED
STOPPED
FAILED
INTERRUPTED
```

State names are case-sensitive.

No implementation may invent additional states without changing this contract
and its validator together.

## Legal State Transitions

The legal normal path is:

```text
INITIALIZING
OBSERVING
DIAGNOSING
GENERATING_OPTIONS
SELECTING_EXPERIMENT
DEFINING_ACCEPTANCE
IMPLEMENTING
INSPECTING_WORK
REVIEWING
VALIDATING
COMMITTING
PUBLISHING
VERIFYING_EXTERNALLY
FINALIZING
COMPLETED
```

The following corrective transitions are legal:

| From | To | Condition |
| --- | --- | --- |
| `REVIEWING` | `REVISING` | Reviewer returned `REVISE` and revision budget remains |
| `REVISING` | `IMPLEMENTING` | A corrective Worker assignment has been recorded |
| `REVIEWING` | `REPLANNING` | Reviewer returned `STOP`, recovery succeeded, and replan budget remains |
| `IMPLEMENTING` | `REPLANNING` | Selected experiment proved infeasible and recovery succeeded |
| `VALIDATING` | `REVISING` | Validation failure is repairable within unchanged scope and revision budget remains |
| `VERIFYING_EXTERNALLY` | `REVISING` | External verification exposed a repairable defect within unchanged scope |
| `REPLANNING` | `SELECTING_EXPERIMENT` | Previous experiment history is preserved and another candidate is eligible |

The following terminal transitions are legal from any non-terminal state when
their conditions are satisfied:

| To | Condition |
| --- | --- |
| `ESCALATED` | Human authorization or product ownership decision is required |
| `STOPPED` | No safe experiment remains or an explicit stop condition applies |
| `FAILED` | Repository state, contract state, validation, or recovery cannot be trusted |
| `INTERRUPTED` | An external interrupt was received and orderly shutdown completed |

A state transition not listed in this contract is invalid.

## State Transition Preconditions

Before entering `OBSERVING`:

- the runtime directory exists;
- the branch is correct;
- the upstream is correct;
- the worktree is clean;
- the branch is aligned with upstream;
- local `main` and `origin/main` have been recorded;
- the baseline commit has been recorded;
- no child agent is active.

Before entering `GENERATING_OPTIONS`:

- `OBSERVATION.json` exists and validates;
- at least one diagnosed gap is recorded;
- repository facts and Product Director inferences are distinguished.

Before entering `SELECTING_EXPERIMENT`:

- `OPTIONS.json` exists and validates;
- at least two materially different options exist, or a valid single-option
  justification is recorded;
- no option silently requires unauthorized protected-category work.

Before entering `IMPLEMENTING`:

- `DIRECTOR_DECISION.json` exists and validates;
- acceptance criteria are non-empty;
- authorized paths are non-empty;
- prohibited paths are recorded;
- validation commands are recorded;
- external verification steps are recorded;
- revision and replan budgets are recorded;
- no implementation file has changed since the baseline or latest accepted
  commit;
- exactly one Worker assignment exists for the pass being started.

Before entering `REVIEWING`:

- the Worker process completed;
- the Worker result is valid;
- the complete diff has been inspected by the Product Director;
- all changed paths are authorized;
- no secret or temporary runtime artifact entered the repository;
- no child Worker remains active.

Before entering `VALIDATING`:

- the latest Reviewer verdict is `ACCEPT`;
- no unauthorized path is changed;
- the staged area is empty;
- the worktree contains only the reviewed diff.

Before entering `COMMITTING`:

- all required targeted checks passed;
- `make validate` passed;
- the latest Reviewer verdict is `ACCEPT`;
- acceptance criteria have been evaluated;
- protected refs remain unchanged;
- only authorized paths will be staged.

Before entering `PUBLISHING`:

- one accepted commit was created;
- the worktree is clean;
- the commit contains only authorized paths;
- the commit count remains within budget;
- local `main` and `origin/main` remain unchanged.

Before entering `VERIFYING_EXTERNALLY`:

- publication used `make safe-push`;
- the local branch and upstream branch point to the same commit;
- the external verification plan is recorded;
- a clean isolated consumer workspace can be created.

Before entering `FINALIZING`:

- no Worker or Reviewer remains active;
- external verification has either passed or a terminal failure reason has
  been recorded;
- the repository is clean or rejected work has been safely preserved and
  removed;
- protected refs have been checked;
- the stop reason and recommendation are known.

Before entering `COMPLETED`:

- `EXTERNAL_VERIFICATION.json` records `PASS`;
- every accepted commit is published;
- local branch and upstream are aligned;
- local `main` and `origin/main` remain unchanged;
- the repository is clean;
- `FINAL_REPORT.md` exists and is non-empty.

## RUN_STATE.json Contract

`RUN_STATE.json` is the authoritative state pointer for the session.

It must contain:

| Field | Type | Constraint |
| --- | --- | --- |
| shared fields | object members | All shared artifact fields are required |
| `state` | string | One recognized runtime state |
| `previousState` | string or null | Null only in `INITIALIZING` |
| `stateSequence` | integer | Starts at zero and increases by one per transition |
| `startAtUtc` | string | Session start timestamp |
| `updatedAtUtc` | string | Timestamp of the current state write |
| `softDeadlineAtUtc` | string | Start plus soft working limit |
| `hardDeadlineAtUtc` | string | Start plus hard watchdog limit |
| `mainCommitAtStart` | string | Protected local `main` commit |
| `originMainCommitAtStart` | string | Protected `origin/main` commit |
| `upstream` | string | Must equal `origin/experiment/autonomous-product-director` |
| `revisionCount` | integer | Zero through two |
| `replanCount` | integer | Zero through one |
| `acceptedCommitCount` | integer | Zero through three |
| `workerPassCount` | integer | Non-negative |
| `reviewPassCount` | integer | Non-negative |
| `activeAgentRole` | string or null | `worker`, `reviewer`, or null |
| `activeAgentId` | string or null | Both active-agent fields must be null together |
| `selectedOptionId` | string or null | Null before experiment selection |
| `currentAssignmentId` | string or null | Null when no Worker assignment is active |
| `latestVerdict` | string or null | `ACCEPT`, `REVISE`, `STOP`, or null |
| `stopReasonCode` | string or null | Required in terminal states except `COMPLETED` |
| `recommendation` | string or null | Required before finalization completes |
| `artifacts` | object | Maps artifact roles to runtime-relative file names |

The `artifacts` object must never contain repository paths.

The `stateSequence` value must make rollback or silent state rewriting
detectable.

## OBSERVATION.json Contract

`OBSERVATION.json` records the repository baseline and diagnosed gaps.

It must contain:

| Field | Type | Constraint |
| --- | --- | --- |
| shared fields | object members | All shared artifact fields are required |
| `observedCommit` | string | Must equal the session baseline commit |
| `repositoryClean` | boolean | Must be true |
| `upstreamAligned` | boolean | Must be true |
| `protectedRefs` | object | Contains local and remote `main` commits |
| `productEntryPoints` | array of strings | Non-empty |
| `consumerVisibleCapabilities` | array of objects | May be empty only with justification |
| `evidenceBackedCoverage` | array of objects | Records current evidence-backed surfaces |
| `validationBaseline` | array of objects | Command, exit code, and observed result |
| `documentationEntryPoints` | array of strings | Repository-relative paths |
| `recentProductCommits` | array of objects | Commit and subject |
| `repositoryFacts` | array of objects | Fact plus repository evidence |
| `directorInferences` | array of objects | Inference plus supporting facts |
| `diagnosedGaps` | array of objects | At least one gap |
| `availableSeconds` | integer | Positive |
| `budgetSummary` | object | Recorded budget facts and reserve |
| `observationConclusion` | string | Non-empty |

Each diagnosed gap must contain:

```text
gapId
category
affectedConsumer
currentLimitation
repositoryEvidence
consequence
protectedCategoryRequired
measurableWithinSession
```

Permitted gap categories are:

```text
product
evidence
usability
correctness
infrastructure
```

## OPTIONS.json Contract

`OPTIONS.json` records materially different candidate experiments.

It must contain:

| Field | Type | Constraint |
| --- | --- | --- |
| shared fields | object members | All shared artifact fields are required |
| `sourceObservation` | string | Must name `OBSERVATION.json` |
| `options` | array of objects | Two or three options by default |
| `singleOptionJustification` | string or null | Required only when one option exists |
| `comparisonMethod` | string | Non-empty |
| `generatedAtStateSequence` | integer | Must match the generating state |

Every option must contain:

```text
optionId
title
productHypothesis
targetConsumerOutcome
repositoryEvidence
likelyAuthorizedPaths
expectedVerification
epistemicRisks
implementationRisks
compatibilityRisks
estimatedFileCount
estimatedWorkerPasses
protectedCategoryRequired
humanAuthorizationRequired
reversibility
selectionAdvantages
rejectionReasons
```

`optionId` values must be unique within the session.

An option requiring human authorization may be recorded but must not be
selected without explicit authorization.

## DIRECTOR_DECISION.json Contract

`DIRECTOR_DECISION.json` is the immutable acceptance contract for one selected
experiment.

It must contain:

| Field | Type | Constraint |
| --- | --- | --- |
| shared fields | object members | All shared artifact fields are required |
| `decisionId` | string | Unique within the session |
| `selectedOptionId` | string | Must exist in `OPTIONS.json` |
| `selectionRationale` | string | Non-empty and comparative |
| `rejectedOptions` | array of objects | Every non-selected option |
| `productHypothesis` | string | Observable and bounded |
| `authorizedPaths` | array of strings | Non-empty and unique |
| `prohibitedPaths` | array of strings | Non-empty |
| `requiredReadings` | array of strings | Repository-relative paths |
| `productAcceptanceCriteria` | array of objects | Non-empty |
| `epistemicAcceptanceCriteria` | array of objects | Non-empty |
| `compatibilityCriteria` | array of objects | Non-empty |
| `targetedChecks` | array of strings | Non-empty |
| `repositoryChecks` | array of strings | Must include `make validate` |
| `externalVerificationSteps` | array of objects | Non-empty |
| `revisionLimit` | integer | Zero through two |
| `replanLimit` | integer | Zero through one |
| `commitLimit` | integer | One through three |
| `stopConditions` | array of strings | Non-empty |
| `preferredCommitMessage` | string | Non-empty |
| `protectedCategoryAuthorization` | object or null | Required when protected paths are authorized |

Each acceptance criterion must contain:

```text
criterionId
description
verificationMethod
requiredOutcome
```

Corrective revisions must not alter this artifact.

A replan must produce a new numbered decision artifact while preserving the
previous one.

## WORKER_ASSIGNMENT Contract

Every Worker assignment must contain:

| Field | Type | Constraint |
| --- | --- | --- |
| shared fields | object members | All shared artifact fields are required |
| `assignmentId` | string | Unique within the session |
| `decisionId` | string | Must reference the active Director decision |
| `passNumber` | integer | Starts at one |
| `assignmentType` | string | `initial` or `corrective` |
| `objective` | string | One bounded task |
| `repositoryEvidence` | array of objects | Non-empty |
| `authorizedPaths` | array of strings | Must equal or be a strict subset of decision paths |
| `prohibitedPaths` | array of strings | Must include all non-authorized protected areas |
| `requiredReadings` | array of strings | Non-empty |
| `acceptanceCriteria` | array of strings | References decision criterion identifiers |
| `targetedChecks` | array of strings | Non-empty |
| `repositoryChecks` | array of strings | Must include `make validate` |
| `reviewFindingsToCorrect` | array of objects | Empty for initial assignments |
| `commitProhibited` | boolean | Must be true |
| `pushProhibited` | boolean | Must be true |
| `branchMutationProhibited` | boolean | Must be true |

A corrective assignment must preserve the active decision and authorized
scope.

## WORKER_RESULT Contract

Every Worker result must contain:

| Field | Type | Constraint |
| --- | --- | --- |
| shared fields | object members | All shared artifact fields are required |
| `assignmentId` | string | Matches the active assignment |
| `passNumber` | integer | Matches the assignment |
| `status` | string | `COMPLETED`, `BLOCKED`, `FAILED`, or `INTERRUPTED` |
| `taskUnderstood` | string | Non-empty |
| `changedPaths` | array of strings | Every observed changed path |
| `implementationSummary` | array of strings | Non-empty when status is `COMPLETED` |
| `commandsRun` | array of objects | Command, exit code, and result |
| `validationEvidence` | array of objects | Non-empty when validation was attempted |
| `acceptanceEvidence` | array of objects | Criterion identifier and observed result |
| `unresolvedRisks` | array of strings | Explicit array |
| `environmentLimitations` | array of strings | Explicit array |
| `reportedGitStatus` | array of strings | Exact reported status lines |
| `endedAtUtc` | string | Valid UTC timestamp |

A Worker result is invalid when:

- the result artifact is absent;
- required fields are absent;
- the status is `INTERRUPTED`;
- the Worker timed out;
- the Worker process failed before reporting;
- `changedPaths` differs from the Product Director's observed repository
  state;
- the result claims a successful command whose recorded exit code is non-zero;
- the result omits final Git status;
- the Worker committed, pushed, switched branches, or spawned another agent.

An invalid Worker result must never be reviewed or committed.

## REVIEW_VERDICT Contract

Every Reviewer verdict must contain:

| Field | Type | Constraint |
| --- | --- | --- |
| shared fields | object members | All shared artifact fields are required |
| `reviewId` | string | Unique within the session |
| `assignmentId` | string | References the reviewed assignment |
| `workerPassNumber` | integer | References the reviewed Worker pass |
| `verdict` | string | `ACCEPT`, `REVISE`, or `STOP` |
| `touchedPaths` | array of strings | Independently observed paths |
| `scopeCompliant` | boolean | Required |
| `acceptanceEvaluation` | array of objects | Every active criterion |
| `findings` | array of objects | Ordered by severity |
| `independentChecks` | array of objects | Commands and observed outcomes |
| `epistemicConcerns` | array of objects | Explicit array |
| `requiredCorrections` | array of objects | Required for `REVISE` |
| `stopReasons` | array of objects | Required for `STOP` |
| `commitRecommended` | boolean | True only for `ACCEPT` |
| `reportedGitStatus` | array of strings | Exact status lines |
| `endedAtUtc` | string | Valid UTC timestamp |

Permitted finding severities are:

```text
critical
high
medium
low
```

`ACCEPT` requires:

- `scopeCompliant` is true;
- every required acceptance criterion passes;
- no unresolved critical or high finding exists;
- `commitRecommended` is true;
- `requiredCorrections` is empty;
- `stopReasons` is empty.

`REVISE` requires:

- bounded corrections exist;
- required corrections remain inside unchanged authorized paths;
- the active decision remains valid;
- `commitRecommended` is false.

`STOP` requires:

- the current experiment should not be repaired as-is;
- `commitRecommended` is false;
- at least one stop reason exists.

## EXTERNAL_VERIFICATION.json Contract

External verification must contain:

| Field | Type | Constraint |
| --- | --- | --- |
| shared fields | object members | All shared artifact fields are required |
| `publishedCommit` | string | Commit verified in the isolated workspace |
| `publishedUpstream` | string | Experimental upstream branch |
| `workspacePath` | string | Absolute path below `/tmp` |
| `workspaceWasCleanClone` | boolean | Must be true |
| `checkoutMatchedPublishedCommit` | boolean | Must be true |
| `steps` | array of objects | Every planned verification step |
| `consumerOutputsInspected` | array of objects | Non-empty |
| `machineReadableOutputsValidated` | array of objects | Explicit array |
| `repositoryValidation` | object | Command, exit code, and result |
| `workspaceCleanAfterVerification` | boolean | Must be true |
| `acceptanceCriteriaResults` | array of objects | Every product criterion |
| `result` | string | `PASS` or `FAIL` |
| `failureReasons` | array of strings | Empty only for `PASS` |
| `completedAtUtc` | string | Valid UTC timestamp |

A `PASS` result requires every mandatory step and acceptance criterion to pass.

External verification must not modify the primary repository.

## FINAL_REPORT.md Contract

`FINAL_REPORT.md` is the human-facing session record.

It must contain these headings:

```text
# RKM Autonomous Product Director Session Report
## Mission
## Baseline
## Observation
## Diagnosed Gaps
## Candidate Options
## Selected Experiment
## Acceptance Contract
## Implementation History
## Review History
## Validation
## External Verification
## Commits and Changed Paths
## Epistemic Limitations
## Remaining Risks
## Branch Publication State
## Recommendation
## Stop Reason
## Final Git State
```

The final report must distinguish:

- repository facts;
- Product Director inferences;
- Worker claims;
- Reviewer findings;
- directly observed validation results;
- externally verified consumer results.

The report must not claim success when `EXTERNAL_VERIFICATION.json` records
`FAIL`.

The report may recommend:

```text
PROMOTE
CONTINUE_EXPERIMENT
REVISE_WITH_HUMAN_DIRECTION
DISCARD
NO_PROMOTION_DECISION
```

The report must never perform promotion.

## Artifact Ownership and Immutability

Only the Product Director may create:

```text
OBSERVATION.json
OPTIONS.json
DIRECTOR_DECISION.json
WORKER_ASSIGNMENT-<pass>.json
EXTERNAL_VERIFICATION.json
FINAL_REPORT.md
```

The launcher initializes `RUN_STATE.json`.

The Product Director replaces `RUN_STATE.json` only through legal transitions.

Worker and Reviewer natural-language responses must be captured by the Product
Director into the corresponding structured result artifacts without changing
their substantive meaning.

Once an artifact becomes immutable, later corrections must create a numbered
successor rather than overwrite history.

A corrective Worker pass must not overwrite the preceding assignment, result,
or review.

A replan must not overwrite the previous options or decision history.

## Scope Enforcement

The Product Director must determine changed paths independently using Git.

The authoritative changed-path set is derived from repository state, not from
the Worker report.

Every changed path must:

- be repository-relative;
- be listed in the active assignment;
- be listed in or permitted by the active decision;
- comply with routed `AGENTS.md` rules;
- comply with protected-category authorization.

A mechanically required additional path is unauthorized unless the active
decision explicitly permitted that category of generated or contract-required
change.

Unauthorized scope requires immediate stop unless:

- no commit has occurred;
- the path can be safely preserved outside the repository;
- the path can be restored without destructive Git commands;
- repository integrity can be proven afterward.

## Revision Counters

`revisionCount` counts corrective Worker passes after the initial pass.

The first implementation permits values:

```text
0
1
2
```

A transition into `REVISING` when `revisionCount` already equals two is
invalid.

A corrective revision must preserve:

- decision identifier;
- selected option;
- product hypothesis;
- authorized paths;
- prohibited paths;
- acceptance criteria;
- external verification plan.

## Replan Counters

`replanCount` counts complete experiment reselections.

The first implementation permits values:

```text
0
1
```

A second replan is invalid.

A replan must preserve:

- the original observation;
- all prior candidate options;
- failed decision artifacts;
- Worker and Reviewer history;
- rejection evidence;
- diagnostic patches and status records.

## Commit Counters

`acceptedCommitCount` counts commits created by the Product Director during the
session.

The first implementation permits values from zero through three.

Every accepted commit must:

- correspond to one accepted bounded task;
- contain only authorized paths;
- pass staged whitespace validation;
- pass required targeted checks;
- pass `make validate`;
- use a repository-oriented commit message;
- be published only through `make safe-push`.

## Agent Lifecycle Rules

At most one Worker and one Reviewer thread may exist at the same time.

Only one write-capable agent may be active.

A Reviewer may start only after the Worker has stopped and the Product
Director has inspected repository state.

Before finalization:

- every Worker must be stopped;
- every Reviewer must be stopped;
- every completed agent thread must be closed;
- `activeAgentRole` and `activeAgentId` must both be null.

Ambiguous agent state requires `FAILED` or `INTERRUPTED`.

## Invalid Worker Recovery

For an invalid Worker result:

1. do not start a Reviewer;
2. do not stage, commit, or push;
3. preserve the complete diff and status below a unique diagnostic directory
   under `/tmp/rkm-runs/`;
4. restore only assignment-authorized tracked paths;
5. preserve and remove only assignment-authorized untracked paths;
6. verify that previous accepted commits remain intact;
7. verify protected refs;
8. stop with `WORKER_RESULT_INVALID`.

The following commands are prohibited during recovery:

```text
git reset --hard
git clean -fd
git checkout .
```

## Reviewer STOP Recovery

For a Reviewer `STOP`:

1. preserve the current diff and status;
2. record the stop reasons;
3. determine whether the overall mission remains valid;
4. determine whether safe path-specific restoration is possible;
5. restore only active assignment paths;
6. verify repository cleanliness and protected refs;
7. replan only when the replan budget and complete-cycle budget remain;
8. otherwise enter `STOPPED`.

Rejected work must never be committed.

## Protected Ref Invariants

The session must record at initialization:

```text
mainCommitAtStart
originMainCommitAtStart
```

At every commit, publication, external verification, and finalization boundary:

- local `main` must equal `mainCommitAtStart`;
- local `origin/main` must equal `originMainCommitAtStart`.

Any difference requires immediate `FAILED` unless the difference is proven to
be a harmless local remote-tracking refresh that still points to the same
commit recorded at session start.

The autonomous system must not update, merge, switch to, or push `main`.

## Deadline and Reserve Invariants

The first session uses:

```text
soft working limit: 110 minutes
finalization reserve: 10 minutes
hard watchdog limit: 120 minutes
```

No new Worker assignment may begin after the soft deadline.

When the finalization reserve begins, the Product Director may only:

- finish or abandon the active bounded pass;
- stop agents;
- preserve diagnostics;
- validate already accepted work;
- publish already accepted commits;
- perform external verification when enough time remains;
- finalize the report.

## Terminal Reason Codes

Permitted stop and failure reason codes are:

```text
MISSION_COMPLETED
NO_SAFE_EXPERIMENT
HUMAN_AUTHORIZATION_REQUIRED
PRODUCT_STRATEGY_DECISION_REQUIRED
EXPERIMENT_REJECTED
REVISION_BUDGET_EXHAUSTED
REPLAN_BUDGET_EXHAUSTED
VALIDATION_FAILED
EXTERNAL_VERIFICATION_FAILED
WORKER_RESULT_INVALID
REVIEWER_STOP
UNAUTHORIZED_SCOPE
PROTECTED_REF_CHANGED
UNSAFE_BRANCH_STATE
UNSAFE_UPSTREAM_STATE
REPOSITORY_STATE_AMBIGUOUS
AGENT_STATE_AMBIGUOUS
BUDGET_INSUFFICIENT
SOFT_DEADLINE_REACHED
HARD_TIMEOUT
USAGE_LIMIT
ENVIRONMENT_ERROR
EXTERNAL_INTERRUPT
```

`COMPLETED` must use `MISSION_COMPLETED`.

`ESCALATED` must use either:

```text
HUMAN_AUTHORIZATION_REQUIRED
PRODUCT_STRATEGY_DECISION_REQUIRED
```

`INTERRUPTED` must use:

```text
EXTERNAL_INTERRUPT
```

## Finalization Invariants

A successful finalization requires:

- no active agents;
- a clean primary repository;
- every accepted commit published;
- experimental branch aligned with upstream;
- protected refs unchanged;
- valid required artifacts;
- external verification result `PASS`;
- complete final report;
- explicit recommendation;
- terminal state `COMPLETED`;
- stop reason `MISSION_COMPLETED`.

A stopped or failed finalization requires:

- no active agents when controllable;
- diagnostic preservation;
- no rejected commit;
- no unreviewed push;
- protected refs checked;
- explicit terminal reason;
- final report describing the incomplete outcome.

Stopping safely is preferable to manufacturing a successful result.

## State Validator Responsibilities

The planned `scripts/rkm-autonomous-state.py` validator must provide:

```text
initialize
validate-artifact
validate-session
transition
summarize
self-test
```

The validator must:

- reject unknown contract versions;
- reject unknown artifact types;
- reject malformed JSON;
- reject missing required fields;
- reject illegal states;
- reject illegal transitions;
- reject counter overflow;
- reject inconsistent session identifiers;
- reject inconsistent baseline commits;
- reject inconsistent branches;
- reject path escapes;
- reject repository paths in runtime artifact mappings;
- reject acceptance contracts created after implementation began;
- reject corrective revisions that alter immutable decisions;
- reject `ACCEPT` verdicts with failed criteria;
- reject external `PASS` results with failed steps;
- reject successful finalization without a clean repository;
- reject successful finalization without aligned publication;
- reject successful finalization when protected refs changed.

The validator must not:

- launch Codex;
- modify repository files;
- create commits;
- push branches;
- repair malformed artifacts silently;
- infer missing required values;
- rewrite immutable history.

## First Implementation Conformance Scenarios

The validator self-test must cover at least:

1. a valid complete session;
2. a valid `REVISE` loop followed by `ACCEPT`;
3. a valid single replan followed by `ACCEPT`;
4. a valid escalation for protected-category authorization;
5. rejection of an illegal transition;
6. rejection of a missing acceptance contract;
7. rejection of implementation before acceptance definition;
8. rejection of an unauthorized changed path;
9. rejection of revision count three;
10. rejection of replan count two;
11. rejection of commit count four;
12. rejection of a malformed Worker result;
13. rejection of an invalid Reviewer `ACCEPT`;
14. rejection of external verification `PASS` with a failed step;
15. rejection of completed state with changed protected refs;
16. rejection of completed state with an unclean repository;
17. rejection of completed state without a final report;
18. rejection of runtime artifacts written inside the repository.

## Compatibility Boundary

The first validator and launcher must implement this contract without changing:

- schemas;
- registries;
- graph contracts;
- data contracts;
- decision-query public behavior;
- the existing bounded Director;
- Worker configuration;
- Reviewer configuration;
- `main`.

A later implementation may revise this contract only through an explicit,
reviewed, validated repository change.
