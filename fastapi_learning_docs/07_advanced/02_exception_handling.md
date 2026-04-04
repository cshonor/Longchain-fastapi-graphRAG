# FastAPI 错误处理

在路由里用 **`HTTPException`** 返回标准错误；用 **`@app.exception_handler(异常类型)`** 统一处理自定义异常或改写框架默认行为（校验失败、底层 HTTP 错误等）。

（与 [自定义 HTTP 中间件](../03_response_middleware/01_custom_http_middleware.md) 区分：中间件包一整条请求；异常处理器在**已匹配路由或校验阶段**出错时介入。）

---

## 一、HTTPException（最常用）

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()
items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
```

- **`detail`**：可以是 **`str`**、**`dict`**、**`list`**，会进入响应体。  
- 常见状态码：**400**、**401**、**403**、**404**、**422**（校验失败，默认也由框架处理）。

---

## 二、带响应头

```python
raise HTTPException(
    status_code=404,
    detail="Item not found",
    headers={"X-Error": "There goes my error"},
)
```

---

## 三、自定义异常 + 处理器

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


app = FastAPI()


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something."},
    )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}
```

处理器签名为 **`(request: Request, exc: 异常类型)`**，返回 **`Response`** 子类即可。

---

## 四、改写默认行为

### 1. RequestValidationError（422）

```python
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )
```

**`exc.body`** 在部分请求下可能为 **`None`**，前端字段名以当前 Starlette/FastAPI 版本为准。

### 2. 统一把 HTTP 错误改成纯文本

注册 **`starlette.exceptions.HTTPException`**（见下文「必记」），可把默认 JSON 错误改成 **`PlainTextResponse`**：

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc: StarletteHTTPException):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
```

**注意**：一旦全局注册，所有 **`HTTPException`**（含 FastAPI 抛出的）都会走该处理器；`detail` 为 **dict** 时 **`str(...)`** 可读性一般，生产环境多保留 JSON。

---

## 五、在默认行为上「加日志」

先 **`import` 框架自带处理器**，再在自定义处理器里打日志后 **`await`** 交给默认实现：

```python
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"HTTP错误: {exc}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"参数错误: {exc}")
    return await request_validation_exception_handler(request, exc)
```

---

## 六、必记：抛错用 FastAPI，全局捕获用 Starlette 名

| 场景 | 导入 |
|------|------|
| 在业务代码里 **`raise`** | **`from fastapi import HTTPException`**（可带 **`headers`**） |
| **`@app.exception_handler(...)` 捕获所有 HTTP 类错误 | **`from starlette.exceptions import HTTPException as StarletteHTTPException`** |

FastAPI 的 **`HTTPException`** 继承自 Starlette；注册处理器时绑 **父类** 才能一并接住 FastAPI 抛出的子类。

---

## 可运行示例

[`fastapi_exception_handling_demo.py`](./fastapi_exception_handling_demo.py)（含 418 自定义异常、422 自定义体、HTTP 错误纯文本示例）。

---

内容整理自博客园「麦克煎蛋」等 FastAPI 错误处理教程。
