# Enterprise Operations & Audit Automation Platform

An internal enterprise platform for audit governance, approval automation,
employee operations, KPI monitoring, and real-time collaboration.

This repository is being built incrementally. Phase 1 establishes the system
architecture and database design before application scaffolding begins.

## Technology Stack

- Frontend: Angular 19, Angular Material, RxJS, NgRx, Angular Signals,
  Reactive Forms, ApexCharts
- Backend: FastAPI, SQLAlchemy, PostgreSQL, Redis, Celery
- Realtime: WebSockets
- Platform: Docker, Docker Compose, GitHub Actions
- Security: JWT authentication, refresh-token rotation, RBAC, department scope

## Architecture Documents

- [System architecture](docs/architecture/system-architecture.md)
- [Final folder structure](docs/architecture/folder-structure.md)
- [Backend blueprint](docs/architecture/backend-blueprint.md)
- [Database design](docs/database/schema-design.md)
- [ER diagram](docs/database/er-diagram.md)
- [Delivery roadmap](docs/architecture/delivery-roadmap.md)

## Current Status

Implemented through Phase 7:

- FastAPI backend foundation, logging, errors, settings, and health endpoint
- PostgreSQL schema models, Alembic baseline, and deterministic seed script
- JWT login, rotating refresh tokens, sessions, RBAC permission checks
- Audit lifecycle APIs
- Workflow task inbox and approval actions
- Employee leave and expense request APIs
- Analytics dashboard API
- Angular 19 enterprise shell, login, audit portfolio, approval inbox,
  operations portal, and dashboard views
- Docker Compose configuration for PostgreSQL, Redis, API, worker, and frontend

## Local Commands

```bash
python3 -m venv backend/.venv
backend/.venv/bin/pip install -e "backend[dev]"
npm install --prefix frontend

make backend-lint
make backend-test
make frontend-check
make compose-check
```

When Docker Desktop is running:

```bash
docker compose up -d postgres redis
make migrate
make seed
```

Demo admin credentials seeded for local development:

```text
admin@example.com
ChangeMe123!
```
