from datetime import UTC, datetime

from app.core.celery_app import celery_app


@celery_app.task(name="workflow.scan_sla_breaches")
def scan_sla_breaches() -> dict[str, str]:
    # The worker boundary is established here. Phase 8 will persist escalations
    # and emit notification outbox events from an async service.
    return {"status": "scheduled", "checked_at": datetime.now(UTC).isoformat()}
