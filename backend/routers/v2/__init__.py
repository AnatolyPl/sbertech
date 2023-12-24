from fastapi import APIRouter

from backend.routers.v2.deposits import router as deposit_router

router = APIRouter(prefix="/v2", tags=["V2"])
router.include_router(deposit_router)
