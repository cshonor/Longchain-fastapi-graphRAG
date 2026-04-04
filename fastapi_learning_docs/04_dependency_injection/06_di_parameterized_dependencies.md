# FastAPI 依赖注入（六）可参数化依赖项

**思路**：依赖不必是「写死的全局函数」。若希望**同一套逻辑、多种配置**（例如不同关键字、不同角色名），可定义**带配置的类**：`__init__` 收**配置**，`__call__` 收**请求参数**并返回要注入的值；再 **`Depends(实例)`** 把该实例当作可调用依赖。

与 [依赖项类](./02_di_class_dependency.md) 对照：那一篇是「类本身被调用，`__init__` 由 Query 等填充，**注入的是实例**」；本篇是「**先**用 `__init__` 在代码里配好，`__call__` 再处理请求，**注入的是 `__call__` 的返回值**」。

（上一篇：[yield 依赖项](./05_di_yield_dependencies.md)）

---

## 一、实现步骤

1. 建类，`__init__` 接收**配置参数**。  
2. 实现 **`__call__`**，签名里写要从请求解析的字段（Query、Header 等与普通依赖相同）。  
3. 在模块里 **`实例 = 类(...)`** 创建带不同配置的实例。  
4. 路由里 **`Depends(实例)`**。

---

## 二、示例

```python
from fastapi import Depends, FastAPI

app = FastAPI()


class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content

    def __call__(self, q: str = ""):
        if q:
            return self.fixed_content in q
        return False


checker = FixedContentQueryChecker("bar")


@app.get("/query-checker/")
async def read_query_check(fixed_content_included: bool = Depends(checker)):
    return {"fixed_content_in_query": fixed_content_included}
```

---

## 三、执行方式

FastAPI 会把该实例当作依赖可调用对象，在解析时等价于按请求去调用：

```text
checker(q=<来自请求的 q>)
```

返回值赋给路由参数 `fixed_content_included`。

---

## 四、优点

- 同一类可 new 出**多个不同配置**的实例，少写重复函数。  
- 适合：按资源 ID 校验、不同策略的权限/规则检查、可复用校验器等。

---

## 一句话

**`__init__` 配配置 + `__call__` 吃请求 + `Depends(实例)` = 可参数化、可复用的依赖。**

---

## 可运行示例

见 [`fastapi_dep_parameterized_demo.py`](./fastapi_dep_parameterized_demo.py)。
