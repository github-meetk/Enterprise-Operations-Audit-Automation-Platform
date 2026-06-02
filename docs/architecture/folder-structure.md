# Final Folder Structure

The repository is a monorepo. Backend, frontend, infrastructure, and project
documentation are versioned together so contract changes remain reviewable.

```text
enterprise-operations-platform/
├── .github/
│   └── workflows/
│       ├── backend-ci.yml
│       ├── frontend-ci.yml
│       └── container-build.yml
├── backend/
│   ├── alembic/
│   │   ├── versions/
│   │   └── env.py
│   ├── app/
│   │   ├── api/
│   │   │   ├── dependencies.py
│   │   │   ├── error_handlers.py
│   │   │   └── router.py
│   │   ├── core/
│   │   │   ├── cache.py
│   │   │   ├── celery_app.py
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── logging.py
│   │   │   ├── middleware.py
│   │   │   ├── pagination.py
│   │   │   └── security.py
│   │   ├── modules/
│   │   │   ├── identity/
│   │   │   ├── organization/
│   │   │   ├── audit/
│   │   │   ├── workflow/
│   │   │   ├── operations/
│   │   │   ├── notification/
│   │   │   └── analytics/
│   │   ├── platform/
│   │   │   ├── activity/
│   │   │   ├── files/
│   │   │   └── outbox/
│   │   ├── workers/
│   │   │   ├── analytics_tasks.py
│   │   │   ├── notification_tasks.py
│   │   │   ├── outbox_tasks.py
│   │   │   └── workflow_tasks.py
│   │   └── main.py
│   ├── scripts/
│   │   └── seed.py
│   ├── tests/
│   │   ├── api/
│   │   ├── integration/
│   │   ├── services/
│   │   └── conftest.py
│   ├── alembic.ini
│   ├── pyproject.toml
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── core/
│   │   │   │   ├── api/
│   │   │   │   ├── auth/
│   │   │   │   ├── guards/
│   │   │   │   ├── interceptors/
│   │   │   │   ├── layout/
│   │   │   │   └── realtime/
│   │   │   ├── features/
│   │   │   │   ├── analytics/
│   │   │   │   ├── audits/
│   │   │   │   ├── auth/
│   │   │   │   ├── notifications/
│   │   │   │   ├── operations/
│   │   │   │   ├── organization/
│   │   │   │   └── workflows/
│   │   │   ├── shared/
│   │   │   │   ├── components/
│   │   │   │   ├── directives/
│   │   │   │   ├── pipes/
│   │   │   │   └── models/
│   │   │   ├── store/
│   │   │   ├── app.config.ts
│   │   │   └── app.routes.ts
│   │   ├── environments/
│   │   ├── styles/
│   │   └── main.ts
│   ├── angular.json
│   ├── package.json
│   └── Dockerfile
├── infra/
│   ├── nginx/
│   │   └── nginx.conf
│   └── postgres/
│       └── init.sql
├── docs/
│   ├── architecture/
│   └── database/
├── .env.example
├── compose.yml
├── Makefile
└── README.md
```

## Backend Module Template

Each domain module follows one predictable structure:

```text
modules/<module>/
├── api/
│   ├── dependencies.py
│   └── routes.py
├── application/
│   ├── services.py
│   └── dto.py
├── domain/
│   ├── enums.py
│   ├── events.py
│   └── exceptions.py
├── infrastructure/
│   └── repository.py
├── models.py
└── schemas.py
```

Not every module needs every file on day one. The ownership rule matters more
than empty folders:

- `api` translates HTTP concerns into application calls;
- `application` coordinates use cases and transactions;
- `domain` contains business vocabulary, transitions, and events;
- `infrastructure` implements persistence and external adapters;
- `models.py` owns SQLAlchemy mappings;
- `schemas.py` owns request and response contracts.

## Frontend Feature Template

```text
features/<feature>/
├── components/
├── pages/
├── data-access/
├── models/
├── store/
└── <feature>.routes.ts
```

- Pages compose screens and route parameters.
- Components stay presentational where practical.
- Data-access services own HTTP calls and feature facades.
- NgRx state remains feature-scoped and is registered with lazy routes.
- Signals are used for local UI state and derived view models.
