SHELL := /bin/bash
.PHONY: pdf test build up help be fe

pdf:
	cd backend && uv run python test_data/convert.py

# Usage: make test [be] [fe]  (no args = both)
test:
	@svc="$(filter-out test,$(MAKECMDGOALS))"; \
	if [ -z "$$svc" ]; then svc="be fe"; fi; \
	for s in $$svc; do \
	  case $$s in \
	    be) (cd backend && uv run pytest -v) || exit 1;; \
	    fe) (cd frontend && pnpm lint) || exit 1;; \
	    *) echo "unknown suite: $$s (use be|fe)"; exit 1;; \
	  esac; \
	done

# BE needs no build step, so this only builds the frontend.
build:
	cd frontend && pnpm build

# Usage: make up [be] [fe]  (no args = both)
up:
	@svc="$(filter-out up,$(MAKECMDGOALS))"; \
	if [ -z "$$svc" ]; then svc="be fe"; fi; \
	trap 'kill 0' INT TERM; \
	for s in $$svc; do \
	  case $$s in \
	    be) (cd backend && uv run fastapi dev main.py) & ;; \
	    fe) (cd frontend && pnpm dev) & ;; \
	    *) echo "unknown service: $$s (use be|fe)"; exit 1;; \
	  esac; \
	done; \
	wait

# Swallow service args so make doesn't treat them as targets.
be fe:
	@:

help:
	@echo "Targets: pdf test [be] [fe] build up [be] [fe]"
