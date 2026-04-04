# FastAPI 启动与关闭（生命周期）

在**开始对外接请求之前**做初始化（连库、预热缓存、加载配置），在**进程退出前**做清理（关连接、刷日志），使用 ASGI **lifespan**（推荐）或旧版 **`on_event`**。

（与 [BackgroundTasks](./03_background_tasks.md) 区分：lifespan 绑定**进程/应用**起停；BackgroundTasks 绑定**单次 HTTP 响应**之后。）

---

## 一、推荐写法：`lifespan`

使用 **`@asynccontextmanager`**，在 **`yield` 之前**跑启动逻辑，在 **`yield` 之后**跑关闭逻辑。创建 **`FastAPI(lifespan=...)`**。

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI

items: dict[str, dict] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}
    yield
    with open("log.txt", "a", encoding="utf-8") as log:
        log.write("Application shutdown\n")


app = FastAPI(lifespan=lifespan)


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    return items[item_id]
```

- **`yield` 前**：启动阶段（可 `await` 异步初始化）。  
- **`yield` 后**：关闭阶段（服务停止时执行）。  
- 需要多段逻辑时，在两侧**顺序编写**或拆成函数依次调用即可。

---

## 二、旧写法：`on_event`（已弃用）

仍可在老项目里见到，但 **FastAPI 已标记弃用**，新代码请用 **lifespan**。

```python
app = FastAPI()


@app.on_event("startup")
async def startup_event():
    ...


@app.on_event("shutdown")
def shutdown_event():
    ...
```

可注册**多个** `startup` / `shutdown`，按注册顺序执行；**全部 startup 跑完后**才开始接请求。

---

## 三、要点

1. **挂在主应用**：`lifespan` / `on_event` 写在**挂载到 ASGI 服务器的那一个 `FastAPI()`** 上；**子应用**（`mount`）若自带 `FastAPI`，可有**自己的** lifespan，与主应用分别执行。  
2. **启动/关闭函数**可以是 **`async def`** 或 **`def`**（同步会在线程池跑，视版本而定；异步初始化优先 `async def`）。  
3. **关闭阶段**应处理超时与异常，避免拖死 worker 退出（生产可配合进程管理器的 kill 超时）。

---

## 可运行示例

[`fastapi_lifespan_demo.py`](./fastapi_lifespan_demo.py)（内存 `items` + 关闭时追加 `demo_lifespan.log`）。

---

整理自社区教程（含「麦克煎蛋」等）并与当前 FastAPI 推荐写法对齐。
