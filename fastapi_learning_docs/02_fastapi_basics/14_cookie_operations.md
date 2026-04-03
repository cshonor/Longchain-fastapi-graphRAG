# FastAPI Cookie 操作（极简速记）

读取 Cookie 的写法和 `Query`、`Path` 同一套思路；写入 Cookie 则通过 **`Response.set_cookie()`**（或等价响应对象）。

---

## 一、读取客户端发来的 Cookie

```python
from fastapi import Cookie, FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(ads_id: str | None = Cookie(default=None)):
    return {"ads_id": ads_id}
```

- `Cookie(default=None)`：**可选** Cookie；请求里没带该 Cookie 时为 `None`。
- 必填 Cookie：`ads_id: str = Cookie(...)`。

需要文档说明、别名等，与 `Query` / `Path` 一样往 `Cookie(...)` 里塞 `title`、`description`、`alias` 等即可。

---

## 二、后端设置 Cookie（写入 Set-Cookie）

### 方式 1：注入 `Response`（常见）

```python
from fastapi import FastAPI, Response

app = FastAPI()


@app.post("/cookie-and-object/")
def create_cookie(response: Response):
    response.set_cookie(key="fakesession", value="fake-value")
    return {"message": "ok"}
```

### 方式 2：返回 `JSONResponse`

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.post("/cookie/")
def create_cookie():
    response = JSONResponse(content={"message": "ok"})
    response.set_cookie(key="fakesession", value="fake-value")
    return response
```

`set_cookie` 还可设置 `max_age`、`httponly`、`samesite`、`secure` 等，按业务与安全要求选择。

---

## 两句话总结

1. **读 Cookie**：`Cookie(...)`  
2. **写 Cookie**：`response.set_cookie(...)`

---

## 可运行示例

见 [`fastapi_cookie_demo.py`](./fastapi_cookie_demo.py)。
