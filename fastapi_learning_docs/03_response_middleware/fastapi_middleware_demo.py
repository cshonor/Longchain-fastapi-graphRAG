"""
自定义 HTTP 中间件（耗时头）— 对应 01_custom_http_middleware.md

运行（在项目根目录 longchain/）：
  uvicorn fastapi_middleware_demo:app --reload --app-dir fastapi_learning_docs/03_response_middleware

或：
  cd fastapi_learning_docs/03_response_middleware
  uvicorn fastapi_middleware_demo:app --reload

文档：http://127.0.0.1:8000/docs
"""

import time

from fastapi import FastAPI, Request

app = FastAPI(title="HTTP middleware demo")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    return response


@app.get("/ping")
def ping():
    return {"ok": True}


@app.get("/")
def root():
    return {"docs": "/docs", "ping": "/ping"}
