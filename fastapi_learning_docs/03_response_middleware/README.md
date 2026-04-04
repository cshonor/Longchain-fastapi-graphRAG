# 03 — Response 与中间件（Response & middleware）

**核心内容**：`response_model`、各类 `Response`、自定义头与状态码；中间件、CORS。  
**核心目标**：统一接口输出形态，处理跨域、日志、耗时等横切逻辑。

对照代码：`fastapi_app/main.py`、`fastapi_app/middleware/`。

---

## 本章笔记

- [自定义 HTTP 中间件（`@app.middleware("http")`）](./01_custom_http_middleware.md)
- [中间件 Demo（可直接跑）](./fastapi_middleware_demo.py)

响应与 OpenAPI 的细项笔记主要在 **`../02_fastapi_basics/`**（第 16～21 章）。
