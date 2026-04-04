"""
可参数化依赖（callable 实例）— 对应 06_di_parameterized_dependencies.md

运行：
  uvicorn fastapi_dep_parameterized_demo:app --reload --app-dir fastapi_learning_docs/04_dependency_injection

文档：http://127.0.0.1:8000/docs
"""

from fastapi import Depends, FastAPI

app = FastAPI(title="Parameterized dependency demo")


class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content

    def __call__(self, q: str = ""):
        if q:
            return self.fixed_content in q
        return False


checker_bar = FixedContentQueryChecker("bar")
checker_foo = FixedContentQueryChecker("foo")


@app.get("/query-checker/")
async def read_query_check(fixed_content_included: bool = Depends(checker_bar)):
    return {"fixed_content_in_query": fixed_content_included}


@app.get("/query-checker-foo/")
async def read_query_check_foo(foo_included: bool = Depends(checker_foo)):
    return {"foo_in_query": foo_included}


@app.get("/")
def root():
    return {
        "docs": "/docs",
        "try": [
            "/query-checker/?q=foobar",
            "/query-checker/?q=hello",
            "/query-checker-foo/?q=food",
        ],
    }
