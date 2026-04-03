"""
自定义 HTTP 状态码 — 对应 16_response_status_code.md

思路参考：博客园《FastAPI 基础学习(十四) Response自定义状态码》（麦克煎蛋）

运行：
  uvicorn fastapi_response_status_demo:app --reload --app-dir fastapi_learning_docs/02_fastapi_basics

文档：http://127.0.0.1:8000/docs
"""

from fastapi import Body, FastAPI, Response, status
from fastapi.responses import JSONResponse

app = FastAPI(title="FastAPI response status_code demo")


# --- 1) 装饰器 status_code ---
@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}


# --- 2) Response 上改 status_code ---
tasks: dict[str, str] = {"foo": "Listen to the Bar Fighters"}


@app.put("/get-or-create-task/{task_id}", status_code=200)
def get_or_create_task(task_id: str, response: Response):
    if task_id not in tasks:
        tasks[task_id] = "This didn't exist before"
        response.status_code = status.HTTP_201_CREATED
    return tasks[task_id]


# --- 3) JSONResponse(status_code=...) ---
items: dict[str, dict] = {
    "foo": {"name": "Fighters", "size": 6},
    "bar": {"name": "Tenders", "size": 3},
}


@app.put("/items-body/{item_id}")
async def upsert_item(
    item_id: str,
    name: str | None = Body(None),
    size: int | None = Body(None),
):
    if item_id in items:
        item = items[item_id]
        if name is not None:
            item["name"] = name
        if size is not None:
            item["size"] = size
        return item
    item = {"name": name, "size": size}
    items[item_id] = item
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)


@app.get("/")
def root():
    return {
        "docs": "/docs",
        "routes": [
            "POST /items/",
            "PUT /get-or-create-task/{task_id}",
            "PUT /items-body/{item_id}",
        ],
    }
