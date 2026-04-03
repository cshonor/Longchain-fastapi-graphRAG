"""
Query(...) 附加信息 Demo，对应 09_query_params_query_extra.md

运行（任选其一）：
  在项目根目录 longchain/ 下：
    uvicorn fastapi_query_extra_demo:app --reload --app-dir fastapi_learning_docs/02_fastapi_basics
  或先进入本目录再启动：
    cd fastapi_learning_docs/02_fastapi_basics
    uvicorn fastapi_query_extra_demo:app --reload

文档：http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, Query

app = FastAPI(title="Query(...) extra info demo")


# 1) 可选 + 校验 + 文档信息 + deprecated + alias
# - alias 用于支持非 Python 变量名的参数，如 item-query
# - pattern 用于正则校验
@app.get("/search")
def search(
    q: str | None = Query(
        None,
        alias="item-query",
        title="Query string",
        description="Search query (accepts only 'fixedquery' here for demo)",
        min_length=3,
        max_length=50,
        pattern="^fixedquery$",
        deprecated=True,
    ),
):
    return {"q": q}


# 2) 必填 Query：Query(...) 让它成为 required
@app.get("/required")
def required_query(q: str = Query(..., min_length=1, description="Required query string")):
    return {"q": q}


# 3) 多值 Query：?q=1&q=2&q=3
@app.get("/tags")
def list_query(q: list[str] | None = Query(None, description="Repeat ?q= to pass multiple values")):
    return {"q": q}


@app.get("/")
def root():
    return {
        "docs": "/docs",
        "try": [
            # alias 的参数名是 item-query（不是 q）
            "GET /search?item-query=fixedquery",
            "GET /search?item-query=bad   # 422 (pattern)",
            "GET /required?q=hello",
            "GET /required   # 422 (missing q)",
            "GET /tags?q=foo&q=bar&q=baz",
        ],
    }

