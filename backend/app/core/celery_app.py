from celery import Celery

from app.core.config import get_settings

settings = get_settings()
celery_app = Celery("enterprise_operations", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    imports=("app.workers.workflow_tasks",),
    beat_schedule={
        "scan-workflow-sla-every-five-minutes": {
            "task": "workflow.scan_sla_breaches",
            "schedule": 300.0,
        }
    },
)
