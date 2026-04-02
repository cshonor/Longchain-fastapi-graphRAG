# Pydantic 自动类型校验（FastAPI 稳的关键）

这篇讲的核心就是一句话：

**FastAPI 为什么这么稳、这么省心？很多时候全靠 Pydantic 在背后做自动类型校验。**

---

## 一、Pydantic 是干嘛的？

一句话：

**定义数据长什么样 → 传错了直接报错，不用你手写一堆 `if` 判断。**

它通常解决这些事：

- 参数校验
- 数据格式检查
- 类型约束（并生成 Schema）

---

## 二、怎么用？

步骤很固定：

1. 定义一个类，继承 `BaseModel`
2. 写字段 + 类型
3. 传错类型 / 少传字段 → **直接抛异常并给出详细错误**

```python
from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int  # 必须传，必须是 int
    name: str = "jack guo"  # 有默认值，可不传
    signup_timestamp: datetime | None = None
    friends: list[int] = []
```

---

## 三、传错会发生什么？

比如乱传：

```python
User(
    signup_timestamp="不是时间",
    friends=[1, 2, 3, "错的字符串"],
)
```

Pydantic 会一次性告诉你所有问题，例如：

- `id` 缺失
- `signup_timestamp` 格式不对
- `friends` 里出现了非 int

你不需要写这种代码：

```python
if not isinstance(id, int):
    raise Exception(...)
```

---

## 四、和 FastAPI 的关系

FastAPI 内部会把几乎所有“入参/出参”都交给 Pydantic 校验：

- 路径参数类型
- 查询参数类型
- 请求体 JSON 格式与字段类型
- 响应格式（`response_model`）

你写接口时：

```python
from fastapi import FastAPI

app = FastAPI()


@app.post("/user")
def create_user(user: User):
    return user
```

只要前端传的 JSON 不对，FastAPI 会**自动拦截**并返回 **422** 的校验错误。

---

## 五、超级形象的理解

- **Pydantic = 数据安检员**
- **FastAPI = 前台服务**

所有进来的数据先过安检，不合格直接打回。

---

## 六、最终极简总结（背这句）

**Pydantic = 自动数据校验工具**  
**FastAPI = 用它做接口参数校验**  
少写判断，少写 bug，开发更快更稳。

