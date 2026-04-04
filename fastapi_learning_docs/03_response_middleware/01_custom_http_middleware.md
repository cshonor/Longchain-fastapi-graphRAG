# FastAPI 中间件（一）自定义 HTTP 中间件

中间件是在**请求进入具体路由之前**与**响应返回客户端之前**执行的**全局**逻辑，适合日志、计时、统一响应头、简单鉴权等横切能力。

（与 `02_fastapi_basics` 里 [Response / 状态码](../02_fastapi_basics/16_response_status_code.md) 互补：中间件改的是**整条链路**，不单某一路由。）

---

## 一、执行顺序（概念）

1. 收到 `request`  
2. **前置**逻辑（鉴权、日志开始时间等）  
3. **`response = await call_next(request)`** → 继续走后续中间件与路由  
4. 拿到 `response`  
5. **后置**逻辑（加头、记录耗时等）  
6. `return response`

> **BackgroundTasks** 一般在**响应发送完成、中间件走完后**才执行（概念上属于「响应之后」的后台工作）。

---

## 二、注册方式

使用装饰器 **`@app.middleware("http")`**。

函数签名需包含：

- `request: Request`  
- `call_next`：可调用对象，`await call_next(request)` 得到下游的 `Response`

---

## 三、示例：统计处理耗时（`X-Process-Time`）

```python
import time

from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    return response
```

计时用 **`time.perf_counter()`** 比 `time.time()` 更适合测量间隔。

---

## 四、常见用途

- 全局访问日志 / trace id  
- 统一 CORS 以外的自定义响应头  
- 接口耗时、指标采集  
- 简易鉴权、限流（复杂场景常配合专用库或网关）  
- 对异常响应做统一包装（需谨慎，避免掩盖业务错误）

---

## 一句话

- **`@app.middleware("http")`**：注册 HTTP 中间件  
- **`await call_next(request)`**：前后逻辑的分界  
- **前** = 面向请求；**后** = 面向响应  

---

## 可运行示例

见同目录 [`fastapi_middleware_demo.py`](./fastapi_middleware_demo.py)。
