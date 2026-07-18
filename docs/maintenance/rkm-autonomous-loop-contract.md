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
- revision, replan, and accepted-commit budgets;
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

The required value for this contract is:

```text
rkm-autonomous-loop/v2
```

A runtime artifact with any other value must be rejected. Version selection,
historical compatibility, and future migration rules are defined by the
Compatibility Boundary section.

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

The final session directory is published only by the Initialization Bootstrap
Transaction. Before that publication it must not exist. The adjacent private
staging directory used by that transaction is not a session directory and is
not discoverable as valid runtime state. The Product Director may begin
observation only after the complete initialized session directory has been
atomically published.

Neither a final session directory nor a staging directory may be reused by
another run. An existing final session directory makes initialization fail
closed.

## Initialization Bootstrap Transaction

This section is the sole normative authority for initial publication. It uses
one atomic initialization bundle and does not authorize a general same-state
`RUN_STATE.json` mutation rule.

Initialization proceeds exactly as follows:

1. The final session directory must not yet exist.
2. The launcher creates a private staging directory adjacent to the final
   session directory.
3. The exclusive Git observer produces `GIT_OBSERVATION-01.json` inside that
   staging directory.
4. The launcher produces the initial `RUN_STATE.json` in the same staging
   directory.
5. Both artifacts are validated together as one bootstrap bundle.
6. The bundle establishes `INITIALIZING` with `stateSequence: 0`.
7. `GIT_OBSERVATION-01.json` uses `createdAtState: INITIALIZING`,
   `createdAtStateSequence: 0`, `observedStateSequence: 0`, and
   `bootstrapInitialization: true`.
8. `RUN_STATE.json` maps `GIT_OBSERVATION-01.json`, records its artifact and
   observation identifiers, and contains the initialization transition-history
   entry for sequence zero.
9. Cross-identities, session ID, branch, baseline, repository root, protected
   refs, ancestry, timestamps, and artifact names must agree before
   publication.
10. After complete validation, the launcher atomically renames the staging
    directory to the final session-directory path.
11. No artifact is valid or discoverable at the final session path before that
    atomic directory publication.
12. A failed, interrupted, or partial bootstrap leaves no valid session. The
    staging directory is diagnostic debris, not a valid runtime session.
13. If the final session directory already exists, initialization fails
    closed.
14. After publication, all normal temporal and state-sequence rules apply.

This transaction is the sole narrow exception to the rule that an immutable
artifact's `createdAtState` and `createdAtStateSequence` refer to an already
published `RUN_STATE.json`. The exception applies only to
`GIT_OBSERVATION-01.json` inside this atomic bootstrap bundle and refers to the
simultaneously published initial `RUN_STATE.json`. It does not apply to later
Git observations, Worker or Reviewer artifacts, agent supervision,
validation, recovery, external verification, or any later transition.

The bundle must use either one common bootstrap publication timestamp for
`GIT_OBSERVATION-01.json.createdAtUtc`, the initialization
`transitionedAtUtc`, `startedAtUtc`, and `updatedAtUtc`, or an explicitly
ordered pair in which `observedAtUtc <= createdAtUtc` for the observation and
that `createdAtUtc` is no later than the equal initialization
`transitionedAtUtc`, `startedAtUtc`, and `updatedAtUtc` value. Both members and
all timestamps become visible only in the single atomic directory publication,
and neither arrangement may cite an impossible future state or sequence.

The bootstrap validator must reject a bundle with only `RUN_STATE.json`; only
`GIT_OBSERVATION-01.json`; mismatched session identity; mismatched sequence or
state other than `INITIALIZING`; a missing or non-true
`bootstrapInitialization`; publication at the final path before bundle
validation; non-atomic two-step publication; an existing final session
directory; interrupted staging publication; or staging debris presented as a
valid session. The public facade must never report a valid initialized session
from any partial bootstrap bundle.

## Required Runtime Artifacts

A complete successful session contains every mandatory artifact below and
every applicable attempt artifact. `RECOVERY_RECORD-01.json` is required only
when recovery was attempted; all other listed `-01` families occur on the
normal successful path.

| Artifact | Owner | Created | Mutability |
| --- | --- | --- | --- |
| `RUN_STATE.json` | Launcher and Product Director | In the atomic initialization bundle | Replaced atomically after each state transition |
| `OBSERVATION.json` | Product Director | During observation | Immutable after option generation begins |
| `OPTIONS.json` | Product Director | After diagnosis | Immutable after experiment selection |
| `DIRECTOR_DECISION-01.json` | Product Director | During acceptance definition | Immutable when published; atomically registered on entry to implementation |
| `GIT_OBSERVATION-01.json` | Git observer | In the atomic initialization bundle, then at every repository-sensitive checkpoint | One immutable file per observation |
| `WORKER_ASSIGNMENT-01.json` | Product Director | Before every Worker pass | One immutable file per Worker pass |
| `AGENT_SUPERVISION-01.json` | Agent supervisor | After every Worker or Reviewer process stops | One immutable file per supervised process event |
| `WORKER_RESULT-01.json` | Worker result recorder | After every Worker pass | One immutable file per Worker pass |
| `WORK_INSPECTION-01.json` | Product Director | After every Worker pass | One immutable file per inspection |
| `REVIEW_VERDICT-01.json` | Reviewer result recorder | After every review | One immutable file per review |
| `VALIDATION_RESULT-01.json` | Product Director | After every validation attempt | One immutable file per attempt |
| `RECOVERY_RECORD-01.json` | Product Director | After every recovery attempt | One immutable file per attempt |
| `EXTERNAL_VERIFICATION-01.json` | External verifier | After every external-verification attempt | One immutable file per attempt |
| `FINAL_REPORT.md` | Product Director | During finalization | Immutable after session completion |

Revision and replan runs must preserve previous handoff files.

Every repeatable artifact family is numbered from its first occurrence:

```text
WORKER_ASSIGNMENT-01.json
WORKER_RESULT-01.json
WORK_INSPECTION-01.json
REVIEW_VERDICT-01.json
WORKER_ASSIGNMENT-02.json
WORKER_RESULT-02.json
WORK_INSPECTION-02.json
REVIEW_VERDICT-02.json
AGENT_SUPERVISION-01.json
AGENT_SUPERVISION-02.json
GIT_OBSERVATION-01.json
GIT_OBSERVATION-02.json
VALIDATION_RESULT-01.json
VALIDATION_RESULT-02.json
RECOVERY_RECORD-01.json
EXTERNAL_VERIFICATION-01.json
```

Director decisions use the same rule:

```text
DIRECTOR_DECISION-01.json
DIRECTOR_DECISION-02.json
```

Within each family, numbers are two-digit, contiguous, begin with `01`, and
are never reused. Unnumbered names for repeatable artifacts are prohibited
from pass or attempt one. A later occurrence creates the next file; it must
never rename, replace, or overwrite an immutable first occurrence. Numbering
is independent between families. Worker assignment, result, and inspection
numbers correspond to their common Worker pass. Review numbering counts only
reviews: `REVIEW_VERDICT-01.json` is the first actual review even when an
earlier Worker pass ended before review. `workerPassNumber` links a review to
its Worker pass without making the review number equal that pass number.
Agent-supervision event numbering independently counts every supervised Worker
or Reviewer process in observed-stop order; `AGENT_SUPERVISION-01.json` is
always the first such event, regardless of role, pass number, or review number.
The first RUN_STATE and first Git observation are jointly required and become
valid only through the Initialization Bootstrap Transaction; neither is a
valid initialized-session fragment on its own.

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
- contain no credentials, access tokens, passwords, private keys, or secrets
  outside the unavoidable exact process bytes in `stdoutCapture` and
  `stderrCapture`; those runtime-only fields are governed by Embedded Process
  Stream Evidence and must never be copied into repository content.

Artifact updates must be atomic.

The writer must:

1. write the complete object to a temporary file in the same runtime directory;
2. validate the temporary JSON;
3. replace the destination using an atomic rename.

Partially written artifacts must never be treated as valid state.

## Shared Artifact Fields

Every JSON artifact contains these stable session fields:

| Field | Type | Constraint |
| --- | --- | --- |
| `contractVersion` | string | Must equal `rkm-autonomous-loop/v2` |
| `sessionId` | string | Must equal the session identifier in `RUN_STATE.json` |
| `artifactType` | string | Must match the artifact being represented |
| `baselineCommit` | string | Forty-character lowercase Git object identifier |
| `branch` | string | Must equal `experiment/autonomous-product-director` |

Every immutable structured JSON artifact additionally contains:

| Field | Type | Constraint |
| --- | --- | --- |
| `artifactId` | string | Unique across all immutable artifacts in the session |
| `createdAtUtc` | string | Valid ISO 8601 UTC timestamp |
| `createdBy` | string | One of the permitted owners for that artifact |
| `createdAtState` | string | Runtime state in which the artifact became immutable |
| `createdAtStateSequence` | integer | Exact authoritative sequence of `createdAtState` |

The permitted `createdBy` values are:

```text
launcher
product-director
worker-recorder
reviewer-recorder
external-verifier
git-observer
agent-supervisor
```

`createdAtState` and `createdAtStateSequence` use the authoritative
relationships defined in Temporal Semantics.

`RUN_STATE.json` is intentionally mutable and is not an immutable structured
artifact. It uses the stable session fields but not `artifactId`, `createdBy`,
`createdAtUtc`, `createdAtState`, or `createdAtStateSequence`; its initialization
and transition timestamps are governed by its own contract. This is the only
shared-field exception.

## Temporal Semantics

This section is the sole authority for relationships among runtime timestamps
and state sequences. Other sections specify which fields a family carries and
refer to these rules; they must not redefine the relationships.

- `createdAtUtc` is the timestamp at which a complete immutable artifact is
  atomically published at its final runtime-relative name.
- `createdAtState` is the state in effect at publication, and
  `createdAtStateSequence` equals the current authoritative
  `RUN_STATE.stateSequence`; neither may cite a future state or sequence.
- The sole exception is bootstrap `GIT_OBSERVATION-01.json`: its creation state
  and sequence refer to the simultaneously published initial RUN_STATE under
  Initialization Bootstrap Transaction. It is not valid before atomic bundle
  publication, and no other artifact or lifecycle point may use this
  exception.
- `GIT_OBSERVATION-<observation>.json` uses `observedAtUtc` and
  `observedStateSequence`. Its observation completes no later than publication,
  so `observedAtUtc <= createdAtUtc`, and
  `observedStateSequence == createdAtStateSequence`.
- A structured component-result envelope uses `observedAtUtc` for the component
  evaluation. When that envelope is published within an immutable artifact,
  its `observedAtUtc <= createdAtUtc`; a standalone in-memory envelope has no
  artifact creation timestamp.
- `WORKER_RESULT-<pass>.json` and `REVIEW_VERDICT-<review>.json` use
  `endedAtUtc`; `endedAtUtc <= createdAtUtc`.
- `AGENT_SUPERVISION-<event>.json` uses `processStartedAtUtc`,
  `processEndedAtUtc`, `observedStoppedAtUtc`, and
  `processInvocation.launchedAtUtc`. Their sole ordering is:

  ```text
  processInvocation.launchedAtUtc == processStartedAtUtc
  processStartedAtUtc <= processEndedAtUtc
  processEndedAtUtc <= observedStoppedAtUtc
  observedStoppedAtUtc <= createdAtUtc
  ```

  A Worker supervision is published in `IMPLEMENTING` before its bound Worker
  result; a Reviewer supervision is published in `REVIEWING` before its bound
  verdict. Its creation state and sequence equal the active process lifecycle
  state and sequence, and the bound result or verdict uses that same lifecycle
  state and sequence.
- `EXTERNAL_VERIFICATION-<attempt>.json` uses `completedAtUtc`;
  `completedAtUtc <= createdAtUtc`.
- When an artifact is published immediately from a completed process result,
  the applicable process `endedAtUtc` or `completedAtUtc` may equal, but must
  not exceed, `createdAtUtc`.
- Transition-history `transitionedAtUtc` values are strictly increasing.
  Artifact `createdAtUtc` values within one `createdAtStateSequence` are
  non-decreasing in creation order.
- An artifact authorizing a transition must be atomically published before
  that transition's `transitionedAtUtc`.
- After every completed transition, `RUN_STATE.updatedAtUtc` equals the latest
  transition-history `transitionedAtUtc`. At initialization, both equal
  `startedAtUtc`, subject to the common timestamp or ordered-pair rule in
  Initialization Bootstrap Transaction.

An artifact that violates any applicable relationship is invalid.

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

| From | To | Complete prerequisite evidence |
| --- | --- | --- |
| `REVIEWING` | `REVISING` | Latest exact numbered verdict is `REVISE`; authoritative supervision proves the Reviewer stopped and binds its still-present active identifiers to that durable verdict; corrections are bounded by the unchanged decision; the Budget Accounting entry check passes and is charged; Active Agent Lifecycle Rules govern the atomic clearing |
| `REVISING` | `IMPLEMENTING` | A fresh numbered corrective assignment references the exact immutable trigger; one Corrective Entry Context validates; the recorded revision charge for this operation matches the decision and trigger; Active Agent Lifecycle Rules govern Worker registration |
| `REVIEWING` | `REPLANNING` | Latest exact numbered verdict is `STOP`; authoritative supervision proves the Reviewer stopped and binds its still-present active identifiers to that durable verdict; rejected-work diagnostics and completed recovery are preserved; the Budget Accounting entry check passes and is charged; Active Agent Lifecycle Rules govern the atomic clearing |
| `INSPECTING_WORK` | `REPLANNING` | The authoritatively supervised Worker result has status `BLOCKED`; the numbered inspection confirms bounded experiment infeasibility; Worker fields were cleared only by entry into `INSPECTING_WORK`; diagnostics and completed recovery are preserved; the Budget Accounting entry check passes and is charged; no agent is active |
| `VALIDATING` | `REVISING` | A numbered `post-review` or `pre-commit` validation result records the failed command, exit code, diagnostic, and affected criterion; the defect is repairable inside unchanged scope; the Budget Accounting entry check passes and is charged; no agent is active |
| `VERIFYING_EXTERNALLY` | `REVISING` | The latest numbered external-verification result is immutable `FAIL` evidence with the exact defect and exact primary and isolated observations; the post-publication corrective context is feasible; the Budget Accounting entry check passes and is charged; no agent is active |
| `REPLANNING` | `SELECTING_EXPERIMENT` | The rejected decision and evidence remain immutable; safe recovery is complete; the recorded replan charge for the rejected decision and trigger is verified rather than capacity being checked again; at least one eligible recorded candidate remains; no agent is active |

Recovery evidence must identify the rejected decision and pass, preserved
diagnostic location, paths restored or removed by orchestration, commands and
exit codes, protected-ref comparison, and the exact authoritative Git
observation after recovery. A corrective assignment must be newly created
after the evidence that caused correction. It must reference the exact
immutable `REVIEW_VERDICT-<review>.json`, `VALIDATION_RESULT-<attempt>.json`,
`EXTERNAL_VERIFICATION-<attempt>.json`, `WORK_INSPECTION-<pass>.json`, or
`RECOVERY_RECORD-<attempt>.json` that requires the correction. An initial
assignment or any assignment created before that evidence is not reusable.

Replanning does not create a replacement decision before selection.
`REPLANNING` returns only to `SELECTING_EXPERIMENT` under the prerequisites in
the table. The replacement option is then selected, the normal
`SELECTING_EXPERIMENT` to `DEFINING_ACCEPTANCE` transition occurs, and its new
acceptance criteria are defined. Only in `DEFINING_ACCEPTANCE`, after the new
option and acceptance contract are complete, may the Product Director create
the next numbered Director decision and the fresh initial Worker assignment.
The subsequent `DEFINING_ACCEPTANCE -> IMPLEMENTING` transition performs the
atomic decision and initial-Worker registration defined below. The rejected
decision and digest remain immutable throughout.

### Atomic Decision And Initial Worker Registration

This subsection is the sole authority for the first
`DEFINING_ACCEPTANCE -> IMPLEMENTING` transition for each decision. Before the
transition, the complete numbered immutable Director decision and the fresh
numbered initial Worker assignment must exist, validate, and agree with the
selected option and acceptance definition. Their artifact names, artifact
identifiers, decision mapping, budget entry, assignment identifier, and Worker
identity are not required to be active or present in `RUN_STATE.json` before
the transition; pre-registration there is prohibited. No same-state
`RUN_STATE.json` rewrite is authorized.

The transition performs one atomic `RUN_STATE.json` replacement that, in this
order as one indivisible operation:

1. verifies and canonicalizes the complete immutable numbered Director
   decision;
2. calculates its complete canonical SHA-256 digest;
3. records `activeDecisionArtifact` and `activeDecisionDigest`;
4. appends the immutable `decisionDigests` mapping;
5. creates the zero-valued `decisionBudgetUsage` entry for the new decision;
6. verifies and registers the fresh initial Worker assignment and its unique
   Worker identity;
7. appends the decision and assignment artifact identifiers, `decisionId`,
   `assignmentId`, `workerAgentId`, and every other applicable identifier to
   its append-only used-identifier collection;
8. appends the transition-history entry with the exact decision and assignment
   evidence names;
9. advances `stateSequence` by one and enters `IMPLEMENTING`.

After the transition, every recorded digest, active pointer, decision mapping,
zero-valued budget entry, assignment mapping, Worker registration, used
identifier, artifact-array entry, and transition-history item must agree
exactly with the immutable decision, immutable assignment, canonical digest,
and transition evidence. Any partial registration, prior registration,
ordering substitution, stale mapping, or disagreement rejects the transition
atomically and leaves the previous `RUN_STATE.json` unchanged.

A Worker that discovers bounded experiment infeasibility reports `BLOCKED`,
then takes `IMPLEMENTING -> INSPECTING_WORK`. The Product Director publishes
the matching numbered inspection, preserves diagnostics, completes recovery
when required, and only then may take `INSPECTING_WORK -> REPLANNING`. A
`BLOCKED` pass is structurally valid but review-ineligible; it creates no
review artifact and does not increment `reviewPassCount`. `FAILED`,
`INTERRUPTED`, malformed, missing, or identity-mismatched results cannot use
this replan path.

Every orderly terminal outcome passes through `FINALIZING`. Any other
non-terminal state may enter it only after the intended disposition, reason,
recommendation, diagnostics, and finalization-entry preconditions are known;
the transition atomically records `terminalDisposition`.

Only these terminal transitions are legal:

| From | To | Condition |
| --- | --- | --- |
| `FINALIZING` | `COMPLETED` | Every successful-finalization invariant and completion precondition passes |
| `FINALIZING` | `ESCALATED` | Human authorization or a product-ownership decision is required and the escalation reason is recorded |
| `FINALIZING` | `STOPPED` | No safe experiment remains or an explicit stop condition applies |
| `FINALIZING` | `FAILED` | Repository, contract, validation, agent, or recovery state cannot be trusted |
| `FINALIZING` | `INTERRUPTED` | An external interrupt was received and orderly shutdown evidence was preserved |

Direct operational-to-terminal transitions are invalid. A process death that
prevents orderly finalization leaves an incomplete, non-terminal session.
Every transition not listed in this contract is invalid.

## State Transition Preconditions

Before entering `OBSERVING`:

- the complete initialization bundle was validated and atomically published at
  the previously absent final session path;
- the final directory contains both the mutually consistent initial
  `RUN_STATE.json` and `GIT_OBSERVATION-01.json`, and no staging directory is
  being treated as valid runtime state;
- `repositoryRoot` is present and matches the authoritative Git root;
- authoritative current branch and upstream are correct;
- authoritative staged, tracked-modified, and untracked path sets are empty;
- authoritative `HEAD` is aligned with upstream with zero ahead and behind;
- authoritative local `main` and `origin/main` have been recorded;
- authoritative local `main` and `origin/main` both resolve, equal
  `mainCommitAtStart` and `originMainCommitAtStart`, respectively, and are each
  proven ancestors of experimental `HEAD` by fresh merge-base ancestry checks;
- the authoritative `HEAD` baseline commit has been recorded;
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

Before the atomic decision and initial-Worker registration transition from
`DEFINING_ACCEPTANCE` to `IMPLEMENTING` for a decision:

- the complete numbered immutable Director decision exists and validates but
  is not yet active or registered in `RUN_STATE.json`;
- acceptance criteria are non-empty;
- authorized paths are non-empty;
- prohibited paths are recorded;
- validation commands are recorded;
- external verification steps are recorded;
- revision and replan budgets are recorded;
- the primary repository is clean relative to the baseline or latest accepted
  commit;
- authoritative staged, tracked-modified, and untracked path sets are empty;
- the authorized product-path union satisfies the six-file mission limit;
- exactly one fresh, unique numbered initial Worker assignment exists for the
  pass being started, validates, and is not yet registered in `RUN_STATE.json`;
- no prior Worker or Reviewer is active;
- all inputs required by Atomic Decision And Initial Worker Registration are
  complete, and that transition performs every registration and digest action.

Before a corrective transition from `REVISING` to `IMPLEMENTING`:

- the active numbered Director decision and its recorded digest remain
  unchanged;
- exactly one of the two Corrective Entry Contexts validates;
- the fresh corrective assignment references the exact immutable evidence
  that triggered correction and was created after it;
- the matching revision operation is already charged exactly once under
  Budget Accounting; no unused capacity is demanded again;
- no Worker or Reviewer is active before the transition;
- Worker registration satisfies Active Agent Lifecycle Rules.

Before entering `INSPECTING_WORK`:

- a fresh immutable `AGENT_SUPERVISION-<event>.json` authoritatively proves the
  Worker process stopped;
- the immutable numbered Worker result has been recorded;
- its `workerAgentId`, assignment identifier, and pass number match the active
  Worker registration and numbered assignment;
- the Worker result is bound to that exact supervision artifact, whose process
  identity, assignment, pass, invocation, outcome, exact captures, and digests
  match;
- Worker clearing satisfies Active Agent Lifecycle Rules.

Before entering `REVIEWING`:

- the Worker result status is exactly `COMPLETED`;
- authoritative supervision proves the Worker process stopped;
- the assignment identifier is unique across the session and matches the
  result;
- the assignment and result carry the same `workerAgentId` registered for the
  pass;
- the result names the exact fresh supervision artifact for that Worker,
  assignment, and pass;
- the pass number is unique, contiguous, and matches the assignment and
  result;
- the Product Director independently inspected the complete diff and recorded
  the immutable numbered `WORK_INSPECTION-<pass>.json`;
- authoritative Git changed paths exactly equal Worker-reported changed paths
  and are equal to the assignment paths or a valid subset of them;
- the authoritative staged path set is empty;
- pre-execution and post-execution Git observations show unchanged checkpoint
  commits, refs, branch identity, and upstream, with no unexpected persistent
  changed paths;
- no unauthorized untracked artifact, secret, or runtime artifact entered the
  repository;
- all changed paths remain within the active decision and assignment;
- Reviewer registration satisfies Active Agent Lifecycle Rules.

`BLOCKED`, `FAILED`, and `INTERRUPTED` Worker results must never enter
`REVIEWING`. A missing, timed-out, still-running, non-completed, or invalid
result must follow Non-Completed and Invalid Worker Recovery.

Before entering `VALIDATING`:

- the latest Reviewer verdict is `ACCEPT`;
- the transition out of `REVIEWING` satisfied Active Agent Lifecycle Rules,
  including stopped-process, durable-verdict, identity, and atomic-clear
  requirements;
- the Reviewer verdict names the exact fresh authoritative supervision artifact
  for that Reviewer and review;
- no unauthorized path is changed;
- the staged area is empty;
- the worktree contains only the reviewed diff.

Before entering `COMMITTING`:

- the latest applicable numbered validation results record that all required
  targeted checks and `make validate` passed;
- the latest Reviewer verdict is `ACCEPT`;
- acceptance criteria have been evaluated;
- protected refs remain unchanged;
- only authorized paths will be staged;
- the accepted-commit operation has positive remaining allowance under Budget
  Accounting;
- no accepted-commit charge exists for the new operation identifier;
- entering `COMMITTING` atomically registers one fresh
  `pendingCommitOperation` with the active decision and exact pre-charge usage.

Before entering `PUBLISHING`:

- one accepted commit was created during the registered pending operation;
- the worktree is clean;
- the commit contains only authorized paths;
- the pending operation, active decision, validation evidence, and exact commit
  match;
- relevant budget usage has not changed since pending-operation registration;
- the `COMMITTING -> PUBLISHING` transition atomically records the single
  accepted-commit charge, appends the commit to `acceptedSessionCommits`, and
  clears `pendingCommitOperation`;
- local `main` and `origin/main` remain unchanged.

Before entering `VERIFYING_EXTERNALLY`:

- publication used `make safe-push`;
- the local branch and upstream branch point to the same commit;
- the external verification plan is recorded;
- a clean isolated consumer workspace can be created.

Before entering `FINALIZING`:

- intended state, reason, recommendation, and applicable diagnostics are known;
- the transition records disposition, reason, and recommendation atomically;
- for a disposition other than `FAILED` or `INTERRUPTED`, authoritative
  supervision with verified invocation, exact captures, and digests proves
  every agent stopped and the agents are cleared; missing, unverifiable, or
  ambiguous supervision is preserved and permits only `FAILED` or
  `INTERRUPTED`;
- external-verification or incomplete-outcome evidence is recorded;
- rejected work is removed when possible, and trustworthy protected refs are
  checked.

Before entering a terminal state from `FINALIZING`:

- `FINAL_REPORT.md` is substantive and consistent;
- target state equals `terminalDisposition`;
- reason and recommendation are valid and non-null;
- no agent remains active when controllable;
- for `COMPLETED`, `STOPPED`, or `ESCALATED`, every Worker or Reviewer process
  relevant to the disposition has fresh identity-matched authoritative
  supervision with verified invocation, exact captures, and digests; for
  `FAILED` or `INTERRUPTED`, any absent, unverifiable, or ambiguous supervision
  is explicit failure evidence and is not replaced by self-attestation;
- the applicable finalization invariants pass.

Before entering `COMPLETED`:

- `repositoryRoot` is present and has been inspected authoritatively;
- the latest numbered external-verification artifact records `PASS`, and all
  external and acceptance criteria results pass;
- authoritative accepted-commit relationships match the recorded accepted
  session commits and `acceptedCommitCount`;
- every accepted commit is authoritatively published;
- authoritative local branch, upstream, and external published commit are the
  same commit, with zero ahead and behind;
- authoritative staged, tracked-modified, and untracked path sets are empty;
- authoritative local `main` and `origin/main` equal their initialization
  values;
- fresh authoritative `localMainIsAncestorOfHead` and
  `originMainIsAncestorOfHead` values are both true;
- no agent is active;
- `FINAL_REPORT.md` satisfies the substantive final-report contract and does
  not contradict structured runtime artifacts.

## Corrective Entry Contexts

Exactly two corrective-entry contexts exist. Every corrective assignment sets
`correctiveContext` to one of these values and must satisfy that context; no
hybrid or third context is valid.

### Retained Pre-Commit Diff

`retained-pre-commit-diff` applies after a review or validation failure and
before an accepted commit for that reviewed work. It requires:

- the authorized uncommitted diff to be preserved rather than cleaned;
- a fresh primary Git observation whose changed paths exactly equal the path
  set in the latest numbered work inspection and, when applicable, the durable
  review or validation evidence that triggered correction;
- every changed path to remain within the unchanged active decision and fresh
  corrective assignment, with an empty staged set and no unexpected untracked,
  secret, or repository-local runtime path;
- unchanged `HEAD`, branch, upstream, accepted session commits, local `main`,
  and `origin/main` across the applicable checkpoint observations.

### Post-Publication Clean Primary Repository

`post-publication-clean-primary` applies only after failed external
verification of an accepted published commit. It requires:

- the primary worktree to be clean relative to that accepted published commit,
  with empty staged, tracked-modified, untracked, and changed path sets;
- authoritative branch `HEAD`, upstream, and the failed verification's
  accepted published commit to be equal, and protected refs unchanged;
- the immutable failed `EXTERNAL_VERIFICATION-<attempt>.json` and its exact
  primary and isolated Git observations;
- a fresh corrective assignment, created after the failure evidence, that
  explicitly authorizes the corrective paths within the unchanged decision.

This context must not compare the clean primary path set with the earlier
pre-commit reviewed-diff path set. After Worker registration, the new Worker
may create a fresh diff only on the newly assigned authorized paths from the
clean accepted commit.

## RUN_STATE.json Contract

`RUN_STATE.json` is the authoritative state pointer for the session.

It must contain:

| Field | Type | Constraint |
| --- | --- | --- |
| shared stable fields | object members | Stable session fields are required; immutable creation fields do not apply |
| `state` | string | One recognized runtime state |
| `previousState` | string or null | Null only in `INITIALIZING` |
| `stateSequence` | integer | Starts at zero and increases by one per transition |
| `startedAtUtc` | string | Session initialization timestamp |
| `updatedAtUtc` | string | Timestamp of the current state write |
| `softDeadlineAtUtc` | string | Start plus soft working limit |
| `hardDeadlineAtUtc` | string | Start plus hard watchdog limit |
| `repositoryRoot` | string | Mandatory absolute canonical Git repository root |
| `mainCommitAtStart` | string | Protected local `main` commit |
| `originMainCommitAtStart` | string | Protected `origin/main` commit |
| `upstream` | string | Must equal `origin/experiment/autonomous-product-director` |
| `revisionCount` | integer | Zero through two |
| `replanCount` | integer | Zero through one |
| `acceptedCommitCount` | integer | Zero through three |
| `workerPassCount` | integer | Non-negative |
| `reviewPassCount` | integer | Non-negative |
| `activeAgentRole` | string or null | `worker`, `reviewer`, or null |
| `activeAgentId` | string or null | Role and identifier are null together; otherwise identity matches the active role |
| `selectedOptionId` | string or null | Null before experiment selection |
| `currentAssignmentId` | string or null | Null when no Worker assignment is active |
| `currentReviewId` | string or null | Null when no Reviewer is active |
| `activeDecisionArtifact` | string or null | Numbered decision file for the selected experiment |
| `activeDecisionDigest` | string or null | Lowercase SHA-256 digest of the canonical active decision |
| `decisionDigests` | object | Immutable mapping of every numbered decision file to its digest |
| `decisionBudgetUsage` | object | Mapping of every decision identifier to revision, replan, and accepted-commit usage |
| `budgetCharges` | array of objects | Append-only exact-once operation charges in chronological order |
| `acceptedSessionCommits` | array of strings | Ordered exact commits accepted and created during this session |
| `pendingCommitOperation` | object or null | Non-null only in `COMMITTING`; fresh operation identity, active decision, pre-commit `HEAD`, registration sequence, and exact pre-charge usage |
| `usedArtifactIds` | array of strings | Every immutable structured artifact identifier in creation order |
| `usedObservationIds` | array of strings | Every Git-observation identifier in creation order, beginning with the bootstrap observation |
| `usedDecisionIds` | array of strings | Every numbered decision identifier ever registered |
| `usedAssignmentIds` | array of strings | Every assignment identifier ever registered in creation order |
| `usedAgentIds` | array of strings | Every Worker and Reviewer agent identifier ever registered |
| `usedReviewIds` | array of strings | Every review identifier ever recorded |
| `usedSupervisionIds` | array of strings | Every agent-supervision identifier ever consumed |
| `usedSupervisionEventNumbers` | array of integers | Every supervision event number ever consumed, in order |
| `usedProcessHandles` | array of strings | Every supervised process handle ever consumed |
| `transitionHistory` | array of objects | Complete append-only history through the current state |
| `latestVerdict` | string or null | `ACCEPT`, `REVISE`, `STOP`, or null |
| `terminalDisposition` | string or null | Null before `FINALIZING`; in `FINALIZING` and terminal states, the exact intended or reached terminal state |
| `stopReasonCode` | string or null | Non-null in `FINALIZING` and every terminal state; `MISSION_COMPLETED` for `COMPLETED` |
| `recommendation` | string or null | Non-null in `FINALIZING` and every terminal state |
| `artifacts` | object | Maps artifact roles to runtime-relative file names |

The `artifacts` object must never contain repository paths.

Initialization is fail-closed and occurs only through Initialization Bootstrap
Transaction. In the adjacent private staging directory, `initialize` must
obtain the authoritative primary `GIT_OBSERVATION-01.json` in the intended
`INITIALIZING` context and construct the initial RUN_STATE around that same
evidence. Local `main` and `origin/main` must both resolve;
`mainCommitAtStart` and `originMainCommitAtStart` are copied from those exact
observed commits; and `localMainIsAncestorOfHead` and
`originMainIsAncestorOfHead` must both be true. The initial
`artifacts.gitObservations` array contains exactly
`GIT_OBSERVATION-01.json`; `usedArtifactIds` contains its `artifactId`; and
`usedObservationIds` contains its `observationId`. The initial transition
history contains exactly the sequence-zero initialization entry and names
that observation as evidence. All bootstrap cross-identities and timestamps
must validate together before the directory is published.

Failure to resolve a protected ref, disagreement with a protected value
supplied for the session, either false ancestry result, an incomplete or
inconsistent bundle, or a publication-rule violation rejects initialization
without a valid initialized RUN_STATE or valid session. No later replacement
of RUN_STATE may repair a partial bootstrap in place. Baseline observation
repeats the Git checks freshly before option generation.

Its scalar entries name `OBSERVATION.json`, `OPTIONS.json`, and
`FINAL_REPORT.md` when present. Its ordered array entries are `decisions`,
`gitObservations`, `workerAssignments`, `workerResults`, `workInspections`,
`agentSupervisions`, `reviewVerdicts`, `validationResults`, `recoveryRecords`,
and `externalVerifications`. Each array contains every immutable runtime-
relative file name for that family in numeric order from `-01`; no historical
entry may be removed when a later occurrence is appended. Transition-history
evidence names must resolve through these mappings.

After bootstrap, a new Git observation is consumed by the next legal
transition that depends on it. That transition atomically appends its file name
to `artifacts.gitObservations`, its `artifactId` to `usedArtifactIds`, and its
`observationId` to `usedObservationIds`. The complete immutable observation
must already exist and validate, but pre-registration through a same-state
RUN_STATE rewrite is prohibited.

Identifiers in `usedArtifactIds`, `usedObservationIds`, `usedDecisionIds`,
`usedAssignmentIds`, `usedAgentIds`, `usedReviewIds`, `usedSupervisionIds`, and
`usedSupervisionEventNumbers` are session-global and must never be removed or
reused. Values in `usedProcessHandles` are equally append-only and unique.
Worker and Reviewer agent identifiers share one namespace. Every assignment,
Worker result, Reviewer verdict, and agent-supervision identity must match the
applicable used-identifier sets. `activeDecisionDigest` must equal the mapping
entry for `activeDecisionArtifact`. Earlier decision digest mappings and
budget-usage entries must remain present after a replan.

Atomic Decision And Initial Worker Registration is the only way to add a new
active decision and its initial Worker to these fields. A newly published
agent-supervision artifact is consumed by the next legal transition that
depends on it; that transition atomically appends its file name to
`artifacts.agentSupervisions`, its `artifactId` to `usedArtifactIds`, its
`supervisionId` to `usedSupervisionIds`, and its `eventNumber` to
`usedSupervisionEventNumbers`, and its `processHandle` to
`usedProcessHandles`. Before that consuming transition, the complete
immutable supervision artifact must exist and validate, but those RUN_STATE
entries need not yet exist. This transition-time append is not a same-state
RUN_STATE rewrite.

Each `decisionBudgetUsage` member is keyed by immutable `decisionId` and must
contain non-negative integer `revisionUsage`, `replanUsage`, and
`acceptedCommitUsage` values. A new decision is added with all three values
zero. These per-decision values never reset or disappear, and the session-wide
`revisionCount`, `replanCount`, and `acceptedCommitCount` never reset.

Every `budgetCharges` entry has the fields required by Budget Accounting.
Counts and usage values must equal applicable charge-entry totals; a counter
mutation without its matching charge, or vice versa, is invalid.
`pendingCommitOperation` is registered on entry into `COMMITTING`, remains
unchanged there, and is cleared only by the atomic publishing charge or
terminal recovery preserving it diagnostically. `terminalDisposition` is null
before `FINALIZING`, then equals the intended and eventual terminal state.

Each `transitionHistory` entry must contain `stateSequence`, `fromState`,
`toState`, `transitionedAtUtc`, and the runtime-relative evidence artifact
names used for the transition. The initialization entry has
`stateSequence: 0`, `fromState: null`, `toState: INITIALIZING`, and
`transitionedAtUtc` equal to `startedAtUtc`. The array is append-only and is
replaced atomically as part of the complete `RUN_STATE.json` update.

The `stateSequence` value must make rollback or silent state rewriting
detectable. Every transition increases it by exactly one. Timestamp and
artifact-publication ordering is governed only by Temporal Semantics.

`OPTIONS.json.generatedAtStateSequence` and its
`createdAtStateSequence` must equal the actual `GENERATING_OPTIONS` sequence
recorded in transition history. Assignment, result, and inspection artifacts
are ordered by Worker pass: an assignment precedes its result, its result
precedes its inspection, and pass `N` finishes before assignment `N+1` is
created. A review, when eligible, follows its referenced inspection; review
numbers are independently contiguous and count actual reviews only. The
validator rejects out-of-order artifacts, skipped family numbers, and every
Temporal Semantics violation.

## Authoritative Git Observation

Repository-sensitive validation requires a fresh, read-only observation of
the applicable repository, recorded as the next immutable numbered
`GIT_OBSERVATION-<observation>.json`. `repositoryRoot` is mandatory for
initialization, every repository-sensitive artifact validation, every
repository-sensitive transition, session validation, and finalization.
`GIT_OBSERVATION-01.json` is initially produced only inside the private staging
directory and becomes authoritative only when its complete bootstrap bundle is
atomically published under Initialization Bootstrap Transaction. Every later
observation is published under the normal already-current RUN_STATE rules.

Each Git observation contains the immutable shared fields and:

| Field | Type | Constraint |
| --- | --- | --- |
| `observationId` | string | Unique within the session and linked one-to-one with `artifactId` |
| `observationNumber` | integer | Starts at one and is contiguous |
| `repositoryRole` | string | Exactly `primary` or `isolated-verification` |
| `repositoryRoot` | string | Absolute canonical root reported by Git |
| `workspaceId` | string or null | Required for `isolated-verification`; null for `primary` |
| `verificationId` | string or null | Required when associated with external verification |
| `purpose` | string | Non-empty lifecycle checkpoint purpose |
| `bootstrapInitialization` | boolean | Exactly `true` only for `GIT_OBSERVATION-01.json` in the initialization bootstrap bundle; exactly `false` otherwise |
| `observedStateSequence` | integer | Current authoritative state sequence at observation |
| `observedAtUtc` | string | UTC checkpoint timestamp |
| `currentBranch` | string | Exact branch observed at the checkpoint |
| `configuredUpstream` | string | Exact full upstream ref |
| `headCommit` | string | Exact `HEAD` commit |
| `upstreamCommit` | string | Exact configured-upstream commit |
| `localMainCommit` | string or null | Exact local protected-ref commit; primary requires a string, isolated may use null only when the ref is absent |
| `originMainCommit` | string | Exact remote-tracking protected-ref commit relevant to the observed repository |
| `localMainIsAncestorOfHead` | boolean | Exact merge-base result for primary `localMainCommit`, or for recorded `mainCommitAtStart` when an isolated workspace lacks the local ref, against `headCommit` |
| `originMainIsAncestorOfHead` | boolean | Exact merge-base result for `originMainCommit` against `headCommit` |
| `baselineCommitObserved` | string | Recorded session baseline resolved in this repository |
| `acceptedSessionCommitsObserved` | array of strings | Exact applicable accepted commits and relationships |
| `stagedPaths` | array of strings | Complete NUL-derived path set |
| `trackedModifiedPaths` | array of strings | Complete NUL-derived path set |
| `untrackedPaths` | array of strings | Complete NUL-derived path set |
| `changedPaths` | array of strings | Exact union of the three path sets |
| `aheadCount` | integer | Exact observed ahead count |
| `behindCount` | integer | Exact observed behind count |

A `primary` observation must use the canonical primary repository root stored
in `RUN_STATE.repositoryRoot`; its `workspaceId` is null. An
`isolated-verification` observation must use the canonical root of the
disposable consumer workspace and identify that workspace. An isolated
observation cannot satisfy a primary-repository invariant, and a primary
observation cannot substitute for isolated consumer verification. External
verification must reference the exact primary and isolated observation
identifiers it used. Both roles are subject to the same read-only Git-observer
allowlist.

Only the authoritative Git observation component may invoke Git. It may use
the Python standard library `subprocess` module only for the following
read-only command forms, with an explicit working directory and without shell
interpolation:

```text
git rev-parse --show-toplevel
git symbolic-ref --quiet --short HEAD
git rev-parse --abbrev-ref --symbolic-full-name @{upstream}
git rev-parse --verify <allowed-ref-or-commit>
git diff --cached --name-status -z --find-renames HEAD
git diff --name-status -z --find-renames
git ls-files --others --exclude-standard -z
git rev-list --left-right --count <allowed-symmetric-range>
git rev-list --format=<fixed-machine-format> <allowed-revision-range>
git merge-base --is-ancestor <allowed-commit> <allowed-commit>
git show --no-patch --format=<fixed-machine-format> <allowed-commit>
```

Allowed refs and commits are limited to `HEAD`, the configured upstream,
`refs/heads/main`, `refs/remotes/origin/main`, the recorded baseline, recorded
accepted session commits, and commits returned by an earlier allowed
observation command. The allowed symmetric range is exactly `HEAD` and the
configured upstream combined with Git's symmetric-difference revision
operator. Other allowed revision ranges may contain only those values. Fixed
machine formats may request only commit identifiers, parent identifiers, and
subjects needed by this contract. Adding a Git command or widening an argument
class requires an explicit contract change. The component must derive, at
minimum:

| Authoritative fact | Required meaning |
| --- | --- |
| repository root | Canonical root reported by Git and matched to `repositoryRoot` |
| current branch | Exact checked-out branch |
| configured upstream | Full upstream ref for the current branch |
| `HEAD` | Current forty-character commit identifier |
| upstream commit | Commit resolved from the configured upstream |
| local `main` | Commit resolved from `refs/heads/main` |
| `origin/main` | Commit resolved from `refs/remotes/origin/main` |
| local-main ancestry | `localMainIsAncestorOfHead`, derived only by the allowlisted merge-base ancestry operation |
| origin-main ancestry | `originMainIsAncestorOfHead`, derived only by the allowlisted merge-base ancestry operation |
| staged paths | Complete paths differing between `HEAD` and the index |
| tracked modified paths | Complete tracked paths differing between index and worktree |
| untracked paths | Complete untracked path set, without ignored paths |
| complete changed-path set | Union of staged, tracked-modified, and untracked paths |
| worktree cleanliness | True only when all three path sets are empty |
| upstream alignment | True only when `HEAD` equals the upstream commit |
| ahead and behind counts | Counts derived from the symmetric commit relationship between `HEAD` and upstream |
| accepted commit relationship | Commits after the baseline that the session accepted, matched to commit objects and ancestry |
| published commit relationship | Equality and ancestry among `HEAD`, upstream, and every accepted session commit |

For a primary observation, local `main` and `origin/main` must both resolve.
At initialization and the baseline observation, their observed commits must
equal `RUN_STATE.mainCommitAtStart` and `RUN_STATE.originMainCommitAtStart`,
and both ancestry booleans must be true. Equality with the initialization
values and ancestry to experimental `HEAD` are distinct facts: neither
implies the other. Ancestry must not be inferred from a branch name, equal or
unchanged protected-ref hashes, ahead or behind counts, or another artifact's
claim. A divergent experimental branch is unsafe and must be rejected before
option generation.

For the bootstrap observation, comparison with RUN_STATE means comparison
inside the unpublished bundle. Its `sessionId`, `branch`, `baselineCommit`,
`repositoryRoot`, protected-ref commits and ancestry, artifact name and
identifiers, state, sequence, and timestamps must agree with the simultaneously
published initial RUN_STATE. The Git observer retains exclusive ownership of
the observation and every Git command; the launcher and bootstrap validator
may validate and publish the bundle but must not manufacture or replace Git
facts.

Path collection must use unambiguous machine-readable Git output, including
NUL-delimited output where paths are returned. Renames and unusual valid path
characters must not cause a changed path to be omitted. The accepted and
published relationships must be derived from the commit graph and exact
commit identifiers, not inferred from counts alone.

Artifact booleans, path arrays, commit identifiers, reported status lines,
and command-line claims are untrusted claims. Where the contract depends on
repository state, the validator must compare every such claim with the fresh
authoritative observation and reject any mismatch. Comparing one artifact
claim only with another artifact claim is insufficient.

An observation establishes only facts visible at its recorded checkpoint. A
pre-action and post-action observation may establish unchanged persistent
commits, refs, branch identity, upstream, and path sets at those two
checkpoints. It cannot prove that an agent never temporarily staged a path,
switched away and back, created and concealed an intermediate commit, or took
another transient action that left no observable state. Historical behavioral
claims about Worker or Reviewer processes require the exact authoritative
`AGENT_SUPERVISION-<event>.json` and must not be inferred from Git snapshots
alone. Contract checks therefore require unchanged checkpoint commits and
refs, unchanged branch identity at checkpoints, expected persistent changed
paths, bound durable results, authoritative agent supervision, and absence of
persistent unauthorized mutation.

The component's Git access is inspection-only. It must never invoke an
operation that adds, restores, resets, cleans, checks out, switches, commits,
merges, rebases, tags, fetches, pulls, pushes, updates refs, or modifies Git
configuration. This prohibition includes direct Git commands, plumbing
commands with mutating effects, hooks used for mutation, and subprocesses
that perform those actions. Operational orchestration, not validation, owns
all permitted repository mutations.

## OBSERVATION.json Contract

`OBSERVATION.json` records the repository baseline and diagnosed gaps.

It must contain:

| Field | Type | Constraint |
| --- | --- | --- |
| shared fields | object members | All shared artifact fields are required |
| `gitObservationId` | string | Exact primary baseline Git observation identifier |
| `observedCommit` | string | Must equal the session baseline commit |
| `repositoryClean` | boolean | Must be true |
| `upstreamAligned` | boolean | Must be true |
| `repositoryRoot` | string | Mandatory and equal to authoritative Git root |
| `currentBranch` | string | Must equal authoritative branch |
| `configuredUpstream` | string | Must equal authoritative upstream |
| `upstreamCommit` | string | Must equal authoritative upstream commit |
| `aheadCount` | integer | Must equal authoritative value and be zero |
| `behindCount` | integer | Must equal authoritative value and be zero |
| `stagedPaths` | array of strings | Must be empty and match authoritative Git |
| `trackedModifiedPaths` | array of strings | Must be empty and match authoritative Git |
| `untrackedPaths` | array of strings | Must be empty and match authoritative Git |
| `changedPaths` | array of strings | Complete union; must be empty and match authoritative Git |
| `protectedRefs` | object | Exact `localMainCommit` and `originMainCommit` values matching authoritative Git |
| `localMainIsAncestorOfHead` | boolean | Must be true and equal authoritative Git observation |
| `originMainIsAncestorOfHead` | boolean | Must be true and equal authoritative Git observation |
| `productEntryPoints` | array of strings | Non-empty |
| `consumerVisibleCapabilities` | array of objects | May be empty only with justification |
| `evidenceBackedCoverage` | array of objects | Records current evidence-backed surfaces |
| `validationBaseline` | array of objects | Exact numbered `baseline` validation-result artifact names and identifiers |
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

`OBSERVATION.json` is valid only when a fresh authoritative Git observation
proves all of the following at the observation baseline:

- `repositoryClean` is exactly `true`;
- `upstreamAligned` is exactly `true`;
- `observedCommit` and `baselineCommit` equal authoritative `HEAD`;
- `currentBranch`, configured upstream, upstream commit, ahead count, and
  behind count equal authoritative values;
- protected local `main` and `origin/main` values equal authoritative values;
- protected local `main` and `origin/main` equal the values stored at session
  initialization, and authoritative `localMainIsAncestorOfHead` and
  `originMainIsAncestorOfHead` are both exactly true;
- staged, tracked-modified, untracked, and complete changed-path sets are all
  empty.

False cleanliness, alignment, or protected-main ancestry is not a permissible
observation of a risky baseline; it invalidates the observation and prevents
option generation. Artifact ancestry booleans are claims and must be rejected
when either disagrees with the authoritative Git observation.

Every artifact referenced by `validationBaseline` must be created in
`OBSERVING`, before `OBSERVATION.json` is published, and must satisfy the
baseline-specific null-reference rules in Immutable Corrective Evidence
Contracts. It must not invent a future decision or Worker pass.

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

The selected experiment's complete union of authorized product paths must not
exceed six. A product path is every repository file that implementation may
create, modify, delete, rename, regenerate, or mechanically update. Generated
outputs, manifests, lock files, indexes, snapshots, fixtures, and other
mechanically required companion files each count as product files; being
generated or mechanically required does not exempt a path. Runtime artifacts
below `/tmp` do not count because they are not product paths.

The union is computed across the active decision and every assignment for the
selected experiment, not per assignment or per commit. Splitting work into
passes does not reset it. A value above six is valid only when explicit human
authorization was recorded before the first implementation transition for
that decision and states the higher maximum and exact authorized path union.
Protected-category authorization alone does not imply authorization to exceed
six. `estimatedFileCount`, artifact assertions, or a larger global setting
must never override the actual union.

## DIRECTOR_DECISION Contract

Each numbered `DIRECTOR_DECISION-<decision>.json` is the immutable acceptance
contract for one selected experiment.

It must contain:

| Field | Type | Constraint |
| --- | --- | --- |
| shared fields | object members | All shared artifact fields are required |
| `decisionId` | string | Unique within the session |
| `decisionNumber` | integer | Starts at one and increases by one for each replan |
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
| `productFileLimitAuthorization` | object or null | Required when more than six product paths are authorized |

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

During Atomic Decision And Initial Worker Registration, the decision validator
must canonicalize the complete decision object and calculate a SHA-256 digest.
The canonical representation is the UTF-8 encoding of Python standard-library
`json.dumps` with `ensure_ascii=False`, `allow_nan=False`, `sort_keys=True`,
and `separators=(",", ":")`. Arrays retain their declared order, object member
names are sorted, and no final newline is included in the digest input.
Duplicate keys must already have been rejected during parsing. Non-finite
numbers are invalid. The resulting digest is the lowercase hexadecimal
SHA-256 of those exact canonical bytes.

The digest covers the complete artifact, including all shared fields and, at
minimum, the product hypothesis, selected option, authorized and prohibited
paths, required readings, every product, epistemic, and compatibility
acceptance criterion, targeted and repository checks, external verification
plan, revision, replan, and commit limits, stop conditions, preferred commit
message, and protected-category authorization. Omitting an unknown or future
field from canonicalization is prohibited.

When non-null, `productFileLimitAuthorization` must record
`authorizedBy: human-product-owner`, an authorization timestamp earlier than
the first implementation transition, the exact product path union, and an
integer maximum no smaller than that union. It authorizes no path absent from
the decision and grants no protected-category authorization.

The transition atomically records the decision artifact name, digest, mapping,
zero-valued budget usage, initial assignment, Worker identity, applicable used
identifiers, transition history, and new state exactly as specified by Atomic
Decision And Initial Worker Registration. No digest or active mapping is
required or permitted in RUN_STATE before that transition. Every later
validation and transition must recalculate and compare the digest. Any in-place
byte change that changes canonical content invalidates the session; replacing
acceptance-significant content while preserving a stale digest is not
recovery.

A replan must select the replacement option first and then, during
`DEFINING_ACCEPTANCE`, create the next numbered decision artifact with a new
`decisionId`, `decisionNumber`, complete acceptance contract, and independently
canonicalizable content, together with a fresh initial assignment. The
subsequent `DEFINING_ACCEPTANCE -> IMPLEMENTING` transition calculates the
digest and atomically registers both artifacts. It must preserve all earlier
decision files and digest mappings. Reusing an earlier decision artifact,
digest, or acceptance contract as the active replan decision is invalid, even
when some fields legitimately remain the same; the new artifact must represent
the complete fresh decision based on the replan evidence.

## WORKER_ASSIGNMENT Contract

Every Worker assignment must contain:

| Field | Type | Constraint |
| --- | --- | --- |
| shared fields | object members | All shared artifact fields are required |
| `assignmentId` | string | Unique within the session |
| `workerAgentId` | string | New session-unique Worker identity registered for this assignment |
| `decisionId` | string | For initial work, the decision being atomically registered; for corrective work, the active decision |
| `passNumber` | integer | Starts at one |
| `assignmentType` | string | `initial` or `corrective` |
| `correctiveContext` | string or null | Null for `initial`; `retained-pre-commit-diff` or `post-publication-clean-primary` for `corrective` |
| `objective` | string | One bounded task |
| `repositoryEvidence` | array of objects | Non-empty |
| `authorizedPaths` | array of strings | Must equal or be a strict subset of decision paths |
| `prohibitedPaths` | array of strings | Must include all non-authorized protected areas |
| `requiredReadings` | array of strings | Non-empty |
| `acceptanceCriteria` | array of strings | References decision criterion identifiers |
| `targetedChecks` | array of strings | Non-empty |
| `repositoryChecks` | array of strings | Must include `make validate` |
| `reviewFindingsToCorrect` | array of objects | Empty for initial assignments |
| `triggerEvidenceArtifact` | string or null | Null for initial; exact numbered immutable source evidence for corrective work |
| `triggerEvidenceId` | string or null | Null for initial; exact `artifactId` of the source evidence |
| `triggerEvidenceCreatedAtUtc` | string or null | Null for initial; exact timestamp of the corrective evidence |
| `commitProhibited` | boolean | Must be true |
| `pushProhibited` | boolean | Must be true |
| `branchMutationProhibited` | boolean | Must be true |

A corrective assignment must preserve the active decision and authorized
scope.

Every corrective assignment must set the applicable non-null
`correctiveContext`, have a new session-unique `assignmentId`,
the next unique pass number, `assignmentType` equal to `corrective`, and a
creation timestamp later than its trigger evidence. It must explicitly map
each requested correction to the latest `REVISE` finding, validation failure,
external-verification failure, inspection finding, or recovery outcome. Its
`workerAgentId` and `assignmentId` must be unused when the assignment is
created and must be added to the corresponding session-global sets when the
Worker is atomically registered. An initial assignment, an earlier corrective
assignment, or a copy with a reused identifier must not authorize corrective
implementation.

## WORKER_RESULT Contract

Every Worker result must contain:

| Field | Type | Constraint |
| --- | --- | --- |
| shared fields | object members | All shared artifact fields are required |
| `assignmentId` | string | Matches the active assignment |
| `workerAgentId` | string | Matches the assignment and registered active Worker identity |
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
| `agentSupervisionArtifact` | string | Exact numbered supervision artifact for this Worker process |
| `agentSupervisionId` | string | Exact supervision identifier in that artifact |

A Worker result is structurally invalid when:

- the result artifact is absent or malformed;
- required fields are absent;
- no valid durable result was captured before a timeout or process failure;
- assignment, agent, pass, or result identity does not match;
- its supervision artifact is missing, stale, invalid, or identity-mismatched;
- `changedPaths` differs from authoritative repository state;
- the result claims a successful command whose recorded exit code is non-zero;
- the result omits final Git status;
- authoritative agent supervision records a prohibited action, or
  checkpoint Git evidence shows a persistent unauthorized mutation.

`BLOCKED`, `FAILED`, and `INTERRUPTED` are valid status values when the artifact
otherwise validates, but they are review-ineligible. `BLOCKED` may use only the
bounded infeasibility replan path defined by Legal State Transitions. `FAILED`
and `INTERRUPTED` must proceed through recovery and `FINALIZING`; they cannot
enter review or replan. A structurally invalid result must never be reviewed,
replanned, or committed.

Before review eligibility, the validator must freshly derive authoritative
Git state. It must require the result status to be exactly `COMPLETED`, the
Worker process to be authoritatively proven stopped by its exact bound
supervision artifact, and no active Worker. The assignment identifier and pass
number must each be unique in the session and must match between assignment
and result. Product Director inspection must be recorded separately from
Worker claims.

Authoritative changed paths must exactly equal `changedPaths` and the
Product Director's independently recorded numbered inspection, and must be
equal to the assignment's authorized paths or a valid subset. The
authoritative staged set must be empty. Pre- and post-Worker checkpoint
observations must show unchanged commits, branch, upstream, and protected refs
and no persistent unauthorized changed path. They do not establish every
transient action between checkpoints. A mismatch between reports is not
enough; repository claims must be compared with the applicable Git
observation and historical behavior must use the exact bound authoritative
agent-supervision evidence.

## AGENT_SUPERVISION Contract

Every Worker and Reviewer process event has exactly one authoritative numbered
immutable artifact:

```text
AGENT_SUPERVISION-<event>.json
```

The first occurrence is exactly `AGENT_SUPERVISION-01.json`. The family uses
the independent contiguous numbering and shared immutable fields defined
above. Its sole artifact owner and `createdBy` value is `agent-supervisor`.
The Product Director, Worker, Reviewer, worker recorder, and reviewer recorder
must not create, replace, or substitute this artifact, self-attest process
termination, or self-attest prohibited transient behavior.

Each supervision artifact must contain:

| Field | Type | Constraint |
| --- | --- | --- |
| shared fields | object members | All shared immutable artifact fields are required |
| `supervisionId` | string | Session-unique and never reused |
| `eventNumber` | integer | Starts at one, contiguous, and equals the file suffix |
| `agentRole` | string | Exactly `worker` or `reviewer` |
| `agentId` | string | Exact registered active agent identity |
| `relatedAssignmentId` | string or null | Non-null only for a Worker and equal to its assignment |
| `relatedReviewId` | string or null | Non-null only for a Reviewer and equal to its review |
| `workerPassNumber` | integer or null | Non-null only for a Worker and equal to its pass |
| `reviewNumber` | integer or null | Non-null only for a Reviewer and equal to its numbered review |
| `processHandle` | string | Non-empty, supervisor-observed, and unique among session process events |
| `processInvocation` | object | Exact executable, ordered arguments, working directory, process handle, and launch timestamp |
| `processStartedAtUtc` | string | UTC process-start timestamp |
| `processEndedAtUtc` | string | UTC terminal-process timestamp |
| `observedStoppedAtUtc` | string | UTC timestamp at which the supervisor observed termination |
| `processOutcome` | string | Exactly `SUCCEEDED`, `FAILED`, `TIMED_OUT`, or `INTERRUPTED` |
| `exitCode` | integer or null | Exact exit code, with null allowed only as constrained below |
| `timedOut` | boolean | Exact supervisor result |
| `interrupted` | boolean | Exact supervisor result |
| `processStopped` | boolean | Must be true for a valid supervision artifact |
| `prohibitedActionFindings` | array of objects | Complete supervisor-observed transient-action findings, possibly empty |
| `stdoutCapture` | object | Exact base64-encoded stdout bytes and decoded byte length |
| `stderrCapture` | object | Exact base64-encoded stderr bytes and decoded byte length |
| `stdoutDigest` | string | Sixty-four-character lowercase hexadecimal SHA-256 of the complete exact stdout bytes, including empty output |
| `stderrDigest` | string | Sixty-four-character lowercase hexadecimal SHA-256 of the complete exact stderr bytes, including empty output |
| `supervisorEvidenceDigest` | string | Sixty-four-character lowercase hexadecimal SHA-256 of the canonical authoritative process-result envelope |
| `createdAtState` | string | `IMPLEMENTING` for Worker; `REVIEWING` for Reviewer |
| `createdAtStateSequence` | integer | Exact sequence of the active process lifecycle event |

Role combinations are exact. A Worker sets `relatedAssignmentId` and
`workerPassNumber` non-null and sets `relatedReviewId` and `reviewNumber` null.
A Reviewer sets `relatedReviewId` and `reviewNumber` non-null and sets
`relatedAssignmentId` and `workerPassNumber` null. The identifiers, role,
pass or review number, and process handle must match the active registration
and the exact bound assignment, result, or verdict. A supervision event is
fresh only for that one process and must never be reused by another result,
verdict, pass, review, or lifecycle transition.

The permitted outcome combinations are exhaustive:

| `processOutcome` | `exitCode` | `timedOut` | `interrupted` | `processStopped` |
| --- | --- | --- | --- | --- |
| `SUCCEEDED` | exactly `0` | `false` | `false` | `true` |
| `FAILED` | non-zero integer | `false` | `false` | `true` |
| `TIMED_OUT` | `null` | `true` | `false` | `true` |
| `INTERRUPTED` | `null` | `false` | `true` | `true` |

No other outcome or combination is valid. In particular, running, stopping,
unknown, or indeterminate process state is not a permitted outcome;
`processStopped: false`, simultaneous timeout and interruption, a null exit
code for ordinary success or failure, or an exit code for timeout or
interruption is invalid.

Durable-artifact outcome compatibility is exact. Worker `COMPLETED` or
`BLOCKED` requires supervised `SUCCEEDED`; Worker `FAILED` requires supervised
`FAILED`; Worker `INTERRUPTED` requires supervised `TIMED_OUT` or
`INTERRUPTED`. A Reviewer verdict is eligible only with supervised
`SUCCEEDED`. A durable success, result, or verdict that disagrees with these
combinations is invalid and cannot override supervision.

Each `prohibitedActionFindings` member contains a unique `findingId`, a
contract-defined prohibited `actionCode`, `observedAtUtc`, non-empty
`evidence`, and any related stream offset or process metadata. A non-empty
array proves prohibited transient behavior and makes the bound Worker result
or Reviewer verdict ineligible for review, corrective progression, commit,
publication, or successful finalization. An empty array supports only the
supervisor's observation scope; an agent, recorder, or Product Director must
not turn it into a broader unsupervised claim.

Permitted `actionCode` values are:

```text
COMMIT_ATTEMPT
PUSH_ATTEMPT
BRANCH_MUTATION_ATTEMPT
CHILD_AGENT_SPAWN_ATTEMPT
UNAUTHORIZED_FILE_MUTATION
UNAUTHORIZED_PROCESS_ATTEMPT
OTHER_CONTRACT_PROHIBITION
```

`OTHER_CONTRACT_PROHIBITION` additionally requires the exact violated contract
rule or assignment prohibition in `evidence`; it must not be used as an
unexplained catch-all.

### Embedded Process Stream Evidence

`AGENT_SUPERVISION-<event>.json` remains the authoritative immutable structured
artifact. This embedded evidence grants no Git command, Git observation,
repository mutation, or repository-fact ownership to the agent supervisor.

Every supervision artifact contains `stdoutCapture`, `stderrCapture`, and
`processInvocation`. Each capture object contains exactly these required
fields:

| Field | Type | Constraint |
| --- | --- | --- |
| `encoding` | string | Exactly `base64` |
| `contentBase64` | string | Canonical RFC 4648 base64 with padding for the exact captured bytes |
| `byteLength` | integer | Non-negative and equal to the decoded-byte length |

`contentBase64` represents the exact captured process bytes without newline
normalization, character-set conversion, truncation, reconstruction, or any
other transformation. Strict validation decodes the standard RFC 4648
alphabet and required padding, then re-encodes the decoded bytes and requires
exact string equality; invalid padding, alternate alphabets, ignored
characters, and otherwise noncanonical encodings are rejected.

`stdoutDigest` and `stderrDigest` are each the lowercase hexadecimal SHA-256
of the exact decoded bytes in the corresponding capture object. An empty
stdout or stderr stream is represented only by:

```text
encoding: base64
contentBase64: ""
byteLength: 0
stdoutDigest or stderrDigest:
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

Null, omitted, padded, reconstructed, or otherwise different representations
of an empty stream are invalid.

`processInvocation` contains at least:

```text
executable
arguments
workingDirectory
processHandle
launchedAtUtc
```

`executable`, `workingDirectory`, and `processHandle` are non-empty strings;
`arguments` is the exact ordered array of string arguments; and
`launchedAtUtc` is a UTC timestamp. Its `processHandle` equals the top-level
`processHandle`, and `launchedAtUtc` equals `processStartedAtUtc` and the
supervisor's authoritative process registration. Executable, ordered
arguments, working directory, handle, and launch time must match that
registration exactly; substitution or reconstruction is invalid.

The authoritative supervision evidence envelope is the complete supervision
artifact object excluding only the `supervisorEvidenceDigest` member itself.
It therefore includes every immutable shared field; every process identity,
registration, role-reference, outcome, and timestamp field;
`processInvocation`; `stdoutCapture`; `stderrCapture`; `stdoutDigest`;
`stderrDigest`; `prohibitedActionFindings`; related assignment, Worker pass,
review, and agent identities; creation state; and state sequence. No nested
member, array element, immutable shared field, or unknown future artifact field
may be omitted from the envelope. The supervisor canonicalizes this complete
object with the deterministic JSON canonicalization parameters defined for
Director decisions and sets `supervisorEvidenceDigest` to the lowercase
hexadecimal SHA-256 of the exact canonical UTF-8 bytes.

The documented input contract of the agent-supervision validator is the
complete immutable `AGENT_SUPERVISION` artifact, including both capture
objects and `processInvocation`, together with the bound assignment/result or
review/verdict artifact, authoritative active-process registration, and exact
expected lifecycle event. It must:

1. strictly decode each canonical base64 value;
2. reject invalid padding or noncanonical encoding;
3. compare each decoded length with `byteLength`;
4. recompute `stdoutDigest` and `stderrDigest` from the decoded bytes;
5. recalculate `supervisorEvidenceDigest` from the complete canonical envelope;
6. compare `processInvocation` with top-level process identity and authoritative
   registration;
7. add the supervision artifact, both capture-object identities and digests,
   and processInvocation identity to `validatedInputs`.

For `validatedInputs`, each capture-object identity is its field name
(`stdoutCapture` or `stderrCapture`) within the exact supervision artifact and
its digest is the lowercase SHA-256 of that capture object's deterministic
canonical JSON. The processInvocation identity includes its process handle and
the lowercase SHA-256 of its complete deterministic canonical JSON. These
object digests supplement rather than replace the decoded stream digests and
complete `supervisorEvidenceDigest`.

The validator fails closed for missing capture objects; inconsistent null or
empty captures; invalid or noncanonical base64; wrong `byteLength`; changed
captured bytes; a declared stream-digest mismatch; reconstructed or normalized
output; capture truncation; processInvocation mismatch; stale or substituted
capture evidence; `supervisorEvidenceDigest` mismatch; or caller-supplied
digest claims without the corresponding exact bytes. A durable Worker result
or Reviewer verdict cannot override exact captured-stream or invocation
evidence that proves a different process or outcome.

Raw captured output may contain sensitive data. It remains an external runtime
artifact inside the session directory outside the repository, subject to that
directory's access controls and cleanup policy. It must never be copied into
canonical RKM data or committed.

Timestamp ordering and lifecycle-state compatibility are governed by Temporal
Semantics. A Worker result or Reviewer verdict must be created after its exact
supervision artifact, carry the same agent and related identifiers, cite that
artifact and `supervisionId`, and use an `endedAtUtc` equal to
`processEndedAtUtc`. A durable result or verdict proves only the agent's
substantive response; it does not independently prove that the process stopped
or that prohibited transient behavior did or did not occur.

A process is eligible for lifecycle progression only when the exact fresh
supervision artifact proves `processStopped: true`, its outcome combination
validates, its identity and related references match, its timestamps and state
sequence validate, both exact stream captures and all digests validate,
processInvocation matches registration, and its prohibited-action findings
permit the proposed transition. The agent-supervision validator must reject
missing or stale supervision; reused supervision IDs or event numbers; wrong
agent, assignment, pass, review, or process-handle identity; false stopped
state; running or unknown state; impossible timestamps; mismatched state
sequences; contradictory exit, timeout, or interruption fields; missing or
invalid capture or digest evidence; invocation mismatch; Worker or Reviewer
self-attestation substituted for authoritative supervision; and any transient
prohibited-behavior claim not supported by supervision.

## Immutable Corrective Evidence Contracts

`WORK_INSPECTION-<pass>.json` records the Product Director's independent
post-Worker inspection. It contains the immutable shared fields plus unique
`inspectionId`, `assignmentId`, `workerAgentId`, `passNumber`, exact
`preWorkerGitObservationId`, exact `postWorkerGitObservationId`,
`authoritativeChangedPaths`, `stagedPaths`, `scopeFindings`,
`acceptanceFindings`, `persistentMutationFindings`, and `inspectionResult`.
Its pass number matches the assignment and result. It may record only
checkpoint-observable Git facts as Git facts; any behavioral finding cites the
exact applicable authoritative agent-supervision artifact.

`VALIDATION_RESULT-<attempt>.json` records one validation attempt. It contains
the immutable shared fields plus unique `validationResultId`, contiguous
`attemptNumber`, `validationPhase`, nullable `decisionId`, nullable
`workerPassNumber`, `commands` with exact exit codes and diagnostics,
`criteriaResults`, `gitObservationIds`, and `result` bounded to `PASS` or
`FAIL`. `validationPhase` is exactly one of:

```text
baseline
post-review
pre-commit
external-correction
```

For `baseline`, `decisionId` and `workerPassNumber` must both be null,
`createdAtState` must be `OBSERVING`, and the artifact must be published during
observation before `OBSERVATION.json`; future decision or pass identifiers are
prohibited. For every decision-related phase, `decisionId` and
`workerPassNumber` are mandatory non-null references to the applicable active
decision and completed Worker pass. `external-correction` records validation
of a fresh corrective pass after failed external verification, not the
external-verification process itself. A failed attempt remains immutable when
a later attempt passes. Every Product Director validation attempt used as
baseline, transition, acceptance, or finalization evidence receives its own
numbered artifact; embedded Worker command claims do not replace it.

`RECOVERY_RECORD-<attempt>.json` records one safe-recovery attempt. It contains
the immutable shared fields plus unique `recoveryId`, contiguous
`attemptNumber`, `sourceEvidenceArtifact`, `sourceEvidenceId`, rejected
decision and pass identifiers, preserved diagnostic location, paths restored
or removed by orchestration, commands and exit codes, exact pre- and
post-recovery Git observation identifiers, protected-ref comparison,
`outcome` bounded to `RECOVERED` or `FAILED`, and remaining risks. A failed
recovery is never overwritten by a later attempt.

Every evidence-family file begins at `-01`, advances contiguously by family,
has a session-unique artifact and domain identifier, records its creation
state and state sequence through the immutable shared fields, and is immutable
from creation. Transitions and corrective assignments reference the exact
artifact file and unique identifier when the evidence is relevant. A later
attempt never overwrites an earlier failure.

## REVIEW_VERDICT Contract

Every Reviewer verdict must contain:

| Field | Type | Constraint |
| --- | --- | --- |
| shared fields | object members | All shared artifact fields are required |
| `reviewId` | string | Unique within the session |
| `reviewerAgentId` | string | Matches the Reviewer registered for this review |
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
| `agentSupervisionArtifact` | string | Exact numbered supervision artifact for this Reviewer process |
| `agentSupervisionId` | string | Exact supervision identifier in that artifact |

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

A review artifact may be created only while the session is in `REVIEWING` and
its `reviewerAgentId` and `reviewId` match `activeAgentId` and
`currentReviewId`. Both identifiers must belong to their session-global used
identifier sets and must never be reused. `assignmentId` plus
`workerPassNumber` must identify the immediately preceding eligible Worker
result and work inspection. The verdict must bind the exact fresh Reviewer
supervision artifact whose role, agent, review identifier, review number,
process handle, invocation, terminal outcome, timestamps, exact captures, and
digests validate. The verdict cannot independently establish that the Reviewer
stopped.

## EXTERNAL_VERIFICATION Contract

Every numbered `EXTERNAL_VERIFICATION-<attempt>.json` must contain:

| Field | Type | Constraint |
| --- | --- | --- |
| shared fields | object members | All shared artifact fields are required |
| `verificationId` | string | Unique within the session |
| `attemptNumber` | integer | Starts at one and is contiguous |
| `publishedCommit` | string | Commit verified in the isolated workspace |
| `publishedUpstream` | string | Experimental upstream branch |
| `workspaceId` | string | Unique disposable consumer-workspace identity |
| `workspacePath` | string | Absolute path below `/tmp` |
| `primaryGitObservationId` | string | Exact primary observation used for publication claims |
| `isolatedGitObservationIds` | array of strings | Exact isolated observations used before and after consumer checks |
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
Every attempt is immutable from `-01`; a failed attempt remains present when a
later correction produces another attempt.

External verification must not modify the primary repository.

`publishedCommit`, `publishedUpstream`, and
`checkoutMatchedPublishedCommit` are claims until compared with authoritative
Git observations in both the primary repository and isolated workspace. A
`PASS` is invalid unless the external checkout commit equals the authoritative
primary branch `HEAD` and upstream commit and contains every accepted session
commit in the required relationship.

External-verification orchestration may create, populate, and remove a
temporary consumer workspace below `/tmp`. Production validation of Git state
in that workspace still uses an `isolated-verification` observation from the
authoritative Git observer. The orchestration permission does not grant any
production validation component permission to mutate a repository.

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

The report must not claim success when the latest numbered external-
verification artifact records `FAIL`.

The report may recommend:

```text
PROMOTE
CONTINUE_EXPERIMENT
REVISE_WITH_HUMAN_DIRECTION
DISCARD
NO_PROMOTION_DECISION
```

The report must never perform promotion.

Every required heading must be followed, before the next heading or end of
file, by substantive non-whitespace content. A heading, empty line, HTML
comment, punctuation-only text, or repeated heading title is not substantive.
A headings-only or template-only report is invalid.

The substantive sections must cross-reference structured artifacts or state
values consistently and collectively state the mission, authoritative
baseline commit, selected experiment and active decision, ordered accepted
commits, exact changed paths, review history and verdicts, validation result,
external verification result, epistemic limitations, remaining risks,
recommendation, stop reason, exact agent-supervision history, and final
authoritative Git state including both protected-main ancestry booleans. For
`COMPLETED`, every such statement must agree with `RUN_STATE.json`, numbered
decisions, results, verdicts, external verification, and fresh Git
observations. Missing facts, unexplained contradictions, or success language
unsupported by structured and authoritative evidence invalidate completion.
The report may identify supervision, capture-object, stream, invocation, and
envelope digests, but it must not copy raw decoded stream content into the
repository.

## Artifact Ownership and Immutability

Only the Product Director may create:

```text
OBSERVATION.json
OPTIONS.json
DIRECTOR_DECISION-<decision>.json
WORKER_ASSIGNMENT-<pass>.json
WORK_INSPECTION-<pass>.json
VALIDATION_RESULT-<attempt>.json
RECOVERY_RECORD-<attempt>.json
FINAL_REPORT.md
```

Only the Git observer may create `GIT_OBSERVATION-<observation>.json`. The
external verifier creates `EXTERNAL_VERIFICATION-<attempt>.json`. Worker and
Reviewer recorders create their corresponding numbered result and verdict
artifacts from the stopped agents' substantive responses.

Only the agent supervisor may create
`AGENT_SUPERVISION-<event>.json`. It is authoritative only for agent-process
identity, invocation, outcome, termination, exact captured streams and their
digests, and supervised transient-action evidence. It has no Git-observation
or repository-mutation authority. The Git observer and agent supervisor are
separate authoritative components and neither may substitute its evidence for
the other's domain.

The launcher initializes `RUN_STATE.json`.

The Product Director replaces `RUN_STATE.json` only through legal transitions.

Under Product Director orchestration, the Worker and Reviewer recorders must
capture the natural-language responses into their corresponding structured
result artifacts without changing substantive meaning.

Once an artifact becomes immutable, later corrections must create a numbered
successor rather than overwrite history.

A corrective Worker pass must not overwrite the preceding assignment, result,
supervision, inspection, review, validation, recovery, or external-verification
evidence.

A replan must not overwrite the previous options or decision history.

## Scope Enforcement

The Product Director must obtain authoritative changed paths from the Git
observer independently of Worker claims.

The authoritative changed-path set is derived by that observer from repository
state, not from the Worker report.

It is the complete authoritative union of staged, tracked-modified, and
untracked paths. Each Worker, Product Director, and Reviewer path claim must
be compared with this set at the applicable lifecycle boundary.

Every changed path must:

- be repository-relative;
- be listed in the active assignment;
- be listed in or permitted by the active decision;
- comply with routed `AGENTS.md` rules;
- comply with protected-category authorization.

A mechanically required additional path is unauthorized unless the active
decision explicitly permitted that category of generated or contract-required
change.

The union of every product path authorized by the active decision and its
assignments must remain at or below six. Generated and mechanically required
paths count individually. Only explicit human authorization recorded before
the decision's first `IMPLEMENTING` transition may set a larger maximum, and
the authoritative path union must remain within that recorded maximum.

Unauthorized scope requires immediate stop unless:

- no commit has occurred;
- the path can be safely preserved outside the repository;
- the path can be restored without destructive Git commands;
- repository integrity can be proven afterward.

## Budget Accounting

This section is the sole normative authority for budget arithmetic, entry
checks, charge timing, and exact-once operation identity. Other sections may
require a Budget Accounting check or recorded charge but must not redefine
either.

`RUN_STATE.json` keeps cumulative session usage in `revisionCount`,
`replanCount`, and `acceptedCommitCount`. It keeps per-decision usage in
`decisionBudgetUsage[decisionId]`. Session and decision usage never decrease
or reset; a new decision is added with zero per-decision usage.

For an operation and its applicable decision:

```text
remaining = min(session maximum - session usage,
                decision limit - decision usage)
```

A replan uses the rejected decision. Entry into a new budgeted operation is
legal exactly when `remaining > 0`; a global, command-line, or artifact value
must not loosen either bound.

| Operation | Session maximum and usage | Decision limit and usage | Entry check and operation registration | Single atomic charge point |
| --- | --- | --- | --- | --- |
| corrective revision | `2`, `revisionCount` | active `revisionLimit`, `revisionUsage` | transition into `REVISING` | completed transition into `REVISING` |
| replan | `1`, `replanCount` | rejected `replanLimit`, `replanUsage` | transition into `REPLANNING` | completed transition into `REPLANNING` |
| accepted commit | `3`, `acceptedCommitCount` | active `commitLimit`, `acceptedCommitUsage` | entry into `COMMITTING` atomically registers `pendingCommitOperation` without charging | completed `COMMITTING -> PUBLISHING` transition after the exact commit and authoritative checks exist |

Revision and replan check, register, increment, and append their charge in one
transition. Entry into `COMMITTING` instead records a fresh operation identity,
decision, pre-commit `HEAD`, sequence, and exact pre-charge usage without
changing counters.

`COMMITTING -> PUBLISHING` verifies that pending record, the exact commit,
decision, validation, protected refs, and unchanged usage; atomically it
increments both usages, appends the commit and charge, clears the pending
record, and enters `PUBLISHING`. After interruption, a matching valid commit
may resume this transition; otherwise authorized recovery must restore the
recorded pre-commit state before finalization. No successful charge precedes
the transition.

Each charge records unique `chargeId` and `operationId`, `operationType`,
decision and trigger identifiers, before-and-after usages, charge state and
sequence, `chargedAtUtc`, and the exact commit when applicable. Reuse, a
one-sided increment, double charge, or unmatched counter mutation is invalid.

Later transitions in the same operation must reference and verify the recorded
charge, operation identity, decision, trigger, and expected usage. They must
not recalculate capacity or demand unused allowance after the charge. A new
decision begins with zero usage; a replan remains charged to the rejected
decision and the cumulative session.

A corrective revision preserves the decision identifier, option, hypothesis,
scope, acceptance criteria, and external-verification plan. A replan preserves
the original observation, options, rejected decisions, agent and review
history, rejection evidence, and diagnostics. Every accepted commit must
correspond to one accepted bounded task, contain only authorized paths, pass
staged whitespace and required checks including `make validate`, use a
repository-oriented message, and be published only through `make safe-push`.

## Active Agent Lifecycle Rules

At most one agent thread may be active at a time. Worker and Reviewer
identifiers must be unique across the session and across both roles.

Only one write-capable agent may be active.

Entering initial `IMPLEMENTING` uses Atomic Decision And Initial Worker
Registration. Entering corrective `IMPLEMENTING` atomically updates
`RUN_STATE.json` to register `activeAgentRole: worker`, the assignment's
`workerAgentId` as `activeAgentId`, and its `assignmentId` as
`currentAssignmentId`. The agent and assignment identifiers are appended to
their session-global used sets in that same update. A Worker may not start
before this update succeeds.

Leaving Worker execution for `INSPECTING_WORK` requires the Worker process to
be proven stopped by the exact fresh immutable numbered agent-supervision
artifact, the immutable numbered Worker result to be recorded and bound to it,
and Worker, assignment, pass, process invocation, process handle,
state-sequence, exact captured-stream, and digest correspondence to validate.
The transition atomically consumes and registers that supervision evidence and
clears `activeAgentRole`, `activeAgentId`, and `currentAssignmentId` in the
same `RUN_STATE.json` update. A still-running, unsupervised, stale-supervised,
or identity-mismatched Worker cannot be cleared into review eligibility.

A Reviewer may start only after authoritative Worker supervision is consumed,
the Worker's active fields were cleared, review eligibility is proven, and the
Product Director has inspected repository state. Entering `REVIEWING`
atomically sets `activeAgentRole` to `reviewer`, `activeAgentId` to a new
`reviewerAgentId`, and `currentReviewId` to a new `reviewId`, and appends both
identifiers to their session-global used sets. These are the only permitted
non-null active-agent fields in `REVIEWING`.

Leaving `REVIEWING` requires the Reviewer process to be proven stopped by exact
fresh authoritative supervision, its unique numbered verdict artifact to be
durably recorded and bound to that supervision, and its
`reviewerAgentId`, `reviewId`, review number, process handle, state sequence,
process invocation, exact captured streams, and digests to match the registered
values and artifacts. The transition atomically consumes and registers the
supervision evidence and clears `activeAgentRole`, `activeAgentId`, and
`currentReviewId`. A verdict from a running, unknown, unsupervised,
stale-supervised, mismatched, or previously used Reviewer is invalid. Starting
a Worker while a Reviewer remains active is invalid.

For `COMPLETED`, `STOPPED`, or `ESCALATED`, all agents and threads are stopped
or closed under authoritative supervision with verified invocation, exact
captures, and digests, and all active-agent fields are null. For `FAILED` or
`INTERRUPTED`, agents are stopped and cleared when controllable; missing,
unverifiable, contradictory, or ambiguous supervision is preserved, reported,
and never represented as a clean lifecycle.

## Non-Completed and Invalid Worker Recovery

A valid `BLOCKED` result is not reviewed. Preserve its diff and diagnostics,
enter `INSPECTING_WORK`, publish the inspection, perform only safe
assignment-path recovery, and record every recovery attempt. It may enter
`REPLANNING` only when bounded infeasibility is confirmed, recovery is
complete, replan allowance is positive, the soft deadline has not passed, and
the finalization reserve remains protected; otherwise use a valid `STOPPED`
disposition through `FINALIZING`.

A valid `FAILED` or `INTERRUPTED` result is not reviewed or replanned. Enter
`INSPECTING_WORK` when its durable identity permits safe Worker clearing,
preserve diagnostics, recover only assignment paths, record the outcome, and
continue through `FINALIZING` to the evidence-required terminal state.

For a structurally invalid result: do not review, replan, stage, commit, or
push; preserve diff and status under `/tmp/rkm-runs/`; restore only authorized
tracked paths; preserve and remove only authorized untracked paths; verify
accepted commits and protected refs; record recovery; then enter `FINALIZING`
with disposition `FAILED` and reason `WORKER_RESULT_INVALID`.

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
7. record the attempt and outcome in the next immutable numbered
   `RECOVERY_RECORD-<attempt>.json`;
8. replan only when the rejected-decision and session replan allowances are
   positive, the soft deadline has not been reached, and the finalization
   reserve remains protected;
9. otherwise enter `FINALIZING` with a valid `STOPPED` disposition.

Rejected work must never be committed.

## Protected Ref Invariants

The session must record at initialization:

```text
mainCommitAtStart
originMainCommitAtStart
```

At every commit, publication, external verification, and finalization boundary:

- local `main` must equal `mainCommitAtStart`;
- local `origin/main` must equal `originMainCommitAtStart`;
- a fresh authoritative Git observation must report
  `localMainIsAncestorOfHead: true`;
- that observation must report `originMainIsAncestorOfHead: true`.

Protected-ref equality with initialization values and protected-main ancestry
to experimental `HEAD` are separately required invariants. Unchanged but
divergent protected refs fail every repository-sensitive finalization and
completion check.

Any difference requires an immediate `FAILED` terminal disposition through
`FINALIZING`, unless the difference is proven to be a harmless local
remote-tracking refresh that still points to the same commit recorded at
session start.

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

`stopReasonCode` is mandatory in every terminal state.

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

Finalization is available only to a session whose complete initialization
bundle was validly and atomically published. A failed, interrupted, partial,
or non-atomic bootstrap has no authoritative RUN_STATE, cannot enter
`FINALIZING`, and cannot manufacture a terminal session or report. Staging
debris remains diagnostic debris only.

A successful finalization requires:

- a validated atomic initialization bundle and unbroken bootstrap identities;
- no active agents and authoritative supervision for every relevant Worker and
  Reviewer process, including verified exact stream captures, invocation, and
  all supervision digests;
- an authoritative Git observation of the primary repository using mandatory
  `repositoryRoot`;
- an authoritatively clean primary repository with empty staged,
  tracked-modified, and untracked path sets;
- the authoritative accepted commit count and ordered commit relationship to
  match `acceptedCommitCount` and `acceptedSessionCommits`;
- every accepted session commit to be present in the authoritative
  experimental branch and upstream history;
- authoritative experimental branch `HEAD`, upstream commit, and externally
  published commit to be equal, with zero ahead and behind;
- authoritative local `main` and `origin/main` to equal their initialization
  values;
- fresh authoritative `localMainIsAncestorOfHead` and
  `originMainIsAncestorOfHead` values both equal to true;
- valid required artifacts;
- the latest numbered external-verification result is `PASS`, every product
  criterion passed there, and every product, epistemic, and compatibility
  criterion in the active decision passed in the recorded review and
  validation evidence;
- a substantive, internally consistent final report;
- explicit recommendation;
- terminal state `COMPLETED`;
- stop reason `MISSION_COMPLETED`.

Artifact booleans, counts, commit strings, status arrays, and success claims
alone cannot establish any successful-finalization invariant. They must agree
with authoritative Git and with the complete artifact history.

A stopped or failed finalization requires:

- no active agents when controllable;
- every controllably stopped Worker or Reviewer has matching authoritative
  supervision with verified exact captures, invocation, and digests, while
  missing, unverifiable, or ambiguous supervision is recorded as a failure fact
  rather than replaced by an agent or Director claim;
- diagnostic preservation;
- no rejected commit;
- no unreviewed push;
- protected refs checked;
- explicit terminal reason;
- final report describing the incomplete outcome.

Stopping safely is preferable to manufacturing a successful result.

## Validator Composition and Responsibility Boundaries

The validator implementation must be modular. It must not place artifact
validation, authoritative Git observation, transition logic, lifecycle logic,
finalization logic, final-report validation, and self-tests together in one
production source file or one undifferentiated executable component.

The one public facade is:

```text
scripts/rkm-autonomous-state.py
```

The facade must remain thin. It may parse the public command line, dispatch to
responsibility-specific components, normalize component diagnostics, aggregate
component results, and map failures to documented exit codes. It must not
implement or duplicate domain rules owned by specialized components. It must
not contain fallback validation that bypasses an unavailable, failed, or
rejecting component.

### Required Validation Domains

The production implementation must provide a separately testable,
responsibility-isolated in-process component for every validation domain in
this table. Each component may be a separate source file or imported module;
the ownership and boundary remain mandatory.

| Domain | Sole owner | Documented input contract | Documented output contract |
| --- | --- | --- | --- |
| Authoritative Git observation | Git observer | Canonical `repositoryRoot`; required lifecycle boundary; intended session, branch, and baseline context for bootstrap or the published RUN_STATE context thereafter; and the contract-bounded refs, commits, protected-main ancestry comparisons, and paths to observe | Immutable structured Git observation candidate for the bootstrap staging bundle or published observation thereafter, containing every authoritative Git fact including both exact protected-main ancestry booleans, plus a component result envelope |
| JSON loading, canonicalization, and shared artifact validation | Artifact loader | Runtime artifact bytes, expected artifact type, and expected session context | Duplicate-key-safe parsed object, canonical bytes or digest inputs where required, shared-field findings, and a component result envelope |
| Initialization bootstrap validation | Bootstrap validator | Absent final-session path; private adjacent staging-directory identity; complete candidate `RUN_STATE.json` and `GIT_OBSERVATION-01.json` bytes; artifact-loader results for both; and the exact Git-observer result | Bundle completeness, cross-identity, state-zero, timestamp, protected-ref, ancestry, publication-readiness, and bootstrap-digest findings in a component result envelope that authorizes only one atomic directory rename |
| Decision, scope, budget, and immutable-digest validation | Decision validator | Validated artifacts, active decision history, authoritative changed-path evidence, and configured global limits | Decision, scope-union, effective-budget, and digest findings in a component result envelope |
| State transition and sequence validation | Transition validator | Validated structured artifacts, immutable Git observation when repository state is relevant, current state, proposed state, and transition history | Transition legality, prerequisite, ordering, timestamp, and sequence findings in a component result envelope |
| Authoritative agent-supervision validation | Agent-supervision validator | Complete immutable `AGENT_SUPERVISION` artifact including `stdoutCapture`, `stderrCapture`, and `processInvocation`; bound assignment/result or review/verdict artifact; authoritative active-process registration; and exact expected lifecycle event | Strict base64, decoded-length, exact-byte stream-digest, complete-envelope digest, process-invocation, process-stop, identity, outcome-combination, timestamp, sequence, prohibited-action, freshness, uniqueness, and binding findings in a component result envelope |
| Worker and Reviewer lifecycle validation | Agent lifecycle validator | Validated assignments, results, verdicts, agent identifiers, active-agent state, the exact agent-supervision result including validated capture and invocation input identities, and immutable Git observation at lifecycle boundaries | Eligibility, uniqueness, ownership, pass-order, exact supervision, capture, invocation, and durable-outcome binding findings in a component result envelope |
| Finalization and publication validation | Finalization validator | Complete validated runtime history and initialization result, external-verification evidence, accepted-commit records, exact validated agent-supervision results including capture and invocation identities, and fresh authoritative Git observation including protected-main ancestry | Terminal-state, bootstrap-validity, publication, protected-ref equality, protected-main ancestry, cleanliness, supervision-evidence, and completion findings in a component result envelope |
| Substantive final-report validation | Report validator | `FINAL_REPORT.md` bytes plus validated structured runtime facts and the finalization result | Heading-substance, required-fact, consistency, and contradiction findings in a component result envelope |

Each domain must have exactly one clear owner, one documented input contract,
one documented output contract, no duplicated domain rules, focused self-tests,
and actionable diagnostics. A component may call a lower-level component only
through its documented output contract. Components must not have circular
dependencies.

The end-to-end conformance harness is test infrastructure outside the
production validator component boundary. Its input contract is the public
facade, complete temporary runtime sessions, disposable temporary Git fixture
repositories, and declared scenario expectations. Its output records exercised
commands, exit codes, repository before-and-after evidence, and scenario
findings. It is not a production validation component and grants no production
component additional process authority.

### Dependency Rules

Only the authoritative Git observation component may execute Git commands. It
may use Python standard-library `subprocess` only for the explicit read-only
Git command allowlist in Authoritative Git Observation. Every other component
must consume the observer's immutable structured output and must not execute
Git or accept caller-supplied Git assertions as authoritative.

The runtime agent supervisor is the sole producer of authoritative process-
supervision artifacts. It supervises only the Worker or Reviewer process
assigned by orchestration, captures the complete invocation, result envelope,
and exact streams, and owns no Git command, repository observation, or
repository mutation. It is orchestration infrastructure, not a Worker or
Reviewer product-agent thread, and never acquires an active-agent role or write
capability. The agent-supervision validator consumes that immutable output and
must not start, stop, signal, or otherwise control a process. The Git observer
must not infer process termination or transient behavior, and the agent
supervisor must not infer repository facts. Their identities, inputs, outputs,
and authority are separate.

Initialization has an acyclic bootstrap dependency. The Git observer produces
the candidate first observation from repository facts and the intended
bootstrap context without depending on a published RUN_STATE. The launcher
constructs the candidate RUN_STATE. The artifact loader validates both
candidate structures. The bootstrap validator consumes those loader results
and the Git-observer result, but never executes Git or modifies either
candidate. Only a `PASS` bootstrap result permits the launcher to perform the
single atomic staging-to-final directory rename. Normal transition, lifecycle,
and finalization validators consume only the published bundle and never feed
back into bootstrap validation. No component may publish one bundle member,
infer the other, or create a circular dependency through RUN_STATE.

The transition validator must consume validated artifact structures and must
not duplicate JSON parsing, artifact canonicalization, Git inspection, or
agent-supervision validation. The agent lifecycle validator must consume the
agent-supervision validator's exact component result and reject a missing,
stale, mismatched, or rejecting result. The report validator must consume
validated structured facts and must not independently reconstruct Git state.
The finalization validator must consume
validated structured runtime artifacts, validated supervision results, and a
fresh authoritative Git observation with both ancestry booleans.

The facade imports or calls specialized production components in-process. It
must not launch any validator component through a child process. Only
the Git observer may create a child process, and only to invoke an allowlisted
read-only Git command through Python standard-library `subprocess`. No other
production component may use `subprocess`, execute Git, or indirectly request
another component to execute Git; it consumes the observer's immutable
structured result.

A component failure must fail closed. Missing component output, an unavailable
component, malformed output, or an output whose identity or validated inputs
do not match the request is a validation failure, not permission to infer data
or continue. A `PASS` result must never compensate for another component's
`REJECT` or `ERROR`.

### Structured Component Results

Every component must return a common deterministic result envelope with at
least:

| Field | Type | Constraint |
| --- | --- | --- |
| `contractVersion` | string | Must equal `rkm-autonomous-loop/v2` |
| `component` | string | Stable identity of the sole domain owner |
| `result` | string | Exactly `PASS`, `REJECT`, or `ERROR` |
| `diagnostics` | array of objects | Deterministically ordered; empty only when no diagnostic applies |
| `validatedInputs` | array of objects | Immutable identities and digests of every consumed input |
| `observedAtUtc` | string | UTC time of the component evaluation or authoritative observation |

For identical component inputs and the same immutable Git observation, result,
validated-input identities, and diagnostic ordering must be deterministic.
`observedAtUtc` records the evaluation and does not permit other fields to vary
nondeterministically.

When a component depends on supervision, `validatedInputs` must include the
exact `AGENT_SUPERVISION` artifact name, `artifactId`, `supervisionId`, event
number, and `supervisorEvidenceDigest`; the `stdoutCapture` and `stderrCapture`
field identities and canonical-object digests; both recomputed decoded-byte
stream digests; the processInvocation handle identity and canonical-object
digest; and the bound result or verdict identity and digest. When a component
depends on repository state, its inputs must identify the exact Git observation
and both protected-main ancestry values. When a component depends on
initialization, its inputs must identify both bootstrap members, their
canonical digests and domain identifiers, the bootstrap result, and the final
path whose prior absence was validated. The facade rejects a component
envelope that omits or disagrees with any applicable authoritative input
family.

Each diagnostic must retain the component identity, the rule or invariant
identity when one exists, the affected runtime artifact or repository path,
and an actionable failure explanation. The facade may normalize presentation
but must not remove or change those facts.

The facade must aggregate required component results and map them to these
public exit-code classes:

Aggregation must include the Git-observer result whenever repository state is
relevant and the agent-supervision-validator result whenever a Worker or
Reviewer process is relevant. The facade must compare validated-input
identities across transition, lifecycle, finalization, Git, and supervision
results; it must fail closed rather than choose between disagreeing results.

| Aggregate condition | Public exit code |
| --- | --- |
| Every required component returned `PASS` | `0` |
| No component returned `ERROR` and at least one returned `REJECT` | `2` |
| Any required component returned `ERROR`, failed to return, or returned malformed output | `3` |

An exit code not defined here must not be used to make a failed validation
appear successful.

### Testing Boundaries

The implementation must contain all three testing layers:

1. focused component self-tests for each responsibility owner;
2. integration tests that exercise documented inputs and outputs between
   component boundaries;
3. public-facade end-to-end tests using complete temporary runtime sessions
   and temporary Git repositories below `/tmp`.

The public-facade end-to-end suite must prove that a missing component cannot
be silently bypassed, conflicting component results fail closed, malformed
component output is rejected, an observer claim cannot replace authoritative
Git observation, no partial bootstrap bundle can be reported as a valid
initialized session, and no component mutates the repository. It must also
exercise through the facade every known bypass regression required by the
conformance scenarios. A scenario name, fixture name, asserted flag, or direct
call to an internal function without the described public behavior is
insufficient evidence.

As test infrastructure, the conformance harness may use `subprocess` to invoke
the public CLI. It may execute Git only inside disposable temporary fixture
repositories below `/tmp`, and may create, mutate, and remove those fixture
repositories. It must never mutate the primary repository. This bounded
test-only permission does not allow the facade or any production validation
component to execute arbitrary processes or to broaden Git authority.

### Incremental Implementation Boundary

The modular implementation may be added incrementally under the repository's
one-file-per-run rule. Leaf components must be implemented and focused-self-
tested before the public facade depends on them. Each file must pass every
check applicable to its isolated responsibility.

A partially assembled validator must not be described as complete. An absent
component must not be replaced with a permissive stub, default `PASS`, inferred
output, or facade fallback. No intermediate module may claim end-to-end
contract conformance.

The complete validator is accepted only after all specialized components, the
thin facade, component self-tests, boundary integration tests, public-facade
end-to-end tests, and standard-validation integration exist and pass.

## State Validator Responsibilities

The thin `scripts/rkm-autonomous-state.py` public facade must provide:

```text
initialize
validate-artifact
validate-session
transition
summarize
self-test
```

This section is a non-normative routing index. It defines no duplicate domain
rules. Each requirement is enforced by its sole owner using the authoritative
sections shown below.

| Rule family | Sole owner | Authoritative contract sections |
| --- | --- | --- |
| JSON parsing, shared fields, canonicalization, and immutable artifact structure | Artifact loader | JSON Encoding Rules; Shared Artifact Fields; artifact-family contracts |
| Repository facts, path sets, refs, commits, protected-main ancestry, and workspace roles | Git observer | Authoritative Git Observation; Protected Ref Invariants |
| Atomic initialization bundle, bootstrap cross-identities, and publication readiness | Bootstrap validator | Initialization Bootstrap Transaction; Runtime Location; RUN_STATE.json Contract; Temporal Semantics |
| Decision immutability, atomic initial registration, scope union, digest, and all budget entry or charge rules | Decision validator | Atomic Decision And Initial Worker Registration; OPTIONS; DIRECTOR_DECISION; Scope Enforcement; Budget Accounting |
| State legality, evidence ordering, timestamps, sequences, and terminal routing | Transition validator | Temporal Semantics; Legal State Transitions; State Transition Preconditions |
| Authoritative process stop, outcome, identity, invocation, exact streams, transient behavior, and supervision digests | Agent-supervision validator | AGENT_SUPERVISION Contract; Embedded Process Stream Evidence; Temporal Semantics; Artifact Ownership and Immutability |
| Worker, Reviewer, assignment, result, identity, supervision binding, and recovery eligibility | Agent lifecycle validator | WORKER_ASSIGNMENT; WORKER_RESULT; AGENT_SUPERVISION; REVIEW_VERDICT; Active Agent Lifecycle Rules; recovery sections |
| Publication, external verification, terminal disposition, protected-main ancestry, supervision, and completion | Finalization validator | EXTERNAL_VERIFICATION; Protected Ref Invariants; Finalization Invariants; Deadline and Reserve Invariants |
| Required headings, substantive content, facts, and contradictions | Report validator | FINAL_REPORT.md Contract |
| Public aggregation, commands, deterministic diagnostics, and exit codes | Thin facade | Validator Composition and Responsibility Boundaries |

The facade requests every required component, fails closed for missing,
malformed, conflicting, `REJECT`, or `ERROR` results, preserves diagnostics,
and applies the documented exit-code mapping. `initialize` reports success
only after the bootstrap validator passes and the one atomic directory rename
publishes both bundle members at the previously absent final path. It neither
reimplements table rules nor compensates for rejection. All prohibitions,
authority, dependency, envelope, testing, and incremental rules remain
authoritative in Validator Composition and Responsibility Boundaries.

## V2 Conformance Scenarios

The `rkm-autonomous-loop/v2` conformance suite must exercise `initialize`,
`validate-artifact`, `validate-session`, `transition`, `summarize`, and
`self-test` through the public CLI. It must use complete runtime directories
and disposable Git repositories below `/tmp` where practical; internal
function calls, fixture names, and asserted booleans alone are insufficient.

Every scenario must assert the exact exit-code class, diagnostic reason,
resulting artifacts and relevant content, atomicity, and authoritative
repository state before and after. Success requires exit zero and validated
content; rejection requires non-zero exit and a rule-specific diagnostic.
Pre- and post-command observations must establish no persistent validator
mutation of paths, commits, refs, branch, upstream, or Git configuration.
Claims about transient Worker or Reviewer behavior require the exact applicable
authoritative `AGENT_SUPERVISION` evidence.

Fixture setup and teardown may mutate only disposable repositories and must
leave the primary repository unchanged.

The suite must cover:

1. duplicate JSON keys and deterministic canonical output;
2. atomic initialization through one validated staging bundle and one
   staging-to-final directory rename, with no partial valid session or partial
   destination files;
3. every authoritative Git observation field and rejection of false
   cleanliness, alignment, changed-path, commit, protected-ref, or protected-
   main ancestry claims;
4. the six-product-file limit and its prior human-authorization exception;
5. initial implementation only after acceptance, a clean ancestry-valid
   baseline, and one atomic transition that registers the complete numbered
   decision, canonical digest, zero budget usage, unique assignment, unique
   Worker, applicable used identifiers, history, sequence, and state without a
   prior same-state RUN_STATE rewrite;
6. corrective entry with the exact non-null `correctiveContext` and retained
   pre-commit diff, and rejection for staging, unexpected paths, stale
   assignment, wrong context, or wrong trigger evidence;
7. post-publication correction from a clean accepted commit after immutable
   failed external-verification evidence;
8. decision-digest mutation, pre-registered decision state, partial atomic
   registration, premature replan decision creation, missing fresh replan
   decision or assignment, and mixed, predecessor, or unknown contract
   versions;
9. valid `BLOCKED` infeasibility through inspection and replan, valid
   `FAILED` or `INTERRUPTED` terminal recovery, structurally invalid Worker
   results, identity mismatches, duplicate identifiers, and invalid paths;
10. independently numbered immutable artifact families, including
    `AGENT_SUPERVISION-01.json`, and rejection of unnumbered, skipped,
    overwritten, missing, future-sequence, late, reused, or stale evidence;
11. atomic Worker and Reviewer registration and clearing, durable matching
    results, verdicts, authoritative supervision, exact embedded stream bytes,
    and exact process invocation, and rejection of active, unsupervised,
    stale-supervised, self-attesting, capture-mismatched, invocation-mismatched,
    or otherwise mismatched agents;
12. Reviewer `ACCEPT`, `REVISE`, and `STOP`, including invalid acceptance,
    one successful correction loop, and one successful replan through
    `INSPECTING_WORK`;
13. baseline, post-review, pre-commit, and external-correction validation
    phases with their required nullable or non-null references;
14. temporal semantics, including increasing transitions, non-decreasing
    artifact creation within one sequence, and `updatedAtUtc` agreement;
15. primary and isolated Git-observation non-substitution and exact external-
    verification references;
16. clean publication, accepted-commit ancestry, fresh local-main and origin-
    main ancestry, isolated consumer checks, substantive final reporting,
    mandatory routing through `FINALIZING`, terminal-disposition and reason-
    code consistency, all terminal outcomes, and protected-category
    escalation;
17. facade fail-closed behavior for missing, malformed, rejecting, or
    conflicting components;
18. production components remaining in-process, only the Git observer using
    read-only Git, and test-only subprocess use confined to disposable
    repositories;
19. separate Git-observer and agent-supervisor authority, with no Git ownership
    in supervision and no process-stop or transient-behavior inference in Git
    observation.

The following correction-family cases are mandatory at all three test layers;
the cells add layer-specific evidence and do not redefine their authoritative
contracts:

| Concern | Focused component self-tests | Boundary integration tests | Public-facade end-to-end tests |
| --- | --- | --- | --- |
| Initialization bootstrap | Accept one complete mutually consistent unpublished bundle and its single atomic directory publication; reject only RUN_STATE present, only `GIT_OBSERVATION-01.json` present, mismatched session identity, mismatched sequence or non-`INITIALIZING` state, wrong `bootstrapInitialization`, final-path publication before validation, non-atomic two-step publication, an already-existing final directory, interrupted staging publication, and staging debris treated as a session | Prove the Git observer, artifact loader, bootstrap validator, launcher publication boundary, transition validator, and facade agree on the same observation, initial RUN_STATE, identities, state zero, ancestry, timestamps, and absent-then-atomically-present final path; prove rejection publishes neither member and cannot be repaired by a same-state rewrite | Exercise `initialize`, `validate-artifact`, `validate-session`, and `summarize`; accept only the complete atomically published bundle and reject every focused case with non-zero exit, no valid final session, unchanged pre-existing final directory when applicable, and a rule-specific diagnostic; never report staging debris or either lone member as initialized |
| Atomic decision registration | Accept the complete ordered atomic update; reject a digest or mapping required before transition, a prior same-state RUN_STATE rewrite, partial registration, stale digest, missing zero budget entry, missing assignment or Worker registration, missing used identifier, and replan registration disagreement | Prove artifact loader, decision validator, transition validator, and lifecycle validator agree on the same decision, assignment, canonical digest, identifiers, transition sequence, and unchanged prior state after rejection | Exercise initial and post-replan success through `transition`; reject every partial or pre-registered variant with non-zero exit, unchanged RUN_STATE bytes, and a rule-specific diagnostic |
| Protected-main ancestry | Derive both exact booleans through the allowed merge-base operation; reject local main not ancestor, origin/main not ancestor, absent protected refs, and artifact `true` when authoritative observation is `false` | Prove Git-observer ancestry, transition launch gates, observation validation, finalization, and report inputs use the same fresh observation while keeping equality and ancestry distinct | Reject a divergent branch before option generation; separately reject local-main divergence, origin/main divergence, and unchanged protected refs that become or remain non-ancestors at finalization or completion; reject claimed-true artifact booleans against authoritative false values |
| Agent supervision | Accept every permitted terminal outcome combination, canonical empty and non-empty captures, and valid Worker and Reviewer binding; reject missing capture objects, inconsistent null or empty captures, invalid or noncanonical base64, wrong byte length, changed bytes, declared stream-digest mismatch, normalized or reconstructed output, truncation, stale or substituted captures, caller digest claims without bytes, processInvocation mismatch, supervisorEvidenceDigest mismatch, and every previously required identity, outcome, timestamp, sequence, freshness, reuse, stopped-state, self-attestation, and prohibited-action case | Prove the supervision validator, lifecycle validator, transition validator, finalization validator, and facade bind the exact same complete artifact, both capture-object identities and digests, decoded-byte digests, processInvocation identity, and complete-envelope digest; reject when a durable Worker result or Reviewer verdict claims one outcome but exact captured stream or processInvocation evidence proves another, including success versus failed, timed-out, interrupted, substituted-process, or prohibited-action evidence | Exercise every component case through `validate-artifact`, `validate-session`, `transition`, and terminal validation; prove durable result or verdict success cannot override missing, rejecting, contradictory, normalized, truncated, stale, substituted, or invocation-mismatched supervision; prove successful finalization and completion reject missing or unverifiable exact stream and invocation evidence while failed or interrupted finalization preserves it as a failure fact |

Budget behavior must be exercised as separate public-CLI scenarios:

| Scenario | Starting usage | Expected result and ending usage |
| --- | --- | --- |
| first revision | session `0`, decision `0`, limit `2` | `PASS`; session `1`, decision `1` |
| second revision | session `1`, decision `1`, limit `2` | `PASS`; session `2`, decision `2` |
| third revision | session `2`, decision `2`, limit `2` | `REJECT`; values unchanged |
| sole replan | session `0`, rejected decision `0`, limit `1` | `PASS`; session `1`, rejected decision `1` |
| second replan | session `1`, rejected decision `1`, limit `1` | `REJECT`; values unchanged |
| first commit | session `0`, decision `0`, limit `3` | `PASS`; session `1`, decision `1` |
| second commit | session `1`, decision `1`, limit `3` | `PASS`; session `2`, decision `2` |
| third commit | session `2`, decision `2`, limit `3` | `PASS`; session `3`, decision `3` |
| fourth commit | session `3`, decision `3`, limit `3` | `REJECT`; values unchanged |
| last-slot completion | charge changes remaining from `1` to `0` | later transitions `PASS` using the recorded charge |
| duplicate charge | operation already has a charge | `REJECT`; counters and charge list unchanged |

Each budget scenario verifies the charge, counters, identity, atomicity,
last-slot completion without rechecking capacity, and duplicate rejection.
Commit scenarios also prove that `COMMITTING` records pre-commit `HEAD` and an
unchanged pending operation without charging; only successful
`COMMITTING -> PUBLISHING` charges, appends, and clears it. The interruption
window must either resume a matching valid commit or restore pre-commit state;
usage remains unchanged before success.

Component, integration, and public-facade end-to-end tests must run through
`scripts/rkm-unit-tests.sh` or another existing standard entry point reached by
`make validate`. That later integration requires separate authorization; this
contract change authorizes no validator, test-runner, or Makefile edit.

## Compatibility Boundary

`rkm-autonomous-loop/v1` was an experimental predecessor.
`rkm-autonomous-loop/v2` supersedes it and is intentionally incompatible with
it. No `rkm-autonomous-loop/v1` validator was accepted for production use, so
this contract requires no automated migration.

`contractVersion` selects the exact validation contract. One session must use
one contract version consistently, and mixed-version sessions are invalid. An
`rkm-autonomous-loop/v2` validator must reject
`rkm-autonomous-loop/v1` artifacts; those artifacts are not valid
`rkm-autonomous-loop/v2` artifacts and must not be reinterpreted or silently
upgraded. The validator must also reject unknown future versions.

Compatibility must never be inferred from similar field names, artifact
names, states, or values. Any future migration must be explicit, separately
authorized, independently validated, and implemented without changing the
meaning or history of source artifacts.

Within `rkm-autonomous-loop/v2`, the atomic two-artifact initialization bundle,
`bootstrapInitialization`, exact ancestry booleans, required numbered
`AGENT_SUPERVISION` family, embedded capture objects, exact stream bytes and
digests, `processInvocation`, and complete-envelope
`supervisorEvidenceDigest` are mandatory compatibility-significant contract
requirements. A validator must not default a missing bootstrap or ancestry
value, infer ancestry from other Git facts, accept a partial or non-atomically
published initialization, treat a Worker result or Reviewer verdict as a
supervision substitute, reconstruct captured output, trust digest claims
without exact bytes, accept an unnumbered or differently named process
artifact, or silently migrate an earlier v2-shaped runtime that lacks these
requirements. Such a runtime is invalid under this exact contract and requires
an explicitly authorized migration rather than permissive interpretation.

The validator and launcher for `rkm-autonomous-loop/v2` must implement this
contract without changing:

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
