"""
错误处理示例 — 对应 02_exception_handling.md

运行：
  uvicorn fastapi_exception_handling_demo:app --reload --app-dir fastapi_learning_docs/07_advanced

说明：本 demo 将 StarletteHTTPException 统一改为 PlainTextResponse，与默认 JSON 错误不同。
"""

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(title="Exception handling demo")

items = {"foo": "The Foo Wrestlers"}


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


class ProductCreate(BaseModel):
    name: str
    price: float


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something."},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.exception_handler(StarletteHTTPException)
async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}


@app.get("/items-verbose/{item_id}")
async def read_item_verbose(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "missing"},
        )
    return {"item": items[item_id]}


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


@app.post("/products", status_code=201)
async def create_product(body: ProductCreate):
    return {"ok": True, "product": body.model_dump()}


@app.get("/")
async def root():
    return {
        "docs": "/docs",
        "try": [
            "GET /items/bar (404 plain text)",
            "GET /unicorns/yolo (418 JSON)",
            "POST /products {} (422 JSON with custom shape)",
        ],
    }
