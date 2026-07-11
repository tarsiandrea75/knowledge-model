SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c

CYCLE_N := $(or $(N),3)
DISCOVER_N := $(or $(N),5)
TAIL_LINES ?= 40

.PHONY: validate status log cycle discover push safe-push fix-eof clean-discovery-artifacts help

validate:
	bash scripts/validate-rkm.sh

status:
	git status --short

log:
	git log --oneline -n 10

cycle:
	set +e; \
	bash scripts/rkm-cycle.sh "$(CYCLE_N)" > /tmp/rkm-cycle-output.txt; \
	exit_code="$$?"; \
	set -e; \
	printf 'rkm-cycle exit code: %s\n' "$$exit_code"; \
	tail -n "$(TAIL_LINES)" /tmp/rkm-cycle-output.txt; \
	git status --short; \
	exit "$$exit_code"

discover:
	set +e; \
	bash scripts/rkm-discover.sh "$(DISCOVER_N)" > /tmp/rkm-discovery-output.txt; \
	exit_code="$$?"; \
	set -e; \
	printf 'rkm-discover exit code: %s\n' "$$exit_code"; \
	tail -n "$(TAIL_LINES)" /tmp/rkm-discovery-output.txt; \
	git status --short; \
	exit "$$exit_code"

push:
	git push

safe-push: validate
	@if [[ -n "$$(git status --porcelain)" ]]; then \
		git status --short; \
		printf 'Working tree must be clean before pushing.\n' >&2; \
		exit 1; \
	fi
	git log --oneline -n 5
	git push

fix-eof:
	@if [[ -z "$(strip $(FILE))" ]]; then \
		printf 'FILE is required. Usage: make fix-eof FILE=path/to/file\n' >&2; \
		exit 1; \
	fi
	bash scripts/rkm-fix-eof.sh "$(FILE)"

clean-discovery-artifacts:
	find . -maxdepth 1 \( \
		-type d \( -name 'rkm-discovery-report-*' -o -name 'rkm-discovery-*' \) \
		-o -type f \( -name 'rkm-discovery-report-*.zip' -o -name 'rkm-discovery-*.zip' \) \
	\) -exec rm -rf -- {} +

help:
	@printf 'RKM developer commands:\n'
	@printf '  make validate                    Run bash scripts/validate-rkm.sh.\n'
	@printf '  make status                      Show git status --short.\n'
	@printf '  make log                         Show the 10 most recent commits.\n'
	@printf '  make cycle [N=3]                 Run scripts/rkm-cycle.sh N, save stdout to /tmp/rkm-cycle-output.txt, print exit code, output tail, and status.\n'
	@printf '  make discover [N=5]              Run scripts/rkm-discover.sh N, save stdout to /tmp/rkm-discovery-output.txt, keep stderr visible, print exit code, output tail, and status.\n'
	@printf '  make push                        Run git push.\n'
	@printf '  make safe-push                   Validate, require clean git status, show recent commits, then push.\n'
	@printf '  make fix-eof FILE=path/to/file   Run scripts/rkm-fix-eof.sh on FILE.\n'
	@printf '  make clean-discovery-artifacts   Remove root-level rkm-discovery-report-* and rkm-discovery-* directories or zip files.\n'
	@printf '  make help                        Show this help.\n'
