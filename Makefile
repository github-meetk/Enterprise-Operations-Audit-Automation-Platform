.PHONY: backend-lint backend-test frontend-check compose-check migrate seed

backend-lint:
	cd backend && .venv/bin/ruff check app scripts alembic

backend-test:
	cd backend && .venv/bin/pytest

frontend-check:
	cd frontend && npx tsc -p tsconfig.app.json --noEmit && npx ngc -p tsconfig.app.json

compose-check:
	docker compose -f compose.yml config --quiet

migrate:
	cd backend && .venv/bin/alembic -c alembic.ini upgrade head

seed:
	cd backend && .venv/bin/python scripts/seed.py
