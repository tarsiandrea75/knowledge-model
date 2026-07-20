# Codex Execution Policy

## Purpose

This policy defines how RKM selects deterministic checks, Codex execution profiles, semantic review strength, escalation behavior, and execution telemetry.

It implements the deterministic-first direction accepted in `LH-009` and tracked by `GB-044 Adaptive Codex Model Routing And Token Budgeting`.

The policy optimizes capability allocation. It does not weaken repository governance, bounded-change rules, validation, protected-main controls, semantic independence, or product-owner authority.

## Principles

1. Use deterministic tools before invoking a model.
2. Do not ask a model to reconfirm facts already proven by scripts or validators unless semantic interpretation remains necessary.
3. Select the least expensive profile that is competent for the task.
4. Escalate when uncertainty, contradiction, or task complexity exceeds the assigned profile.
5. Keep Creator and Reviewer strength proportional to their distinct risks.
6. Generate compact evidence bundles before semantic review.
7. Record profile selection, execution outcome, validation result, verdict, and escalation reason.
8. Keep exact model bindings configurable and separate from policy semantics.
9. Never resume an expensive retry loop without new evidence or a stronger profile.
10. Strategic direction and integration into `main` remain explicit product-owner decisions.

## Deterministic-First Execution

The following work should normally be completed without a model:

- Git branch, ref, merge-base, ancestry, and clean-worktree checks;
- file existence, path scope, line count, and SHA-256 checks;
- manifest and registry parsing;
- schema and data validation;
- identifier and relationship consistency checks;
- generated-artifact regeneration and byte comparison;
- Make target and CLI option discovery;
- command execution and exit-code classification;
- whitespace and final-newline checks;
- structured extraction from machine-readable files;
- token-budget arithmetic;
- evidence-bundle generation;
- exact matching against allowed verdicts or output schemas.

A model may interpret deterministic results, but must not replace an available deterministic check.

## Execution Tiers

RKM uses semantic tiers. Profile names and model bindings are configuration, not permanent repository contracts.

### Tier 0: Deterministic

- Model call: none.
- Typical work: validation, counting, hashing, Git inspection, graph consistency, routing facts, budget checks.
- Reviewer: none unless a semantic claim is produced from the deterministic result.

### Tier 1: Mechanical Model-Assisted

- Intended profile: `rkm-mechanical`.
- Candidate binding: GPT-5.4 Mini or another current low-cost coding-capable model.
- Default reasoning: `low`.
- Typical work:
  - constrained formatting;
  - structured extraction from already selected sources;
  - compact diff summaries;
  - simple classification;
  - bounded wording changes with no architectural effect.
- Escalate when sources conflict, scope expands, or semantic judgment becomes material.

### Tier 2: Bounded Semantic

- Intended profile: `rkm-bounded`.
- Candidate binding: GPT-5.6 Luna or another current low-cost semantic coding model.
- Default reasoning: `low` or `medium`.
- Typical work:
  - single-file documentation synchronization;
  - conservative record wording;
  - task-guide updates;
  - small governance clarifications;
  - no-change audits.
- Reviewer may use the same tier for low-consequence changes or the engineering tier when false acceptance would be costly.

### Tier 3: Engineering

- Intended profile: `rkm-engineering`.
- Candidate binding: GPT-5.6 Terra or another current balanced engineering model.
- Default reasoning: `medium` or `high`.
- Typical work:
  - implementation scripts;
  - validation changes;
  - automation and recovery logic;
  - semantic record review;
  - governance changes with operational consequences;
  - non-trivial debugging.
- This is the default tier for substantive Creator or Reviewer work when lower tiers are insufficient.

### Tier 4: Strategic

- Intended profile: `rkm-strategic`.
- Candidate binding: GPT-5.6 Sol or another current strongest available reasoning model.
- Default reasoning: `high` or `xhigh`.
- Typical work:
  - architecture and ontology design;
  - schema evolution;
  - cross-cutting automation;
  - unresolved contract conflicts;
  - Product Director design;
  - integration analysis;
  - high-risk independent review;
  - strategic planning and brainstorming.

### Tier 5: Exceptional Multi-Agent

- Intended profile: `rkm-exceptional`.
- Use only when the task genuinely benefits from decomposition or parallel specialist work.
- It must not be the default for bounded documentation, simple review, validation, or routine code changes.
- The operation contract must state why multi-agent execution is necessary.

## Creator and Reviewer Selection

Creator and Reviewer profiles may differ.

Examples:

| Change type | Creator | Reviewer |
|---|---|---|
| Fully deterministic | none | none |
| Mechanical documentation | `rkm-mechanical` | none or `rkm-mechanical` |
| Bounded semantic documentation | `rkm-bounded` | `rkm-bounded` or `rkm-engineering` |
| Ordinary code or governance | `rkm-engineering` | `rkm-engineering` |
| Schema, ontology, architecture | `rkm-strategic` | independently `rkm-strategic` |
| Integration decision support | `rkm-strategic` | product-owner decision |

Reviewer strength must reflect the probability and consequence of false acceptance, not merely the model used by the Creator.

A `NO_CHANGE_REQUIRED` result does not require an independent Reviewer when:

- the Creator made no repository change;
- deterministic scope checks confirm a clean worktree and index;
- the operation contract does not require semantic acceptance of a new claim.

## Risk Signals

The selector should increase the execution tier for any of the following:

- paths under `schema/` or `docs/architecture/`;
- ontology, entity-type, relationship-type, evidence, or lifecycle changes;
- multiple authorized project files;
- generated artifacts whose source contract also changes;
- changes to validation, recovery, Director, autopilot, budget, or safe-push logic;
- conflicts between canonical sources;
- external factual research;
- changes affecting release or integration;
- a previous invalid result, `REVISE`, or `STOP`;
- high downstream cost of false acceptance;
- explicit product-owner request for deep strategic analysis.

The selector should decrease model use when:

- all required outcomes are decidable through deterministic checks;
- the target is already current and `NO_CHANGE_REQUIRED` can be proven;
- the task is an exact replacement with fully specified before-and-after values;
- validation and machine-readable contracts cover the complete acceptance condition.

## Evidence Bundles

Before semantic review, the wrapper should generate a compact machine-readable evidence bundle containing only relevant proven facts, such as:

- branch, HEAD, upstream, and protected-main refs;
- authorized and changed paths;
- candidate SHA-256;
- routed readings, guides, risks, and checks;
- validation command results;
- manifest counts;
- lifecycle summaries;
- graph node and edge counts;
- exact commands exercised;
- Creator profile and result;
- unresolved semantic questions.

The Reviewer should receive:

1. the operation goal;
2. the complete target or staged diff;
3. the evidence bundle;
4. directly relevant canonical sources;
5. permission to inspect additional sources when a claim remains uncertain.

A Reviewer should not reread unrelated repository areas merely to reconfirm deterministic invariants.

## Escalation

A profile must return or trigger escalation when:

- the required task exceeds its permitted tier;
- canonical sources conflict;
- the model cannot determine a safe bounded edit;
- output violates its schema or first-line contract;
- validation fails for a reason not already understood;
- unexpected paths change;
- a Reviewer cannot issue a grounded verdict;
- external research is required but unavailable;
- model availability differs from configured bindings.

The default escalation sequence is one step at a time:

```text
deterministic -> mechanical -> bounded -> engineering -> strategic
```

Do not repeat the same failed call without changed evidence, a corrected prompt, or a stronger profile.

A `STOP` remains terminal for the current candidate unless a separately authorized recovery or replanning operation begins.

## Context and Output Budgeting

Prompts should be bounded by relevance.

Prefer:

- stable shared prompt prefixes;
- compact evidence bundles;
- exact source lists;
- machine-readable output schemas;
- low verbosity for classification and routing;
- explicit maximum call and retry counts;
- deterministic preprocessing;
- targeted source opening after uncertainty.

Avoid:

- repeated full-repository discovery;
- asking Creator and Reviewer to read identical irrelevant material;
- long narrative restatement of already proven facts;
- reusing a strategic profile for mechanical preflight;
- unconstrained retries after quota, timeout, or malformed output.

## Model Availability

Exact model names in profile configuration are replaceable bindings.

Before a campaign or unattended run, the wrapper should:

1. verify that the configured profile exists;
2. verify that Codex CLI accepts the selected configuration;
3. perform a minimal preflight only when a model call is actually required;
4. stop cleanly on quota or authentication failure;
5. report a suggested available fallback without silently changing semantic tier.

Fallbacks must preserve or increase required capability. Cost alone must not justify routing a strategic task to a weaker model.

## Telemetry

Every model-assisted operation should record, when available:

- operation ID;
- selected semantic tier;
- profile name;
- model binding;
- reasoning effort;
- sandbox mode;
- approval policy;
- authorized paths;
- evidence-bundle path and digest;
- prompt and output artifact paths;
- call count;
- retry count;
- execution result;
- validation result;
- Reviewer verdict;
- escalation source and destination;
- token or credit use;
- elapsed time;
- final commit and push result.

Telemetry is operational evidence. It does not outrank repository contracts or canonical data.

## Integration Requirements

The adaptive routing layer should integrate incrementally with:

- `scripts/rkm-route-task.py`;
- `scripts/rkm-cycle.sh`;
- `scripts/rkm-discover.sh`;
- `scripts/rkm-recover-revise.sh`;
- `scripts/rkm-codex-commit.sh`;
- `scripts/rkm-director.sh`;
- budget and run-ledger tooling;
- autopilot and cockpit surfaces;
- validation and unit tests.

Each integration must remain a bounded operation with explicit scope, tests, validation, and review appropriate to its risk tier.

## Initial Implementation Order

1. Add the deterministic profile selector.
2. Add selector self-tests and machine-readable output.
3. Add named profile templates.
4. Add the unified Codex execution wrapper.
5. Add evidence-bundle generation.
6. Integrate one existing execution path at a time.
7. Add usage and escalation telemetry.
8. Update routing, guardrails, rule coverage, cockpit, and maturity documentation as implementation becomes durable.
9. Resume the protected Track A documentation campaign with adaptive routing.
10. Perform the final read-only integration-readiness audit before Andrea chooses an integration form.

## Non-Goals

This policy does not:

- guarantee that a cheaper model will be sufficient;
- permanently bind RKM to specific model names;
- permit silent fallback to a weaker semantic tier;
- remove independent review where semantic risk requires it;
- authorize multi-file scope expansion;
- authorize integration into `main`;
- replace repository validation;
- make run summaries authoritative over repository state.
