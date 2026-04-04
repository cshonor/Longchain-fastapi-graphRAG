"""
request.state 在中间件与路由间传数据 — 对应 05_request_state.md

运行：
  uvicorn fastapi_request_state_demo:app --reload --app-dir fastapi_learning_docs/07_advanced

GET /user/info 需经过中间件（非 SKIP 路径）；/docs 与 / 在跳过列表中。
"""

import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="request.state demo")

SKIP_PATHS = {
    "/",
    "/login",
    "/register",
    "/docs",
    "/openapi.json",
    "/redoc",
    "/favicon.ico",
}


@app.middleware("http")
async def attach_user(request: Request, call_next):
    if request.url.path in SKIP_PATHS:
        return await call_next(request)

    # 模拟鉴权：生产环境在此解析 Header/Cookie，失败则 return JSONResponse(401, ...)
    request.state.user = {"id": 1, "name": "test_user"}
    request.state.request_id = str(time.time_ns())

    return await call_next(request)


@app.get("/user/info")
async def user_info(request: Request):
    user = getattr(request.state, "user", None)
    if user is None:
        return JSONResponse(
            status_code=401,
            content={"detail": "未设置 request.state.user（是否命中了 SKIP 路径？）"},
        )
    return {
        "user": user,
        "request_id": getattr(request.state, "request_id", None),
    }


@app.get("/")
async def root():
    return {
        "docs": "/docs",
        "try": "GET /user/info",
        "skip_paths": sorted(SKIP_PATHS),
    }
