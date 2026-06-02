# PostgreSQL Schema Design

## 1. Database Conventions

PostgreSQL is the transactional source of truth. SQLAlchemy models and Alembic
migrations will implement this design.

### Shared conventions

- Primary keys are UUIDs generated application-side.
- Timestamps are timezone-aware UTC values: `created_at`, `updated_at`.
- Mutable business tables use nullable `deleted_at` for soft deletion.
- Tables with concurrent edits use integer `version` for optimistic locking.
- Enumerations are persisted as stable lowercase strings so deployments can
  extend values safely.
- Monetary values use `numeric(14, 2)` plus an ISO 4217 `currency_code`.
- Human-readable references such as `AUD-2026-000001` are unique and indexed.
- JSONB is reserved for variable configuration, snapshots, and event payloads;
  searchable business fields remain relational columns.

Soft-deleted rows are excluded by repository defaults. Immutable tables such
as activity logs and outbox events are never soft-deleted.

## 2. Identity And Organization

### `users`

| Column | Type | Notes |
| --- | --- | --- |
| `id` | uuid PK | |
| `email` | varchar(320) | Case-insensitive unique index |
| `password_hash` | varchar(255) | Never returned by APIs |
| `first_name`, `last_name` | varchar(100) | |
| `employee_number` | varchar(50) | Unique internal identifier |
| `job_title` | varchar(150) | |
| `manager_id` | uuid FK users | Nullable reporting line |
| `is_active` | boolean | Login eligibility |
| `last_login_at` | timestamptz | Nullable |
| shared timestamps | | Includes `deleted_at` |

### `departments`

| Column | Type | Notes |
| --- | --- | --- |
| `id` | uuid PK | |
| `code` | varchar(30) | Unique, stable department code |
| `name` | varchar(150) | |
| `parent_id` | uuid FK departments | Nullable hierarchy |
| `manager_id` | uuid FK users | Nullable |
| shared timestamps | | Includes `deleted_at` |

### `department_memberships`

| Column | Type | Notes |
| --- | --- | --- |
| `id` | uuid PK | |
| `user_id` | uuid FK users | |
| `department_id` | uuid FK departments | |
| `is_primary` | boolean | Exactly one active primary membership per user |
| shared timestamps | | Includes `deleted_at` |

### `roles`, `permissions`, `user_roles`, `role_permissions`

- `roles`: `id`, unique `code`, `name`, `description`, timestamps.
- `permissions`: `id`, unique `code`, `description`, timestamps.
- `user_roles`: user-role association with optional `department_id` scope.
- `role_permissions`: role-permission association.

Permission codes use `<module>:<resource>:<action>`, for example
`audit:audit:create`, `workflow:task:approve`, and `analytics:kpi:view`.

### `auth_sessions`, `refresh_tokens`

- `auth_sessions`: session owner, device metadata, IP address, last activity,
  expiry, and revocation timestamp.
- `refresh_tokens`: session, token hash, token family UUID, expiry,
  `consumed_at`, `revoked_at`, and optional `replaced_by_token_id`.

Refresh token reuse revokes the entire token family.

## 3. Audit And Compliance

### `audits`

| Column | Type | Notes |
| --- | --- | --- |
| `id` | uuid PK | |
| `reference` | varchar(30) | Unique display ID |
| `title` | varchar(255) | |
| `description` | text | |
| `audit_type` | varchar(40) | Internal, external, regulatory, process |
| `status` | varchar(40) | Draft through closed or cancelled |
| `risk_level` | varchar(20) | Low, medium, high, critical |
| `risk_score` | numeric(5,2) | Validated range 0 to 100 |
| `department_id` | uuid FK departments | Audited department |
| `owner_id` | uuid FK users | Business owner |
| `lead_auditor_id` | uuid FK users | Nullable until assigned |
| `workflow_instance_id` | uuid FK workflow_instances | Nullable approval flow |
| `planned_start_at`, `planned_end_at` | timestamptz | |
| `actual_start_at`, `actual_end_at` | timestamptz | Nullable |
| `version` | integer | Optimistic lock |
| shared timestamps | | Includes `deleted_at` |

Audit lifecycle:

```text
draft -> planned -> in_progress -> under_review -> approved -> closed
   \          \             \             \            \
    ------------------------------------------------> cancelled
```

### Supporting audit tables

| Table | Purpose |
| --- | --- |
| `audit_assignments` | Multiple assigned auditors with assignment role |
| `controls` | Reusable compliance controls with owner and control category |
| `audit_controls` | Audit-specific control scope, test result, notes |
| `audit_findings` | Severity, remediation owner, due date, status |
| `finding_comments` | Discussion and mention-ready comment body |
| `evidence_items` | Evidence metadata linked to audit and optionally control |
| `compliance_frameworks` | Framework metadata such as ISO 27001 or internal policy |
| `framework_controls` | Many-to-many mapping between controls and frameworks |

Finding lifecycle:

```text
open -> remediation_in_progress -> ready_for_validation -> resolved
  \                                      \
   ------------------------------------> accepted_risk
```

## 4. Workflow Automation

Workflow definitions are versioned. Running instances always reference an
immutable published version so later edits cannot rewrite history.

### Definition tables

| Table | Purpose |
| --- | --- |
| `workflow_definitions` | Stable workflow identity, key, name, target type |
| `workflow_definition_versions` | Draft or published version and configuration |
| `workflow_steps` | Ordered approval, task, notification, or terminal steps |
| `workflow_step_transitions` | Allowed graph edges with optional conditions |

`workflow_steps.config` and transition `condition` use JSONB for controlled,
validated configuration such as approver resolution strategy, SLA duration,
and escalation path.

### Runtime tables

| Table | Purpose |
| --- | --- |
| `workflow_instances` | One execution for a target entity |
| `workflow_tasks` | Actionable human task with assignee, SLA, and status |
| `workflow_task_actions` | Immutable approve, reject, delegate, and comment actions |
| `workflow_activity_logs` | Immutable state changes and automated actions |
| `workflow_escalations` | Escalation attempts and resolution state |

Runtime records include a `target_type` and `target_id` reference because a
workflow can govern audits, leave requests, expenses, or travel requests.
The service layer validates targets before starting a workflow.

## 5. Employee Operations

### Requests

| Table | Notable fields |
| --- | --- |
| `leave_requests` | requester, leave type, start/end dates, reason, status, workflow instance |
| `expense_requests` | requester, purpose, amount, currency, expense date, status, workflow instance |
| `travel_requests` | requester, origin, destination, start/end dates, estimated amount, status, workflow instance |

Every request tracks its department at creation time. That snapshot preserves
historical reporting if the employee later moves departments.

### `employee_tasks`

Internal task assignments include title, description, assigner, assignee,
department, priority, status, due date, completion timestamp, and optional
links to an originating business entity.

### `expense_items`

Expense line items include category, description, amount, and transaction
date. Receipts are represented in `attachments`.

## 6. Collaboration And Platform

### `notifications`

Stores recipient, notification type, title, body, severity, target type,
target ID, read timestamp, and created timestamp. WebSocket delivery is
best-effort; this persisted row guarantees users can retrieve missed items.

### `mentions`

Stores the mentioned user, author, source type, source ID, and notification
link. Mention parsing occurs in the application layer.

### `attachments`

Stores file name, media type, byte size, object storage key, checksum,
uploader, target type, target ID, scan status, and timestamps. Upload and
download use short-lived signed object-storage URLs.

### `activity_logs`

Immutable application audit trail:

| Column | Type | Notes |
| --- | --- | --- |
| `id` | uuid PK | |
| `actor_id` | uuid FK users | Nullable for system actions |
| `action` | varchar(100) | Stable action code |
| `entity_type`, `entity_id` | varchar(80), uuid | Affected record |
| `before_data`, `after_data` | jsonb | Redacted snapshots where useful |
| `metadata` | jsonb | Request and domain context |
| `request_id`, `correlation_id` | uuid | Traceability |
| `created_at` | timestamptz | Immutable |

### `outbox_events`

Transactional event delivery table with aggregate metadata, event type,
JSONB payload, creation timestamp, processing timestamp, retry count, and
last error. Celery delivers unprocessed events idempotently.

## 7. Analytics

Analytics start as PostgreSQL read models refreshed asynchronously:

| Read model | Purpose |
| --- | --- |
| `mv_audit_status_summary` | Audit counts and completion rates by department and period |
| `mv_risk_heatmap` | Risk distribution by department and audit category |
| `mv_workflow_performance` | Cycle time, SLA compliance, and queue depth by workflow |
| `mv_operations_summary` | Request volumes, approval time, and rejection rates |

Materialized views are refreshed concurrently by Celery after relevant domain
events and on a scheduled fallback. Redis caches dashboard responses briefly.

## 8. Index Strategy

Indexes focus on authorization, user queues, lifecycle filters, and event
delivery.

```sql
CREATE UNIQUE INDEX uq_users_email_active
    ON users (lower(email)) WHERE deleted_at IS NULL;

CREATE UNIQUE INDEX uq_membership_primary_active
    ON department_memberships (user_id)
    WHERE is_primary = true AND deleted_at IS NULL;

CREATE INDEX ix_audits_department_status
    ON audits (department_id, status)
    WHERE deleted_at IS NULL;

CREATE INDEX ix_audits_lead_status
    ON audits (lead_auditor_id, status)
    WHERE deleted_at IS NULL;

CREATE INDEX ix_findings_owner_status_due
    ON audit_findings (remediation_owner_id, status, due_at)
    WHERE deleted_at IS NULL;

CREATE INDEX ix_workflow_tasks_assignee_status_due
    ON workflow_tasks (assignee_id, status, due_at)
    WHERE deleted_at IS NULL;

CREATE INDEX ix_notifications_recipient_unread
    ON notifications (recipient_id, created_at DESC)
    WHERE read_at IS NULL;

CREATE INDEX ix_activity_entity_created
    ON activity_logs (entity_type, entity_id, created_at DESC);

CREATE INDEX ix_outbox_unprocessed
    ON outbox_events (created_at)
    WHERE processed_at IS NULL;
```

Indexes will be reviewed against production-like query plans. Indexing every
column would slow writes and increase storage without improving real access
patterns.

## 9. Migration Strategy

Alembic migrations are the only supported schema-change mechanism.

1. Keep each migration focused and reversible where practical.
2. Apply additive changes before deploying code that uses them.
3. Backfill large datasets in bounded background batches.
4. Enforce new constraints only after backfill validation.
5. Remove old columns in a later deployment after compatibility code is gone.
6. Use `CREATE INDEX CONCURRENTLY` for large production indexes.
7. Run migrations as a separate release job, never from every API replica.

## 10. Seed Strategy

Development seeds are deterministic and idempotent:

- five built-in roles and their permission sets;
- a department hierarchy such as Corporate, Finance, Operations, IT, and
  Compliance;
- demo users for each role;
- compliance frameworks and representative controls;
- workflow definitions for audit approval, leave approval, expense approval,
  and travel approval;
- realistic audit, finding, request, task, and notification examples.

Production receives only required reference data such as built-in roles and
permissions. Demo users and sample transactions are never loaded in
production.
