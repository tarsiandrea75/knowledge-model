# Codex Safe Autonomy

## Purpose

This machine-local configuration lets Codex work autonomously on ordinary
files in the two authorized repositories without repeated approval prompts,
while retaining technical protections around the filesystem and Git. After
complete required validation and review evidence pass, the recommended launcher
also permits an autonomous protected local commit. It is a local operating aid
for trusted maintenance sessions, not a repository-owned credential or
unrestricted machine-access mechanism.

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
- A normal local commit may be created automatically only after complete
  required validation and review evidence pass, and only through the protected
  wrappers with explicit paths.
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
## Safe autonomy and commit modes

The machine provides two launch modes.

### Autonomous work with protected commits (default)

```bash
$HOME/bin/codex-safe-autonomy rag
$HOME/bin/codex-safe-autonomy rkm
```

This mode uses `workspace-write` with `approval_policy = "on-request"` only
to allow the narrowly allowlisted protected wrappers outside the read-only
`.git` sandbox. Codex may edit and validate ordinary files in both authorized
repositories. After all required validation and review evidence pass, it stages
explicit paths and creates a normal local commit through those wrappers. The
allowlisted wrapper invocations do not prompt the human operator.

### Compatibility launcher

```bash
$HOME/bin/codex-safe-autonomy-commit rag
$HOME/bin/codex-safe-autonomy-commit rkm
```

A previous session can also be resumed through the compatibility launcher:

```bash
$HOME/bin/codex-safe-autonomy-commit rag resume SESSION_ID_VALUE
$HOME/bin/codex-safe-autonomy-commit rkm resume SESSION_ID_VALUE
```

This compatibility launcher has the same commit-capable protected mode as the
recommended launcher. `.git` remains read-only inside the sandbox.

After successful validation, Codex must use outside-sandbox execution only for
the following exact, machine-local wrappers:

```bash
/home/andreatarsi/bin/codex-safe-git-add path/to/file
/home/andreatarsi/bin/codex-safe-git-commit "formal technical commit message"
```

Execpolicy marks those wrappers as `allow`, so matching invocations run without
prompting the human operator. The wrappers independently enforce the authorized
repositories and the branch `codex/open-autonomy-era`.

Codex must stage explicit relative paths, invoke the wrappers separately, and
create only normal new commits. Direct mutating Git commands, commit amendment,
branch changes, ref changes, history rewriting, worktree changes, remote
changes, and force operations remain forbidden.

### Human-only push boundary

Codex cannot invoke the push wrapper. A push requires explicit human
authorization and execution from a normal WSL shell:

```bash
$HOME/bin/codex-safe-git-push-current
```

This separation permits autonomous implementation and local commits while
preserving human control over publication to the remote repository.

In the RKM repository, `make safe-push` is a human-only convenience target. It
validates the repository, requires a clean working tree, and then invokes
`/home/andreatarsi/bin/codex-safe-git-push-current`. The `make push` target is
an alias for the same protected path. Codex must not invoke either target,
directly or indirectly; the human operator runs one of them from a normal WSL
shell after explicit authorization.
<!-- SAFE_GIT_EXECUTION_BOUNDARY_END -->

<!-- REPOSITORY_LANGUAGE_POLICY_BEGIN -->
## Repository language policy

Human conversation may use Italian or Rioplatense Spanish. Repository-facing
and persisted artifacts use formal, internationally understandable technical
English by default.

The policy applies to source code, identifiers, comments, docstrings,
documentation, task packets, ADRs, schemas, fixtures, examples, tests, CLI
text, filenames, error messages, and commit messages. Other languages are used
only for explicit localization or translation requirements.
<!-- REPOSITORY_LANGUAGE_POLICY_END -->
