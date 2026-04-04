"""
Depends 入门：共享 common_parameters — 对应 01_di_introduction.md

运行：
  uvicorn fastapi_depends_intro_demo:app --reload --app-dir fastapi_learning_docs/04_dependency_injection

文档：http://127.0.0.1:8000/docs
"""

from fastapi import Depends, FastAPI

app = FastAPI(title="Depends intro demo")


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/")
def root():
    return {"docs": "/docs", "try": ["/items/?skip=1&limit=5&q=test", "/users/"]}
