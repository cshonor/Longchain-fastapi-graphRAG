# FastAPI 自定义响应状态码（Response status code）

HTTP 状态码可在三处设置：**路由装饰器**、**注入的 `Response`**、**直接返回 `JSONResponse` 等**。  
（与 [Header](./15_header_operations.md) 里「`Response` 写头」同一套路。）

---

## 一、装饰器参数 `status_code`

写在 `@app.get` / `@app.post` 等装饰器上，对该路由**默认返回**生效；也会出现在 OpenAPI `/docs` 里。

```python
from fastapi import FastAPI

app = FastAPI()


@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}
```

推荐使用 **`fastapi.status`** 里的常量，可读性更好：

```python
from fastapi import FastAPI, status

app = FastAPI()


@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}
```

---

## 二、通过 `Response` 参数设置 `status_code`

在路径操作函数里声明 `response: Response`，按需改写 **`response.status_code`**（也可同时改 headers、cookies）。适用于「是否新建」等**运行期**才能决定状态码的场景。

```python
from fastapi import FastAPI, Response, status

app = FastAPI()

tasks: dict[str, str] = {"foo": "Listen to the Bar Fighters"}


@app.put("/get-or-create-task/{task_id}", status_code=200)
def get_or_create_task(task_id: str, response: Response):
    if task_id not in tasks:
        tasks[task_id] = "This didn't exist before"
        response.status_code = status.HTTP_201_CREATED
    return tasks[task_id]
```

---

## 三、直接返回 `JSONResponse`（或其它 Response）

需要**按分支**返回不同状态码时，可返回带 `status_code` 的响应对象：

```python
from fastapi import Body, FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

items: dict[str, dict] = {
    "foo": {"name": "Fighters", "size": 6},
    "bar": {"name": "Tenders", "size": 3},
}


@app.put("/items/{item_id}")
async def upsert_item(
    item_id: str,
    name: str | None = Body(None),
    size: int | None = Body(None),
):
    if item_id in items:
        item = items[item_id]
        if name is not None:
            item["name"] = name
        if size is not None:
            item["size"] = size
        return item
    item = {"name": name, "size": size}
    items[item_id] = item
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)
```

---

## 小结

| 方式 | 适用 |
|------|------|
| 装饰器 `status_code=` | 该路由**固定**用一种成功码（如 201） |
| `response.status_code = ...` | **运行时**决定（创建 vs 更新等） |
| `JSONResponse(status_code=...)` | 与返回体一起**显式**指定 |

---

## 参考来源

- 麦克煎蛋：《FastAPI 基础学习(十四) Response自定义状态码》，博客园  
  https://www.cnblogs.com/mazhiyong/

---

## 可运行示例

见 [`fastapi_response_status_demo.py`](./fastapi_response_status_demo.py)。
