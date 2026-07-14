# Rule Routing Validation

## Purpose

Rule routing validation makes the distributed agent rules testable. It checks that root `AGENTS.md`, local `AGENTS.md` files, and task guides remain connected, concise, and enforceable through the standard validation pipeline.

## When to Use

Use this guide when changing root agent routing, local agent rules, task guides, architecture example rules, `scripts/validate-agent-routing.py`, `make agent-routing-validate`, or the validation pipeline step that runs agent rule routing validation.

## Required Readings

- Root `AGENTS.md` for repository invariants and routing.
- The local `AGENTS.md` file for any affected area.
- `docs/maintenance/automation-guardrails.md` for automation and handoff expectations.
- `docs/maintenance/task-guides/updating-validation-scripts.md` when changing the validator implementation.

## Required Checks

- Run `python3 scripts/validate-agent-routing.py --self-test` after changing the validator.
- Run `make agent-routing-validate` after changing agent rules or task guides.
- Run `make validate` before reporting the repository as ready.
- Inspect `git status --short` before handoff.

## Common Failure Modes

- Adding a local rule file without routing to an existing task guide.
- Adding a task guide without the required Markdown headings.
- Expanding root `AGENTS.md` with long-form operational guidance that belongs in a local rule file or task guide.
- Referencing concrete `data/` paths in architecture docs while also using invented example IDs.
- Adding a guide to the repository but missing the task-guide README or root routing reference.

## Done Criteria

- Required local rule files and task guides exist.
- Root `AGENTS.md` references the local rule files, automation guardrails, and task-guide index.
- Local rule files route readers to relevant task guides where such guides exist.
- Agent rule routing validation and full repository validation pass.
- The final `git status --short` output has been reviewed.
