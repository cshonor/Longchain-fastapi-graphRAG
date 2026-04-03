"""
Header 读取与返回 — 对应 15_header_operations.md

思路参考：博客园《FastAPI 基础学习(十三) Header操作》（麦克煎蛋）

运行：
  uvicorn fastapi_header_demo:app --reload --app-dir fastapi_learning_docs/02_fastapi_basics

文档：http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, Header, Response
from fastapi.responses import JSONResponse

app = FastAPI(title="FastAPI Header demo")


@app.get("/items/")
async def read_items(*, user_agent: str | None = Header(default=None)):
    return {"user_agent": user_agent}


@app.get("/items-no-convert/")
async def read_items_no_convert(
    *,
    user_agent: str | None = Header(default=None, convert_underscores=False),
):
    return {"user_agent": user_agent}


@app.get("/tokens/")
async def read_tokens(*, x_token: list[str] | None = Header(default=None)):
    return {"X-Token values": x_token}


@app.get("/headers-and-object/")
def headers_and_object(response: Response):
    response.headers["X-Cat-Dog"] = "alone in the world"
    return {"message": "Hello World"}


@app.get("/headers-json/")
def headers_json():
    content = {"message": "Hello World"}
    headers = {"X-Cat-Dog": "alone in the world", "Content-Language": "en-US"}
    return JSONResponse(content=content, headers=headers)


@app.get("/")
def root():
    return {
        "docs": "/docs",
        "try": [
            "GET /items/  （浏览器会自动带 User-Agent）",
            "GET /tokens/  （可多次发送 X-Token，具体见客户端）",
            "GET /headers-and-object/",
            "GET /headers-json/",
        ],
    }
