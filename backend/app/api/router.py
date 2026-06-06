from fastapi import APIRouter

from app.modules.analytics.routes import router as analytics_router
from app.modules.audit.routes import router as audit_router
from app.modules.identity.routes import router as identity_router
from app.modules.operations.routes import router as operations_router
from app.modules.workflow.routes import router as workflow_router

api_router = APIRouter()


@api_router.get("/health", tags=["platform"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


api_router.include_router(identity_router)
api_router.include_router(audit_router)
api_router.include_router(workflow_router)
api_router.include_router(operations_router)
api_router.include_router(analytics_router)
