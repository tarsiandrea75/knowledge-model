# RKM-002: Human-Safe Push Alias

## Status

DONE

## Objective

Replace the repository's direct-push convenience targets with a documented
human-only alias that invokes the machine-local protected push wrapper after
validation and a clean working-tree check.

## Scope

- Update the RKM `Makefile` push targets to invoke only
  `$HOME/bin/codex-safe-git-push-current` through its absolute machine-local
  path.
- Preserve validation and clean-tree checks before the wrapper invocation.
- Document that Codex must not invoke the target indirectly; the human runs it
  from a normal WSL shell after explicit authorization.
- Update the RAG and RKM durable handoff records with the current autonomy and
  commit checkpoints.

## Out of scope

- No push execution.
- No changes to the push wrapper, credentials, remotes, branches, tags, refs,
  worktrees, or Git history.
- No attempt to grant Codex authority over publication.
- No change to RAG runtime behavior or evaluation logic.

## Acceptance criteria

- RKM `make safe-push` performs validation, requires a clean tree, and invokes
  only the protected push wrapper.
- RKM `make push` cannot bypass the protected wrapper.
- Documentation identifies both targets as human-only and preserves Codex's
  prohibition on invoking push, directly or indirectly.
- RAG and RKM handoffs record the current branch, recent commits, clean-state
  expectations, and the human-only push boundary.
- All relevant repository validations pass.

## Required validation

```bash
make validate
make rag-recommendation-adapter-test
git diff --check
```

## Stop conditions

Stop if implementing the alias requires changing the machine-local wrapper,
granting Codex push authority, changing repository topology, accessing
credentials, or executing a push.

## Handoff

The RKM `push` and `safe-push` targets now share the validated human-only
protected wrapper path. The wrapper itself was not modified and no push was
executed. The RKM full validation suite passed after the Makefile, policy
documentation, handoff, and task-packet updates. Codex remains prohibited
from invoking the target or the push wrapper, directly or indirectly.
