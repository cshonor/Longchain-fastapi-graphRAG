"""
Cookie 读取与设置 — 对应 14_cookie_operations.md

运行：
  uvicorn fastapi_cookie_demo:app --reload --app-dir fastapi_learning_docs/02_fastapi_basics

文档：http://127.0.0.1:8000/docs
"""

from fastapi import Cookie, FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI(title="FastAPI Cookie demo")


@app.get("/items/")
async def read_items(ads_id: str | None = Cookie(default=None, description="Optional tracking id")):
    return {"ads_id": ads_id}


@app.post("/cookie-and-object/")
def create_cookie_with_response(response: Response):
    response.set_cookie(key="fakesession", value="fake-value", httponly=True)
    return {"message": "ok"}


@app.post("/cookie-json/")
def create_cookie_json_response():
    response = JSONResponse(content={"message": "ok"})
    response.set_cookie(key="fakesession", value="fake-value", httponly=True)
    return response


@app.get("/")
def root():
    return {
        "docs": "/docs",
        "try": [
            "GET /items/",
            "GET /items/  + Header Cookie: ads_id=hello",
            "POST /cookie-and-object/",
            "POST /cookie-json/",
        ],
    }
