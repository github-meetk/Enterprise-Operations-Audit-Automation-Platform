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

Phase 1: architecture planning and relational data design.

Application code will be scaffolded in Phase 2 after the architecture baseline
is accepted.
