from __future__ import annotations

import os

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.openapi.utils import get_openapi

from backend.routers.v1 import router as router_v1
from backend.routers.v2 import router as router_v2
from backend.pydantic_models.common import (
    ValidationErrorResponse,
    UnexpectedErrorResponse,
)
from backend import get_logger, get_config


logger = get_logger(__name__)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
        servers=app.servers,
        contact=app.contact,
    )

    http_methods = ["post", "get", "put", "delete"]
    # look for the error 422 and removes it
    for method in openapi_schema["paths"]:
        for m in http_methods:
            try:
                del openapi_schema["paths"][method][m]["responses"]["422"]
            except KeyError:
                pass

    app.openapi_schema = openapi_schema
    return app.openapi_schema


def create_app() -> FastAPI:
    app = FastAPI(
        **get_config().dict(),
        responses={
            status.HTTP_400_BAD_REQUEST: {"model": ValidationErrorResponse},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": UnexpectedErrorResponse},
        },
    )

    app.openapi = custom_openapi

    app.include_router(router_v1)
    app.include_router(router_v2)

    @app.get("/")
    def docs_redirect():
        return RedirectResponse(url="/docs")

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        logger.exception(msg="Validation exception occurred while handling request")
        return JSONResponse(
            content=jsonable_encoder(
                {"error": " AND ".join(f"{error['msg']}" for error in exc.errors())}
            ),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.exception(msg="Unexpected exception occurred while handling request")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder({"error": str(exc)}),
        )

    return app


app = create_app()
