from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_app.api.v1.router import api_router
from fastapi_app.core.config import settings
from fastapi_app.core.exceptions import register_exception_handlers
from fastapi_app.middleware.request_timing import RequestTimingMiddleware


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


def create_app() -> FastAPI:
    application = FastAPI(title=settings.app_name, lifespan=lifespan)
    register_exception_handlers(application)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(RequestTimingMiddleware)
    application.include_router(api_router, prefix="/api/v1")
    return application


app = create_app()
