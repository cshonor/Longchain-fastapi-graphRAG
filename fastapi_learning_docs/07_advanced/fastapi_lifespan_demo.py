"""
应用生命周期 lifespan — 对应 04_lifespan_startup_shutdown.md

运行：
  uvicorn fastapi_lifespan_demo:app --reload --app-dir fastapi_learning_docs/07_advanced

启动时填充内存 items；停止服务时在 demo_lifespan.log 追加一行（Ctrl+C 触发 shutdown）。
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException

LOG_PATH = Path(__file__).resolve().parent / "demo_lifespan.log"

items: dict[str, dict] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    items.clear()
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}
    yield
    with LOG_PATH.open("a", encoding="utf-8") as log:
        log.write("Application shutdown\n")


app = FastAPI(title="Lifespan demo", lifespan=lifespan)


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Unknown item_id")
    return items[item_id]


@app.get("/")
async def root():
    return {"docs": "/docs", "items": list(items.keys()), "log": LOG_PATH.name}
