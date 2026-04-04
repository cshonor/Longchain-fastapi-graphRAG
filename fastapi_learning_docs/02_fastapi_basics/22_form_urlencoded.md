# FastAPI 接收表单数据（Form）

客户端使用 application/x-www-form-urlencoded（或带文件的 multipart/form-data）提交键值对时，在路由参数上用 Form(...) 声明。与 [Request Body（JSON）](./07_request_body.md) 区分：表单用 Form，JSON 用 Pydantic 模型。

OAuth2 密码流里的 OAuth2PasswordRequestForm 也是表单字段，见 [安全](../05_security/02_oauth2_jwt_token.md)。

---

## 1. 依赖

```bash
pip install python-multipart
```

仓库 requirements.txt 若已含 python-multipart 可直接使用。

---

## 2. 导入与声明

```python
from fastapi import FastAPI, Form

app = FastAPI()


@app.post("/login/")
async def login(*, username: str = Form(...), password: str = Form(...)):
    return {"username": username}
```

- Form(...) 表示必填；可用默认值或 Form(None) 表示可选。
- 用法与 Query、Path、Body 类似，可加 description、min_length 等。
- 前置 * 仅让后续参数按关键字传入，可选。

---

## 3. 客户端

- HTML form 默认 enctype 即为 x-www-form-urlencoded。
- Postman：x-www-form-urlencoded 或 form-data。
- axios：Content-Type 为 application/x-www-form-urlencoded 并对 body 编码。
- requests：使用 data= 字典，不要用 json=。

同一接口混用 File() 与 Form() 时为 multipart/form-data，仍由 python-multipart 解析。

---

## 4. 可运行示例

见 [fastapi_form_demo.py](./fastapi_form_demo.py)（根路径 HTML 表单 + POST /login/）。

---

内容整理自博客园「麦克煎蛋」等 FastAPI 表单教程，按当前 FastAPI 用法统一表述。
