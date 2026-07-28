# Codex Safe Autonomy

## Purpose

This machine-local configuration lets Codex work autonomously on ordinary
files in the two authorized repositories without repeated approval prompts,
while retaining technical protections around the filesystem and Git. It is a
local operating aid for trusted maintenance sessions, not a repository-owned
credential or unrestricted machine-access mechanism.

## Launch commands

Start Codex with the protected launcher and choose the desired initial
repository:

```bash
$HOME/bin/codex-safe-autonomy rag
$HOME/bin/codex-safe-autonomy rkm
$HOME/bin/codex-safe-autonomy rag resume <SESSION_ID>
$HOME/bin/codex-safe-autonomy rkm resume <SESSION_ID>
```

`rag` selects `BuildingRAGAgentsWithLLMs` as the initial working directory.
`rkm` selects `knowledge-model` as the initial working directory. In both
cases Codex is authorized to access both repositories listed below. The
`rag` and `rkm` arguments choose only the initial repository; they do not
restrict work to a single repository.

## Authorized repositories

- `/mnt/c/Users/andrea.tarsi/projects/AI/BuildingRAGAgentsWithLLMs`
- `/mnt/c/Users/andrea.tarsi/projects/AI/knowledge-model`

## Safety guarantees

- The configured sandbox is `workspace-write`.
- The configured approval policy is `never` for operations inside the
  authorized boundary.
- Writes are allowed only in the authorized repositories and the configured
  temporary directories.
- The only operational branch is `codex/open-autonomy-era`.
- Creating, changing, renaming, or deleting branches is forbidden.
- Altering tags, refs, reflogs, worktrees, or remotes is forbidden.
- Reset, rebase, merge, and history rewriting are forbidden.
- Force pushes are forbidden.
- No push is performed without explicit user authorization.
- A forbidden operation must fail without requesting permission expansion or
  broader access.

## Safe Git wrappers

Use these wrappers for the permitted Git mutations:

```text
$HOME/bin/codex-safe-git-add
$HOME/bin/codex-safe-git-commit
$HOME/bin/codex-safe-git-push-current
```

Direct mutating Git commands must not be used. In particular, do not bypass
the wrappers to alter branches, refs, history, remotes, or worktrees.

## Machine-local files

The launcher and its policy files are machine-local and are not automatically
part of either repository:

```text
~/.codex/config.toml
~/.codex/rules/default.rules
~/.codex/AGENTS.md
~/bin/codex-safe-autonomy
~/bin/codex-safe-git-add
~/bin/codex-safe-git-commit
~/bin/codex-safe-git-push-current
~/.codex/backup-safe-autonomy-*
```

This document intentionally contains no tokens, passwords, keys, or other
credential material.

## Recovery and verification

Use these commands to verify the local Codex configuration and repository
state:

```bash
codex --strict-config --version
git status --short --branch
git branch --show-current
```

The expected operational branch is:

```text
codex/open-autonomy-era
```

For repository-specific validation, use `scripts/verify.sh fast` in
`BuildingRAGAgentsWithLLMs` and `make validate` in `knowledge-model`, subject
to each repository's current `AGENTS.md` and task instructions.

## Security

- Never save tokens, passwords, SSH keys, or credentials in either repository.
- The launcher grants operational autonomy inside the defined boundary; it
  does not grant unlimited access to the machine.
- Never attempt to bypass the sandbox, rules, or safe Git wrappers.
- Keep machine-local policy and credential material outside the repositories.

<!-- SAFE_GIT_EXECUTION_BOUNDARY_BEGIN -->
## Git commit boundary

The launcher intentionally separates autonomous repository work from Git
metadata mutation:

- Codex may create, edit, move, delete, inspect, and validate ordinary files in
  the two authorized repositories.
- The `workspace-write` sandbox keeps `.git` read-only.
- With `approval_policy = "never"`, Codex does not request permission to escape
  the sandbox.
- Consequently, Codex prepares and validates changes but does not stage,
  commit, or push them from inside the session.

After Codex reports that the changes are ready, the human operator runs the
safe wrappers from a normal WSL shell, using the repository as the current
directory:

```bash
$HOME/bin/codex-safe-git-add <relative-path> [additional-relative-paths]
$HOME/bin/codex-safe-git-commit "commit message"
```

A push is performed only after explicit user authorization:

```bash
$HOME/bin/codex-safe-git-push-current
```

The wrappers enforce the authorized repositories and the branch
`codex/open-autonomy-era`. This is a deliberate safety boundary, not an error to
work around. Codex must never use direct mutating Git commands or attempt to
bypass the sandbox.
<!-- SAFE_GIT_EXECUTION_BOUNDARY_END -->
