# GB-009 Markdown JSON Example Validator

- Status: Implemented
- Priority: Medium
- Area: Documentation validation

## Objective

Provide a targeted check for JSON fenced examples in Markdown documentation.

## Implementation

`scripts/validate-markdown-json.py` validates explicitly selected Markdown
files or directories. The public target is:

```bash
make markdown-json-validate DOCS_PATH=docs/maintenance/rag-recommendation-consumer-walkthrough.md
```

The check is intentionally opt-in by path until the existing documentation
inventory is audited for all JSON examples.

## Validation

```bash
python3 scripts/validate-markdown-json.py --self-test
make validate
```

## Acceptance criteria

- [x] Valid JSON fenced examples pass.
- [x] Invalid JSON reports the Markdown path and line.
- [x] The targeted Make interface avoids reserved environment variable names.
- [x] Self-test coverage runs in the standard RKM unit-test step.
