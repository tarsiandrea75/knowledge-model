# GB-006 Recovery State Autopilot Blocker

- Status: Implemented
- Priority: High
- Area: Automation governance

## Objective

Ensure that unattended autopilot stops when recovery reports
`RECOVERY_FAILED_NEEDS_MANUAL_FIX`, and that the stop decision is covered by
deterministic self-tests.

## Existing implementation

The guardrail is implemented by `scripts/rkm-autopilot.py`:

- `decide_recovery` returns a zero-command manual-fix plan for the failed
  recovery status.
- `recovery_plan_blocks_post_failure_push` prevents a post-failure push.
- The script self-test covers failed recovery, blocked IDE files, manual
  review, recovery availability and the normal no-recovery fallback.

## Validation

```bash
python3 scripts/rkm-autopilot.py --self-test
make validate
```

## Acceptance criteria

- [x] Failed recovery status produces no autopilot commands.
- [x] Failed recovery status blocks post-failure publication.
- [x] Deterministic self-tests cover the stop rule.
- [x] Backlog and rule coverage report reference the implementation.
