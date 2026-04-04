"""
Form 表单（x-www-form-urlencoded）— 对应 22_form_urlencoded.md

运行：
  uvicorn fastapi_form_demo:app --reload --app-dir fastapi_learning_docs/02_fastapi_basics

浏览器打开 http://127.0.0.1:8000/ 填写表单提交；或打开 /docs 调试 POST /login/
"""

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI(title="Form demo")

LOGIN_PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <title>Form 登录示例</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 28rem; margin: 2rem auto; }
    label { display: block; margin-top: 0.75rem; }
    input { width: 100%; padding: 0.4rem; margin-top: 0.25rem; box-sizing: border-box; }
    button { margin-top: 1rem; padding: 0.5rem 1rem; }
  </style>
</head>
<body>
  <h1>POST /login/（application/x-www-form-urlencoded）</h1>
  <form action="/login/" method="post">
    <label>用户名 <input name="username" required autocomplete="username" /></label>
    <label>密码 <input name="password" type="password" required autocomplete="current-password" /></label>
    <button type="submit">提交</button>
  </form>
  <p><small>提交后浏览器会显示 JSON 响应；也可用 <a href="/docs">/docs</a> 试接口。</small></p>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def index():
    return LOGIN_PAGE


@app.post("/login/")
async def login(*, username: str = Form(...), password: str = Form(...)):
    return {"username": username, "password_received": bool(password)}
