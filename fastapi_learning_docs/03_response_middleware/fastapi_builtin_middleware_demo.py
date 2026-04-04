"""
内置中间件：TrustedHost + GZip（本地可跑）
对应 02_advanced_builtin_middleware.md

未启用 HTTPSRedirectMiddleware，避免本地 http://127.0.0.1 被强制改 https。

运行：
  uvicorn fastapi_builtin_middleware_demo:app --reload --app-dir fastapi_learning_docs/03_response_middleware

文档：http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI(title="Builtin middleware demo")

# 本地 + 常见测试 Host；生产改为真实域名列表
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "testserver"],
)
app.add_middleware(GZipMiddleware, minimum_size=100)


@app.get("/big")
def big_payload():
    return {"data": "x" * 2000}


@app.get("/")
def root():
    return {"docs": "/docs", "hint": "GET /big with Accept-Encoding: gzip"}
