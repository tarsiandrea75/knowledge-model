# GB-003 Relationship Predicate Reuse Checker

- Status: Implemented
- Priority: High
- Area: Validation

## Objective

Provide a deterministic review assistant that identifies existing relationship
predicates with overlapping documented semantics before a new predicate is
added.

## Implementation

`scripts/review-relationship-predicate-reuse.py` tokenizes predicate type,
label, description, category and canonical direction fields, then reports
lexical-overlap candidates above a configurable threshold. It is advisory by
default and fails only when an explicit proposed-predicate review finds a
candidate, preserving human semantic judgment.

The public interface is:

```bash
make relationship-predicate-review TYPE=DEPENDS_ON LABEL="Depends on" DESCRIPTION="Declares a dependency on a capability." CATEGORY=Dependency
```

## Validation

```bash
python3 scripts/review-relationship-predicate-reuse.py --self-test
make validate
```

## Acceptance criteria

- [x] Existing registry entries can be compared with a proposed predicate.
- [x] Self-tests cover matching and non-matching cases.
- [x] The normal validation pipeline remains unchanged and green.
- [x] The assistant does not mutate canonical registry or data files.
