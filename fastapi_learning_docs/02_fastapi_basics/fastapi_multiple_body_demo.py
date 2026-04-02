"""
多个 Body 模型、embed=True、Body 标量 — 对应 08_request_body_multiple_embed.md。

运行：
  uvicorn fastapi_multiple_body_demo:app --reload --app-dir fastapi_learning_docs/02_fastapi_basics

文档：http://127.0.0.1:8000/docs
"""

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI(title="Multiple Body / embed / Body scalar demo")


class Item(BaseModel):
    name: str
    price: float


class User(BaseModel):
    username: str


# --- 1) 两个模型：根 JSON 为 {"item": {...}, "user": {...}} ---
@app.post("/multi")
async def two_models(item: Item, user: User):
    return {"item": item.model_dump(), "user": user.model_dump()}


# --- 2) 单模型外包一层 key：{"item": {"name","price"}} ---
@app.post("/embed")
async def embedded(item: Item = Body(..., embed=True)):
    return item.model_dump()


# --- 3) 两个模型 + 根上的一个 int：importance 必须用 Body(...) ---
@app.post("/with-importance")
async def with_scalar(
    item: Item,
    user: User,
    importance: int = Body(...),
):
    return {
        "item": item.model_dump(),
        "user": user.model_dump(),
        "importance": importance,
    }


@app.get("/")
def root():
    return {
        "docs": "/docs",
        "examples": {
            "POST /multi": {
                "item": {"name": "A", "price": 9.9},
                "user": {"username": "alice"},
            },
            "POST /embed": {"item": {"name": "B", "price": 1.0}},
            "POST /with-importance": {
                "item": {"name": "C", "price": 2.0},
                "user": {"username": "bob"},
                "importance": 5,
            },
        },
    }
