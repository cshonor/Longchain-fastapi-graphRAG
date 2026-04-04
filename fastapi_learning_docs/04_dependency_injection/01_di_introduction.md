# FastAPI 依赖注入（一）简介

**依赖注入（DI）**：把「多个路由都要用的公共逻辑」抽成**依赖项**，在路由参数里用 **`Depends(...)`** 声明；FastAPI 在进路由前**自动调用**依赖并把**返回值**注入到该参数。

目的：**复用**、**解耦**、少写重复代码。

适用场景：

- 公共 Query / Header 解析  
- 数据库会话、配置  
- 登录态、权限校验  
- 日志与观测  

（与 [Query 参数](../02_fastapi_basics/06_query_params.md) 对照：依赖函数里的 `q`、`skip` 等同样可按 Query 规则从请求解析。）

---

## 一、最小步骤

### 1. 定义依赖（`def` / `async def` 均可）

```python
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}
```

### 2. 路由里用 `Depends(依赖)`

```python
from fastapi import Depends, FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons
```

多个路由可共用同一个 `common_parameters`，各自得到**当前请求**解析出的字典。

---

## 二、执行顺序（概念）

1. 收到请求  
2. FastAPI 解析路由参数，发现 `commons` 来自 `Depends(common_parameters)`  
3. **调用** `common_parameters(...)`（从请求里填 `q` / `skip` / `limit`）  
4. 将返回值赋给 `commons`  
5. 执行路由函数体  

---

## 一句话

**`Depends(xxx)` = 先跑 `xxx`，把返回值当作普通参数传进路由。**

---

## 可运行示例

见 [`fastapi_depends_intro_demo.py`](./fastapi_depends_intro_demo.py)。
