# FastAPI 后台任务 BackgroundTasks

在响应已返回给客户端之后，再执行不需要写进 HTTP 正文的收尾工作，使用 BackgroundTasks（Starlette：响应发送完毕后按添加顺序调度）。

与 [错误处理](./02_exception_handling.md) 对照：后台任务里的异常一般不会把已成功的响应改成 5xx，但会在服务端产生错误记录。

---

## 一、适用场景

发邮件、写日志、落盘等轻量操作。重计算与强可靠性请用 Celery、Dramatiq、消息队列等。

---

## 二、基础用法

```python
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def write_notification(email: str, message: str = "") -> None:
    with open("log.txt", "w", encoding="utf-8") as f:
        f.write(f"notification for {email}: {message}\n")


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        write_notification,
        email,
        message="some notification",
    )
    return {"message": "后台任务已添加"}
```

add_task(可调用对象, 位置参数..., 关键字参数...)。任务可以是 def 或 async def。

---

## 三、在 Depends 里添加任务

依赖函数里同样可以注入 BackgroundTasks，与路由里是同一队列。

```python
from fastapi import BackgroundTasks, Depends, FastAPI

app = FastAPI()


def write_log(message: str) -> None:
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(message)


def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        background_tasks.add_task(write_log, f"found query: {q}\n")
    return q


@app.post("/send-notification/{email}")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks,
    q: str | None = Depends(get_query),
):
    background_tasks.add_task(write_log, f"message to {email}\n")
    return {"message": "Message sent"}
```

---

## 四、注意点

1. 先响应、后任务。  
2. 任务内异常通常不改已返回状态码，应 try/except 并记录。  
3. 多 worker 时任务只在当前进程；进程重启任务即丢。  
4. 勿把长阻塞或必须持久保证的工作完全压在 BackgroundTasks 上。

---

## 可运行示例

[`fastapi_background_tasks_demo.py`](./fastapi_background_tasks_demo.py)（日志 `demo_background_tasks.log`，`DELETE /log` 可清空）。

---

整理自博客园麦克煎蛋等教程。
