from fastapi import APIRouter

from backend.routers.v1.deposits import router as deposit_router

router = APIRouter(prefix="/v1", tags=["V1"])
router.include_router(deposit_router)
