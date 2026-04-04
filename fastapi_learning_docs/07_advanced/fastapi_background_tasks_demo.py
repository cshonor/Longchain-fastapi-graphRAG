"""
BackgroundTasks — 对应 03_background_tasks.md

运行：
  uvicorn fastapi_background_tasks_demo:app --reload --app-dir fastapi_learning_docs/07_advanced

会在本文件同目录写入 demo_background_tasks.log（多次请求为追加）。
"""

from pathlib import Path

from fastapi import BackgroundTasks, Depends, FastAPI

app = FastAPI(title="BackgroundTasks demo")

LOG_PATH = Path(__file__).resolve().parent / "demo_background_tasks.log"


def write_notification(email: str, message: str = "") -> None:
    line = f"notification for {email}: {message}\n"
    LOG_PATH.write_text(line, encoding="utf-8")


def write_log(message: str) -> None:
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(message)


def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        background_tasks.add_task(write_log, f"found query: {q}\n")
    return q


@app.post("/send-notification/{email}")
async def send_notification_simple(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        write_notification,
        email,
        message="some notification",
    )
    return {"message": "后台任务已添加", "log": str(LOG_PATH.name)}


@app.post("/notify-with-query/{email}")
async def send_notification_with_dep(
    email: str,
    background_tasks: BackgroundTasks,
    q: str | None = Depends(get_query),
):
    background_tasks.add_task(write_log, f"message to {email}\n")
    return {"message": "Message sent", "q": q, "log": str(LOG_PATH.name)}


@app.delete("/log")
async def clear_log():
    if LOG_PATH.exists():
        LOG_PATH.unlink()
    return {"cleared": True}


@app.get("/")
async def root():
    return {
        "docs": "/docs",
        "post": [
            "POST /send-notification/you@example.com",
            "POST /notify-with-query/you@example.com?q=hello",
        ],
        "log_file": LOG_PATH.name,
        "clear": "DELETE /log",
    }
