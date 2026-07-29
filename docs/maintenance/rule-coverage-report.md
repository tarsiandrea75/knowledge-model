# Rule Coverage Report

## Purpose

This report tracks RKM governance rules by enforcement level. It distinguishes rules that are documented, partially supported by automation, fully validated by standard checks or dedicated targets, and still dependent on human or agent discipline.

The report helps maintainers decide which rules should become automated checks. It should be treated as a conservative governance map, not as a maturity claim.

Use `docs/maintenance/governance-backlog.md` for actionable deferred governance work. Rules that are not yet automated should have corresponding backlog entries when they represent concrete implementation work, but this report should not duplicate the backlog table.

## Coverage Levels

- `Documented`: the rule exists in AGENTS files, maintenance docs, or task guides.
- `Partially Validated`: at least one automated check supports the rule, but the full behavior still requires reviewer judgment.
- `Validated`: the rule is enforced by standard validation or a dedicated validation target.
- `Not Yet Automated`: the rule is documented but currently relies on human or agent discipline.
- `Not Applicable`: the rule is contextual and should not be automated directly.

## Coverage Table

| Rule | Primary Location | Coverage Level | Automated Check | Notes |
| --- | --- | --- | --- | --- |
| Clean worktree before push, autopilot, or handoff. | `AGENTS.md`; `docs/maintenance/automation-guardrails.md` | Partially Validated | `make safe-push`; release and automation tooling inspect status in specific flows | The general handoff rule still requires the operator or assistant to inspect `git status --short`. |
| Runtime logs and scratch files must stay outside the repository. | `AGENTS.md`; `docs/maintenance/automation-guardrails.md` | Validated | `scripts/validate-runtime-artifacts.py`; `make runtime-artifacts-validate`; `make validate` | The detector rejects declared runtime directories, generated RKM or Codex run prefixes, and common runtime file suffixes without deleting artifacts. |
| Populated entity types must have a complete registry, schema, manifest, documentation, and graph-export package. | `data/AGENTS.md`; `docs/maintenance/task-guides/adding-new-entity-type.md` | Validated | `scripts/validate-entity-type-packages.py`; `make entity-type-package-validate`; `make validate` | The validator checks populated types and leaves registry-only abstract or planned types available without requiring data records. |
| Root `AGENTS.md` must remain concise. | `AGENTS.md`; `docs/maintenance/task-guides/rule-routing-validation.md` | Validated | `scripts/validate-agent-routing.py`; `make agent-routing-validate`; `make validate` | The validator enforces the root line budget. |
| Required local `AGENTS.md` files must exist. | `AGENTS.md`; `docs/maintenance/task-guides/rule-routing-validation.md` | Validated | `scripts/validate-agent-routing.py`; `make agent-routing-validate`; `make validate` | The validator checks the required local rule files. |
| Required task guides must exist. | `AGENTS.md`; `docs/maintenance/task-guides/README.md` | Validated | `scripts/validate-agent-routing.py`; `make agent-routing-validate`; `make validate` | The validator checks the required task guide inventory. |
| Task guides must use required headings. | `docs/maintenance/task-guides/README.md`; `docs/maintenance/task-guides/rule-routing-validation.md` | Validated | `scripts/validate-agent-routing.py`; `make agent-routing-validate`; `make validate` | The validator checks the required headings for task guides other than the index. |
| Root `AGENTS.md` must route to local rule files and task guides. | `AGENTS.md` | Validated | `scripts/validate-agent-routing.py`; `make agent-routing-validate`; `make validate` | The validator checks required root references, including local rule files and the task guide index. |
| Intended file changes should map to required root rules, local `AGENTS.md` files, task guides, risk notes, and checks before editing. | `AGENTS.md`; `docs/maintenance/task-guides/README.md`; `docs/maintenance/governance-backlog.md` | Validated | `scripts/rkm-route-task.py --self-test`; `make route-task`; `scripts/rkm-unit-tests.sh`; `make validate` | The task router CLI is self-tested and wired into the standard unit test step. |
| Local `AGENTS.md` files must reference relevant task guides. | Local `AGENTS.md` files; `docs/maintenance/task-guides/rule-routing-validation.md` | Validated | `scripts/validate-agent-routing.py`; `make agent-routing-validate`; `make validate` | The validator checks configured local-to-guide references. |
| Architecture docs must not mix concrete `data/` paths with invented IDs. | `AGENTS.md`; `docs/maintenance/automation-guardrails.md`; `docs/maintenance/task-guides/writing-architecture-doc.md` | Validated | `scripts/validate-agent-routing.py`; `make agent-routing-validate`; `make validate` | Current validation catches concrete `data/` paths combined with invented numeric example identifiers. |
| Failed newly added files must be discarded from both index and filesystem when recovery fails and the file should not be kept. | `docs/maintenance/automation-guardrails.md`; `docs/maintenance/task-guides/recovering-failed-new-file.md` | Not Yet Automated | None | This is an operational recovery procedure and still requires disciplined execution. |
| `RECOVERY_FAILED_NEEDS_MANUAL_FIX` must stop further autopilot. | `docs/maintenance/automation-guardrails.md`; `docs/maintenance/task-guides/unattended-autopilot.md`; `docs/maintenance/task-packets/GB-006-recovery-state-autopilot-blocker.md` | Validated | `scripts/rkm-autopilot.py` self-test; `make validate` | Failed recovery produces a zero-command manual-fix plan and blocks post-failure publication. |
| Unattended autopilot should use repeated `make autopilot N=1` rounds. | `docs/maintenance/automation-guardrails.md`; `docs/maintenance/task-guides/unattended-autopilot.md` | Partially Validated | Automation target caps and cockpit checks support bounded runs | The exact unattended loop pattern remains operator discipline. |
| Autopilot cycles should have a configurable per-cycle wall-clock timeout. | `docs/maintenance/governance-backlog.md`; `docs/maintenance/task-guides/unattended-autopilot.md` | Partially Validated | `scripts/rkm-unit-tests.sh`; `scripts/rkm-autocycle.sh` timeout input validation | GB-042 is implemented with Make variable `PER_CYCLE_TIMEOUT_SECONDS` and environment variable `RKM_PER_CYCLE_TIMEOUT_SECONDS`. Unit tests validate timeout input handling; operational timeout expiry depends on GNU `timeout` at run time. |
| Schema, registry, validator, exporter, Makefile, release-process, graph-contract, and migration changes require explicit prompts. | `AGENTS.md`; `docs/maintenance/automation-guardrails.md` | Not Yet Automated | None | Prompt intent is contextual and currently reviewed by humans or agents. |
| Do not add `schema/definitions/<name>.schema.json` when `schema/<name>.schema.json` already exists unless the same commit performs an atomic refactor. | `AGENTS.md`; `docs/maintenance/automation-guardrails.md`; `docs/maintenance/task-guides/refactoring-schema-definition.md` | Validated | `scripts/validate-schema-duplicate-contracts.py`; `make schema-duplicate-contracts-validate`; `make validate` | The validator requires a same-name first-class schema to visibly compose from the reusable definition. |
| Schema definition extraction must update first-class schema, examples, tests, docs, and validation coverage in the same commit. | `docs/maintenance/automation-guardrails.md`; `docs/maintenance/task-guides/refactoring-schema-definition.md` | Partially Validated | `scripts/validate-schema-duplicate-contracts.py`; `make schema-duplicate-contracts-validate`; `make validate` | Composition is validated for same-name schema pairs, but semantic equivalence, migration safety, examples, tests, and documentation coverage still require reviewer judgment. |
| Relationship predicates must be reused before adding new ones. | `docs/maintenance/automation-guardrails.md`; `registries/AGENTS.md` | Not Yet Automated | None | Current validation can check registered predicates in data, but not semantic reuse before a new predicate is added. |
| Hard dependency predicates such as `REQUIRES` require explicit justification. | `docs/maintenance/automation-guardrails.md`; relationship task guides | Not Yet Automated | None | The need for a hard dependency is semantic and reviewer-driven. |
| Adding a new data entity type requires a complete package: records, manifest, validation compatibility, graph export support, schema provenance, docs, and self-test coverage. | `data/AGENTS.md`; `docs/maintenance/task-guides/adding-new-entity-type.md` | Not Yet Automated | None | Existing validators check pieces once wired, but do not detect package completeness for a new entity type. |
| Relationship sets must reference existing source and target IDs and matching source and target data files. | `data/AGENTS.md`; `docs/maintenance/task-guides/adding-relationship-set.md` | Validated | `scripts/validate-data.py`; `make data-validate`; `make validate` | Data validation checks endpoint existence and declared source and target data file matching. |
| Relationship support must cross-reference valid references, claims, evidence, and relationship IDs. | `data/AGENTS.md`; `docs/maintenance/task-guides/adding-relationship-support.md` | Validated | `scripts/validate-data.py`; `make data-validate`; `make validate` | Data validation checks relationship support links resolve. |
| Graph exporters must preserve endpoint integrity, schema validation, and provenance consistency. | `docs/maintenance/graph-export-contract.md`; `docs/maintenance/task-guides/updating-graph-export.md` | Partially Validated | `scripts/validate-graph-exports.py`; graph export generation checks; `make graph-export-validate`; `make validate` | Schema validation and endpoint existence are validated. Broader provenance consistency still requires exporter tests and review. |
| Validation script changes must include self-tests and must not silently weaken validation. | `scripts/AGENTS.md`; `docs/maintenance/task-guides/updating-validation-scripts.md` | Partially Validated | `scripts/rkm-unit-tests.sh`; `make validate` includes validator self-tests | Self-tests run, but reviewers must still judge whether changed validation semantics were weakened. |
| Release preparation requires clean worktree, full validation, release check, changelog or release docs, and version consistency. | `docs/maintenance/task-guides/preparing-release.md`; release docs | Partially Validated | `make release-check`; `make validate`; `scripts/rkm-release-check.py --self-test` | Release checks enforce several readiness gates. Changelog and release-document adequacy still require review. |
| Existing tags must not be modified. | `AGENTS.md`; `docs/maintenance/automation-guardrails.md`; release task guides | Not Applicable | None | This is a contextual governance rule for release operations and should remain an explicit human-controlled action. |

## Highest-Value Automation Candidates

1. Relationship predicate reuse assistant or reviewer check.
2. Recovery state validator that blocks autopilot when recovery failed.
3. Rule coverage consistency validator.
4. Markdown JSON example validator.

## Maintenance Rules

- Update this report when a documented rule becomes validated.
- Link actionable enforcement gaps to `docs/maintenance/governance-backlog.md` when the gap represents planned work.
- Do not inflate maturity claims from documentation alone.
- Prefer small validators with self-tests.
- A rule may remain documented-only if it requires human architectural judgment.
