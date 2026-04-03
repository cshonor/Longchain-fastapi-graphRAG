# FastAPI Header 操作（读取与返回）

读取请求头的方式与 `Query`、`Path`、`Cookie` 同一套路；写入响应头则通过 **`Response.headers`** 或在 **`JSONResponse(..., headers=...)`** 里传入。（与 [Cookie](./14_cookie_operations.md) 对称。）

---

## 一、读取 Header

```python
from fastapi import Header

# 可选：未带该头时为 None
user_agent: str | None = Header(default=None)
```

`Header` 与 `Query` / `Path` / `Cookie` 一样，可附加 `title`、`description`、`alias`、`deprecated` 等元信息。

---

## 二、下划线与连字符（`User-Agent` 等）

HTTP 头名里常有 `-`（如 `User-Agent`），Python 变量名不能写 `-`。

FastAPI 的 `Header` 默认会把参数名里的 **`_` 转成 `-`**，因此可用 **`user_agent`** 表示请求头 **`User-Agent`**。

```python
@app.get("/items/")
async def read_items(*, user_agent: str | None = Header(default=None)):
    return {"user_agent": user_agent}
```

若**不要**这种自动转换，可设置：

```python
Header(default=None, convert_underscores=False)
```

多数场景保持默认即可。

---

## 三、重复的同名 Header（多值）

同一头名出现多次时，可用 **`list[str]`** 接收（例如多个 `X-Token`）：

```python
x_token: list[str] | None = Header(default=None)
```

具体行为以当前 FastAPI / Starlette 版本为准；可在 `/docs` 里试请求。

---

## 四、向客户端返回 Header

### 1. 注入 `Response`，写 `response.headers[...]`

```python
from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/headers-and-object/")
def get_headers(response: Response):
    response.headers["X-Cat-Dog"] = "alone in the world"
    return {"message": "Hello World"}
```

### 2. 使用 `JSONResponse(..., headers=...)`

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/headers-json/")
def get_headers_json():
    content = {"message": "Hello World"}
    headers = {"X-Cat-Dog": "alone in the world", "Content-Language": "en-US"}
    return JSONResponse(content=content, headers=headers)
```

---

## 两句话总结

1. **读请求头**：`Header(...)`  
2. **写响应头**：`response.headers[...]` 或构造 `JSONResponse` 时传入 `headers`

---

## 参考来源

- 麦克煎蛋：《FastAPI 基础学习(十三) Header操作》，博客园  
  https://www.cnblogs.com/mazhiyong/

（原文中 `convert_underscores=False` 的拼写为 **False**。）

---

## 可运行示例

见 [`fastapi_header_demo.py`](./fastapi_header_demo.py)。
