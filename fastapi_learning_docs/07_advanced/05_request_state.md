# `request.state`：请求内附加数据

在一次 HTTP 请求中，把中间件或前置逻辑的结果（当前用户、request id 等）挂在 **`request.state`** 上，路由与 **`Depends`** 里通过 **`Request`** 读取，避免重复解析 Token 或查库。

（与 [自定义 HTTP 中间件](../03_response_middleware/01_custom_http_middleware.md) 搭配：中间件写 `state`，下游读 `state`。）

---

## 作用

- 中间件里统一鉴权 → **`request.state.user`**。  
- 路由里直接 **`request.state.user`**，**不跨请求**、不占全局。  
- 鉴权失败可在中间件 **`return JSONResponse(status_code=401, ...)`**，不必进路由。

---

## 标准写法

```python
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

SKIP_PATHS = {"/", "/login", "/register", "/docs", "/openapi.json", "/redoc"}


@app.middleware("http")
async def attach_user(request: Request, call_next):
    if request.url.path in SKIP_PATHS:
        return await call_next(request)

    request.state.user = {"id": 1, "name": "test_user"}
    request.state.request_id = str(time.time_ns())
    return await call_next(request)


@app.get("/user/info")
async def user_info(request: Request):
    return {"user": request.state.user}
```

未走赋值逻辑的路径（如被 SKIP）**不要**假定 `state.user` 一定存在，可用 **`getattr(request.state, "user", None)`** 或在依赖里校验。

---

## 与 `request.session` 的区别

- **`request.state`**：普通挂属性，**不依赖**额外中间件。  
- **`request.session`**：需 **`SessionMiddleware`**，一般是 **Cookie 会话**；与 `state` 是两种机制，不是互相替代。

---

## 要点

1. **生命周期**：仅**当前请求**。  
2. **文档**：OpenAPI **不会**描述 `state` 字段。  
3. **字段名**：`State` 无静态字段列表，写错属性在运行期才暴露，重要数据建议集中封装或依赖注入。

---

## 可运行示例

[`fastapi_request_state_demo.py`](./fastapi_request_state_demo.py)
