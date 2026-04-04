# FastAPI / Starlette 内置中间件（`add_middleware`）

除 [`@app.middleware("http")`](./01_custom_http_middleware.md) 手写中间件外，常用 **`app.add_middleware(类, **配置)`** 挂载 Starlette 提供的现成中间件。

```python
app.add_middleware(SomeMiddlewareClass, option=value)
```

**顺序**：`add_middleware` **先加的后执行（更外层）**、后加的更靠近应用（与栈结构有关，踩坑时查文档或打日志验证）。

---

## 1. `HTTPSRedirectMiddleware`

将 **HTTP** 请求 **301/308 重定向** 到 **HTTPS**（本地 `http://127.0.0.1` 开发时一般**不要**开，否则联调困难）。

```python
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app.add_middleware(HTTPSRedirectMiddleware)
```

---

## 2. `TrustedHostMiddleware`

校验 **`Host` 头**，缓解 Host 头攻击；只允许名单内主机名。

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["yourdomain.com", "*.yourdomain.com"],
)
```

本地开发常见写法：把 **`localhost`**、**`127.0.0.1`** 等加入列表；测试客户端（如 httpx）可能使用 **`testserver`**，也需按需加入。

---

## 3. `GZipMiddleware`

对**响应体**做 **gzip** 压缩（客户端带 `Accept-Encoding: gzip` 时生效），减少体积。

- **`minimum_size`**：小于该字节数不压缩（默认常见为 **500**，以当前 Starlette 文档为准）。

```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

---

## 补充

- 这些类来自 **Starlette**，FastAPI 直接复用。  
- 其他 **ASGI 中间件**若符合接口，也可通过 `add_middleware` 或底层 ASGI 组合接入（以具体库说明为准）。

---

## 可运行示例

见 [`fastapi_builtin_middleware_demo.py`](./fastapi_builtin_middleware_demo.py)（含 **TrustedHost** + **GZip**；**未**启用 HTTPS 重定向，便于本地调试）。
