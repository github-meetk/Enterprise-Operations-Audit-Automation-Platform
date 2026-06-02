# ER Diagram

The diagram is intentionally split by domain so it remains readable during
implementation and review.

## Identity And Organization

```mermaid
erDiagram
    USERS ||--o{ DEPARTMENT_MEMBERSHIPS : belongs_to
    DEPARTMENTS ||--o{ DEPARTMENT_MEMBERSHIPS : contains
    DEPARTMENTS ||--o{ DEPARTMENTS : parent_of
    USERS ||--o{ USER_ROLES : receives
    ROLES ||--o{ USER_ROLES : assigned
    ROLES ||--o{ ROLE_PERMISSIONS : grants
    PERMISSIONS ||--o{ ROLE_PERMISSIONS : included
    USERS ||--o{ AUTH_SESSIONS : authenticates
    AUTH_SESSIONS ||--o{ REFRESH_TOKENS : rotates

    USERS {
        uuid id PK
        string email UK
        string employee_number UK
        uuid manager_id FK
        boolean is_active
        timestamptz deleted_at
    }
    DEPARTMENTS {
        uuid id PK
        string code UK
        uuid parent_id FK
        uuid manager_id FK
    }
    USER_ROLES {
        uuid id PK
        uuid user_id FK
        uuid role_id FK
        uuid department_id FK
    }
    AUTH_SESSIONS {
        uuid id PK
        uuid user_id FK
        timestamptz expires_at
        timestamptz revoked_at
    }
    REFRESH_TOKENS {
        uuid id PK
        uuid session_id FK
        uuid token_family
        string token_hash
        timestamptz consumed_at
    }
```

## Audit And Compliance

```mermaid
erDiagram
    DEPARTMENTS ||--o{ AUDITS : scoped_to
    USERS ||--o{ AUDITS : owns
    AUDITS ||--o{ AUDIT_ASSIGNMENTS : staffed_by
    USERS ||--o{ AUDIT_ASSIGNMENTS : assigned
    AUDITS ||--o{ AUDIT_CONTROLS : tests
    CONTROLS ||--o{ AUDIT_CONTROLS : included
    AUDITS ||--o{ AUDIT_FINDINGS : produces
    AUDIT_CONTROLS ||--o{ AUDIT_FINDINGS : relates_to
    AUDIT_FINDINGS ||--o{ FINDING_COMMENTS : discussed_in
    AUDITS ||--o{ EVIDENCE_ITEMS : contains
    CONTROLS ||--o{ FRAMEWORK_CONTROLS : mapped
    COMPLIANCE_FRAMEWORKS ||--o{ FRAMEWORK_CONTROLS : defines

    AUDITS {
        uuid id PK
        string reference UK
        uuid department_id FK
        uuid owner_id FK
        uuid lead_auditor_id FK
        uuid workflow_instance_id FK
        string status
        decimal risk_score
        int version
    }
    AUDIT_FINDINGS {
        uuid id PK
        uuid audit_id FK
        uuid audit_control_id FK
        uuid remediation_owner_id FK
        string severity
        string status
        timestamptz due_at
    }
    CONTROLS {
        uuid id PK
        string code UK
        string title
        uuid owner_id FK
    }
```

## Workflow Engine

```mermaid
erDiagram
    WORKFLOW_DEFINITIONS ||--o{ WORKFLOW_DEFINITION_VERSIONS : versions
    WORKFLOW_DEFINITION_VERSIONS ||--o{ WORKFLOW_STEPS : contains
    WORKFLOW_STEPS ||--o{ WORKFLOW_STEP_TRANSITIONS : starts
    WORKFLOW_STEPS ||--o{ WORKFLOW_STEP_TRANSITIONS : ends
    WORKFLOW_DEFINITION_VERSIONS ||--o{ WORKFLOW_INSTANCES : executes
    WORKFLOW_INSTANCES ||--o{ WORKFLOW_TASKS : creates
    WORKFLOW_TASKS ||--o{ WORKFLOW_TASK_ACTIONS : records
    WORKFLOW_INSTANCES ||--o{ WORKFLOW_ACTIVITY_LOGS : traces
    WORKFLOW_TASKS ||--o{ WORKFLOW_ESCALATIONS : escalates

    WORKFLOW_DEFINITIONS {
        uuid id PK
        string key UK
        string target_type
    }
    WORKFLOW_DEFINITION_VERSIONS {
        uuid id PK
        uuid definition_id FK
        int version
        string status
    }
    WORKFLOW_INSTANCES {
        uuid id PK
        uuid definition_version_id FK
        string target_type
        uuid target_id
        string status
    }
    WORKFLOW_TASKS {
        uuid id PK
        uuid instance_id FK
        uuid step_id FK
        uuid assignee_id FK
        string status
        timestamptz due_at
    }
```

## Operations And Collaboration

```mermaid
erDiagram
    USERS ||--o{ LEAVE_REQUESTS : submits
    USERS ||--o{ EXPENSE_REQUESTS : submits
    USERS ||--o{ TRAVEL_REQUESTS : submits
    EXPENSE_REQUESTS ||--o{ EXPENSE_ITEMS : itemizes
    USERS ||--o{ EMPLOYEE_TASKS : assigned
    USERS ||--o{ NOTIFICATIONS : receives
    USERS ||--o{ MENTIONS : mentioned
    USERS ||--o{ ATTACHMENTS : uploads

    LEAVE_REQUESTS {
        uuid id PK
        uuid requester_id FK
        uuid department_id FK
        uuid workflow_instance_id FK
        string status
    }
    EXPENSE_REQUESTS {
        uuid id PK
        uuid requester_id FK
        uuid department_id FK
        uuid workflow_instance_id FK
        decimal total_amount
        string currency_code
        string status
    }
    TRAVEL_REQUESTS {
        uuid id PK
        uuid requester_id FK
        uuid department_id FK
        uuid workflow_instance_id FK
        string status
    }
    NOTIFICATIONS {
        uuid id PK
        uuid recipient_id FK
        string target_type
        uuid target_id
        timestamptz read_at
    }
    ATTACHMENTS {
        uuid id PK
        uuid uploaded_by_id FK
        string target_type
        uuid target_id
        string object_key UK
    }
```

## Polymorphic References

`workflow_instances`, `notifications`, `mentions`, `attachments`, and
`activity_logs` use a controlled `target_type` plus `target_id` pair. A normal
foreign key cannot enforce these polymorphic relationships. Application
services validate target existence and authorization, and integration tests
cover each supported target type.
