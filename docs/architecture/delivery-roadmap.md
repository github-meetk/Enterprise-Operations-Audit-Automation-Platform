# Delivery Roadmap

Each phase ends with working code, tests appropriate to its risk, and a focused
commit. The sequence avoids building UI against unstable contracts.

## Phase 1: Architecture Baseline

- System architecture and bounded contexts
- Final monorepo folder structure
- PostgreSQL schema strategy and ER diagrams
- Backend runtime blueprint

Suggested commit:

```text
docs: establish enterprise platform architecture baseline
```

## Phase 2: Backend Foundation And Identity

- FastAPI project, settings, health endpoints, logging, middleware
- PostgreSQL, Redis, SQLAlchemy async sessions, Alembic
- Organization, users, sessions, token rotation, RBAC
- Seed data and backend tests

Suggested commits:

```text
build(backend): scaffold async FastAPI service and local dependencies
feat(identity): add JWT sessions refresh rotation and RBAC
test(identity): cover authentication and permission boundaries
```

## Phase 3: Angular Foundation

- Angular 19 workspace and Material theme
- Enterprise app shell, responsive sidebar, topbar, breadcrumbs
- Auth UI, guards, token interceptor, session store
- Feature lazy loading, shared UI primitives, NgRx baseline

Suggested commits:

```text
build(frontend): scaffold Angular enterprise application shell
feat(frontend-auth): add login session state and protected routing
```

## Phase 4: Audit And Compliance

- Audit lifecycle, assignments, controls, findings, evidence metadata
- Comments, activity timeline, risk calculation, approval integration
- Audit table, advanced filters, detail workspace, timeline UI

## Phase 5: Workflow Automation

- Versioned workflow definitions and runtime engine
- Approval tasks, routing, actions, SLA tracking, escalation jobs
- Workflow visualizer, task inbox, approval interaction UI

## Phase 6: Employee Operations

- Leave, expense, travel, internal task, directory, department APIs
- Reusable request approval flows
- Operations portal and manager approval views

## Phase 7: Analytics

- Projection refresh workers and KPI endpoints
- Dashboard cards, operational charts, risk heatmap, bottleneck analysis
- ApexCharts integration and role-aware dashboards

## Phase 8: Notifications And Realtime

- Transactional outbox processing
- Persisted notifications, mentions, unread state
- Redis fan-out, WebSocket endpoint, activity feed UI

## Phase 9: Delivery Platform

- Production Dockerfiles, Compose topology, Nginx config
- Environment templates and secrets conventions
- GitHub Actions for lint, test, migration checks, and container builds

## Phase 10: Hardening

- Broader frontend and backend tests
- Query-plan review, cache tuning, rate limits, security headers
- Dependency scans, production runbook, final architecture summary
