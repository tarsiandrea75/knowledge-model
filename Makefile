SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c

CYCLE_N := $(or $(N),3)
AUTOCYCLE_N := $(or $(N),3)
DISCOVER_N := $(or $(N),5)
TAIL_LINES ?= 40
FILES ?=
DAILY_BUDGET ?= 300000
BUDGET_SAFETY_FACTOR ?= 1.25
BUDGET_RESERVE_RATIO ?= 0.20
BUDGET_WINDOW_HOURS ?= 24
BUDGET_GRACE_TOKENS ?= 10000
BUDGET_GRACE_RATIO ?= 0.02
BUDGET_TARGET ?= $(AUTOCYCLE_N)
NEXT_ACTION_TARGET ?= $(AUTOCYCLE_N)
AUTOPILOT_TARGET ?= $(AUTOCYCLE_N)
FORCE ?= false
WORKING_TARGET_MAX ?= 5
PER_CYCLE_TIMEOUT_SECONDS ?= $(if $(RKM_PER_CYCLE_TIMEOUT_SECONDS),$(RKM_PER_CYCLE_TIMEOUT_SECONDS),3600)
EVIDENCE_AS_OF_DATE ?=
EVIDENCE_MAX_AGE_DAYS ?= 365

.PHONY: validate runtime-artifacts-validate entity-type-package-validate data-validate graph-export data-graph-export graph-export-validate agent-routing-validate schema-duplicate-contracts-validate relationship-predicate-review rule-coverage-validate markdown-json-validate validation-inventory-validate release-check route-task rag-recommendation-adapter-test external-rag-evidence-review status log cycle autocycle discover push safe-push install-hooks fix-eof codex-commit recover-revise recovery-plan clean-discovery-artifacts usage-report budget-init budget-report budget-check budget-reset-window next-action autopilot autopilot-dry-run autopilot-recover autopilot-status cockpit cockpit-summary help

validate:
	bash scripts/validate-rkm.sh

runtime-artifacts-validate:
	python3 scripts/validate-runtime-artifacts.py

entity-type-package-validate:
	python3 scripts/validate-entity-type-packages.py

data-validate:
	python3 scripts/validate-data.py

graph-export:
	python3 scripts/export-fixtures-graph.py

data-graph-export:
	python3 scripts/export-data-graph.py

graph-export-validate:
	python3 scripts/validate-graph-exports.py

schema-duplicate-contracts-validate:
	python3 scripts/validate-schema-duplicate-contracts.py

relationship-predicate-review:
	@if [[ -z "$(strip $(TYPE))" || -z "$(strip $(LABEL))" || -z "$(strip $(DESCRIPTION))" || -z "$(strip $(CATEGORY))" ]]; then \
		printf 'TYPE, LABEL, DESCRIPTION and CATEGORY are required.\n' >&2; \
		exit 1; \
	fi
	python3 scripts/review-relationship-predicate-reuse.py \
		--candidate-type "$(TYPE)" --candidate-label "$(LABEL)" \
		--candidate-description "$(DESCRIPTION)" --candidate-category "$(CATEGORY)"

rule-coverage-validate:
	python3 scripts/validate-rule-coverage.py

markdown-json-validate:
	python3 scripts/validate-markdown-json.py "$(or $(DOCS_PATH),docs)"

validation-inventory-validate:
	python3 scripts/validate-validation-inventory.py

agent-routing-validate:
	python3 scripts/validate-agent-routing.py

release-check:
	python3 scripts/rkm-release-check.py

route-task:
	@if [[ -z "$(strip $(PATHS))" ]]; then \
		printf 'PATHS is required. Usage: make route-task PATHS="schema/foo.schema.json data/rag-techniques/hybrid-retrieval.json"\n' >&2; \
		exit 1; \
	fi
	python3 scripts/rkm-route-task.py --paths "$(PATHS)"

rag-recommendation-adapter-test:
	python3 scripts/import-rag-recommendation-artifact.py --self-test

external-rag-evidence-review:
	@if [[ -z "$(strip $(RAG_ROOT))" ]]; then \
		printf 'RAG_ROOT is required. Usage: make external-rag-evidence-review RAG_ROOT=/path/to/BuildingRAGAgentsWithLLMs\n' >&2; \
		exit 1; \
	fi
	args=(--rag-root "$(RAG_ROOT)" --max-age-days "$(EVIDENCE_MAX_AGE_DAYS)"); \
	if [[ -n "$(strip $(EVIDENCE_AS_OF_DATE))" ]]; then args+=(--as-of-date "$(EVIDENCE_AS_OF_DATE)"); fi; \
	python3 scripts/verify-external-rag-evidence.py "$${args[@]}"

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

autocycle:
	RKM_PER_CYCLE_TIMEOUT_SECONDS="$(PER_CYCLE_TIMEOUT_SECONDS)" TOKEN_BUDGET="$(TOKEN_BUDGET)" BUDGET_SAFETY_FACTOR="$(BUDGET_SAFETY_FACTOR)" BUDGET_GRACE_TOKENS="$(BUDGET_GRACE_TOKENS)" BUDGET_GRACE_RATIO="$(BUDGET_GRACE_RATIO)" FORCE="$(FORCE)" bash scripts/rkm-autocycle.sh "$(AUTOCYCLE_N)"

discover:
	set +e; \
	bash scripts/rkm-discover.sh "$(DISCOVER_N)" > /tmp/rkm-discovery-output.txt; \
	exit_code="$$?"; \
	set -e; \
	printf 'rkm-discover exit code: %s\n' "$$exit_code"; \
	tail -n "$(TAIL_LINES)" /tmp/rkm-discovery-output.txt; \
	git status --short; \
	exit "$$exit_code"

push: safe-push

safe-push: validate
	@if [[ -n "$$(git status --porcelain)" ]]; then \
		git status --short; \
		printf 'Working tree must be clean before pushing.\n' >&2; \
		exit 1; \
	fi
	git log --oneline -n 5
	@printf 'Human-only publication: invoking the protected push wrapper.\n'
	/home/andreatarsi/bin/codex-safe-git-push-current

install-hooks:
	git config core.hooksPath .githooks
	@printf 'Git hooks path configured to .githooks.\n'

fix-eof:
	@if [[ -z "$(strip $(FILE))" ]]; then \
		printf 'FILE is required. Usage: make fix-eof FILE=path/to/file\n' >&2; \
		exit 1; \
	fi
	bash scripts/rkm-fix-eof.sh "$(FILE)"

codex-commit:
	@if [[ -z "$(strip $(PROMPT_FILE))" ]]; then \
		printf 'PROMPT_FILE is required. Usage: make codex-commit PROMPT_FILE=path/to/prompt FILE=path/to/file MESSAGE="commit message" OR FILES="path/a path/b"\n' >&2; \
		exit 1; \
	fi
	@if [[ -z "$(strip $(FILE))" && -z "$(strip $(FILES))" ]]; then \
		printf 'FILE or FILES is required. Usage: make codex-commit PROMPT_FILE=path/to/prompt FILE=path/to/file MESSAGE="commit message" OR FILES="path/a path/b"\n' >&2; \
		exit 1; \
	fi
	@if [[ -z "$(strip $(MESSAGE))" ]]; then \
		printf 'MESSAGE is required. Usage: make codex-commit PROMPT_FILE=path/to/prompt FILE=path/to/file MESSAGE="commit message" OR FILES="path/a path/b"\n' >&2; \
		exit 1; \
	fi
	@if [[ -n "$(strip $(FILES))" ]]; then \
		bash scripts/rkm-codex-commit.sh --prompt-file "$(PROMPT_FILE)" --files "$(FILES)" --message "$(MESSAGE)"; \
	else \
		bash scripts/rkm-codex-commit.sh --prompt-file "$(PROMPT_FILE)" --file "$(FILE)" --message "$(MESSAGE)"; \
	fi

recover-revise:
	bash scripts/rkm-recover-revise.sh

recovery-plan:
	python3 scripts/rkm-recovery-plan.py

clean-discovery-artifacts:
	find . -maxdepth 1 \( \
		-type d \( -name 'rkm-discovery-report-*' -o -name 'rkm-discovery-*' \) \
		-o -type f \( -name 'rkm-discovery-report-*.zip' -o -name 'rkm-discovery-*.zip' \) \
	\) -exec rm -rf -- {} +

usage-report:
	python3 scripts/rkm-run-ledger.py report

budget-init:
	python3 scripts/rkm-budget.py init --daily-budget "$(DAILY_BUDGET)" --safety-factor "$(BUDGET_SAFETY_FACTOR)" --reserve-ratio "$(BUDGET_RESERVE_RATIO)" --window-hours "$(BUDGET_WINDOW_HOURS)"

budget-report:
	python3 scripts/rkm-budget.py report

budget-check:
	python3 scripts/rkm-budget.py check --target "$(BUDGET_TARGET)"

budget-reset-window:
	python3 scripts/rkm-budget.py reset-window

next-action:
	python3 scripts/rkm-next-action.py --target "$(NEXT_ACTION_TARGET)" --force="$(FORCE)" --working-target-max "$(WORKING_TARGET_MAX)"

autopilot:
	RKM_PER_CYCLE_TIMEOUT_SECONDS="$(PER_CYCLE_TIMEOUT_SECONDS)" python3 scripts/rkm-autopilot.py --target "$(AUTOPILOT_TARGET)" --force="$(FORCE)" --working-target-max "$(WORKING_TARGET_MAX)"

autopilot-dry-run:
	RKM_PER_CYCLE_TIMEOUT_SECONDS="$(PER_CYCLE_TIMEOUT_SECONDS)" python3 scripts/rkm-autopilot.py --target "$(AUTOPILOT_TARGET)" --force="$(FORCE)" --working-target-max "$(WORKING_TARGET_MAX)" --dry-run

autopilot-recover:
	RKM_PER_CYCLE_TIMEOUT_SECONDS="$(PER_CYCLE_TIMEOUT_SECONDS)" python3 scripts/rkm-autopilot.py --target "$(AUTOPILOT_TARGET)" --force="$(FORCE)" --working-target-max "$(WORKING_TARGET_MAX)" --allow-recovery

autopilot-status:
	python3 scripts/rkm-autopilot.py status

cockpit:
	$(MAKE) status
	@printf '\n== Budget report ==\n'
	$(MAKE) budget-report || true
	@printf '\n== Recovery plan ==\n'
	$(MAKE) recovery-plan || true
	@printf '\n== Next action ==\n'
	$(MAKE) next-action || true
	@printf '\n== Autopilot status ==\n'
	$(MAKE) autopilot-status || true

cockpit-summary: N ?= 3
cockpit-summary:
	python3 scripts/rkm-cockpit-summary.py --target "$(N)" --force="$(FORCE)" --working-target-max "$(WORKING_TARGET_MAX)" --budget-grace-tokens "$(BUDGET_GRACE_TOKENS)" --budget-grace-ratio "$(BUDGET_GRACE_RATIO)"

help:
	@printf 'RKM developer commands:\n'
	@printf '  make validate                    Run bash scripts/validate-rkm.sh.\n'
	@printf '  make data-validate               Validate data instances declared in data/manifest.json.\n'
	@printf '  make graph-export                Generate minimal graph export files from fixtures.\n'
	@printf '  make data-graph-export           Generate graph export files from validated seed data.\n'
	@printf '  make graph-export-validate       Validate graph export node and edge files against schemas.\n'
	@printf '  make schema-duplicate-contracts-validate  Validate same-name first-class schema and definition composition.\n'
	@printf '  make relationship-predicate-review TYPE=... LABEL=... DESCRIPTION=... CATEGORY=...  Review a proposed predicate against the registry.\n'
	@printf '  make rule-coverage-validate             Validate governance coverage rows against repository checks.\n'
	@printf '  make markdown-json-validate DOCS_PATH=docs    Validate JSON fenced examples in selected Markdown files.\n'
	@printf '  make agent-routing-validate      Validate distributed agent rule routing files and task guides.\n'
	@printf '  make release-check               Run the strict pre-tag readiness check for v0.1.0-alpha.\n'
	@printf '  make route-task PATHS="schema/foo.schema.json data/rag-techniques/hybrid-retrieval.json"  Show required readings, task guides, risk notes, and checks for intended paths.\n'
	@printf '  make rag-recommendation-adapter-test  Run the RAG Lab recommendation artifact adapter self-test.\n'
	@printf '  make external-rag-evidence-review RAG_ROOT=...  Verify external RAG evidence hashes and source commit without promotion.\n'
	@printf '  make runtime-artifacts-validate      Reject repository-local runtime logs, scratch files, and run artifacts.\n'
	@printf '  make entity-type-package-validate    Verify populated entity types have registry, schema, manifest, docs, and graph coverage.\n'
	@printf '  make status                      Show git status --short.\n'
	@printf '  make log                         Show the 10 most recent commits.\n'
	@printf '  make cycle [N=3]                 Run scripts/rkm-cycle.sh N, save stdout to /tmp/rkm-cycle-output.txt, print exit code, output tail, and status.\n'
	@printf '  make autocycle [N=3]             Run bash scripts/rkm-autocycle.sh N.\n'
	@printf '                                   Examples: make autocycle N=5; make autocycle N=1 PER_CYCLE_TIMEOUT_SECONDS=1800.\n'
	@printf '  make discover [N=5]              Run scripts/rkm-discover.sh N, save stdout to /tmp/rkm-discovery-output.txt, keep stderr visible, print exit code, output tail, and status.\n'
	@printf '  make push                        Human-only alias for make safe-push.\n'
	@printf '  make safe-push                   Validate, require clean status, then invoke the protected human-only push wrapper.\n'
	@printf '  make install-hooks               Configure Git to use hooks from .githooks.\n'
	@printf '  make fix-eof FILE=path/to/file   Run scripts/rkm-fix-eof.sh on FILE.\n'
	@printf '  make codex-commit PROMPT_FILE=path/to/prompt FILE=path/to/file MESSAGE="commit message"  Run scripts/rkm-codex-commit.sh for one file.\n'
	@printf '  make codex-commit PROMPT_FILE=path/to/prompt FILES="path/a path/b" MESSAGE="commit message"  Run scripts/rkm-codex-commit.sh for multiple files.\n'
	@printf '  make recover-revise              Run bash scripts/rkm-recover-revise.sh.\n'
	@printf '  make recovery-plan               Inspect the current repository and recent logs to recommend recovery without modifying files.\n'
	@printf '  make clean-discovery-artifacts   Remove root-level rkm-discovery-report-* and rkm-discovery-* directories or zip files.\n'
	@printf '  make usage-report                Run python3 scripts/rkm-run-ledger.py report.\n'
	@printf '  make budget-init                 Initialize the local budget profile using DAILY_BUDGET, BUDGET_SAFETY_FACTOR, BUDGET_RESERVE_RATIO, and BUDGET_WINDOW_HOURS.\n'
	@printf '  make budget-report               Show the local budget profile report.\n'
	@printf '  make budget-check [N=3]          Check whether the local budget profile allows BUDGET_TARGET, defaulting to AUTOCYCLE_N.\n'
	@printf '  make budget-reset-window         Reset the local budget accounting window while preserving the existing budget profile.\n'
	@printf '  make next-action [N=3]           Print the next safe operational action without modifying files.\n'
	@printf '  make autopilot [N=3]             Run python3 scripts/rkm-autopilot.py using AUTOPILOT_TARGET, defaulting to AUTOCYCLE_N.\n'
	@printf '                                   Examples: make autopilot N=5; make autopilot N=1 PER_CYCLE_TIMEOUT_SECONDS=1800; make autopilot N=24 FORCE=true.\n'
	@printf '  make autopilot-dry-run [N=3]     Run python3 scripts/rkm-autopilot.py using AUTOPILOT_TARGET with --dry-run.\n'
	@printf '  make autopilot-recover [N=3]     Run python3 scripts/rkm-autopilot.py using AUTOPILOT_TARGET with --allow-recovery.\n'
	@printf '  make autopilot-status            Show the last autopilot decision from .rkm/autopilot-state.json.\n'
	@printf '  make cockpit                     Show status, budget, recovery, next action, and autopilot status without modifying files.\n'
	@printf '  make cockpit-summary [N=]        Show a compact colored decision dashboard.\n'
	@printf '                                   Examples: make cockpit-summary N=24; make cockpit-summary N=24 FORCE=true.\n'
	@printf '  make help                        Show this help.\n'
