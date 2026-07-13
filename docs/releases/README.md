# Release Documentation

This directory contains release documentation for RAG Knowledge Model.

Release notes describe the scope of a package, the validation commands used to check it, compatibility expectations for consumers, and known limitations. They are intended to help maintainers and internal consumers understand what a specific version can be used for and what remains experimental.

Release documentation is separate from git tags. A release note can be prepared before a tag exists, but a git tag must be created intentionally as a separate release action. Do not assume that a documented release version has a corresponding git tag unless the tag exists in the repository.

Before creating a release tag, maintainers should run:

```bash
make release-check
```

The release check is a strict pre-tag readiness gate. It validates that the repository is clean, required release artifacts are present, validation passes, graph export is deterministic, and the worktree remains clean after export. It does not create a git tag. Tags are created intentionally by maintainers after readiness passes.

The first documented package is `v0.1.0-alpha`, an internal alpha intended for evaluation, onboarding, and consumer feedback.
