# Python 枚举（Enum）在 FastAPI 中做严格值校验

这套写法在 FastAPI 里非常常用：用 **Enum** 限制路径参数 / 查询参数只能取“固定可选值”，传错直接 422，并且 `/docs` 会自动显示可选值。

---

## 一、经典写法：`str + Enum`

```python
from enum import Enum


class ModelName(str, Enum):
    resnet = "resnet"
    alexnet = "alexnet"
```

为什么要 `class ModelName(str, Enum)`：

- **既是枚举，又是字符串**：对 API 文档与序列化更友好
- **FastAPI / Pydantic 兼容**：自动生成下拉选择 + 自动校验

---

## 二、Python 3.11+：`StrEnum`（可选）

```python
from enum import StrEnum


class ModelName(StrEnum):
    resnet = "resnet"
    alexnet = "alexnet"
```

---

## 三、FastAPI 最常用场景：路径参数校验

```python
from enum import Enum

from fastapi import FastAPI

app = FastAPI()


class ModelName(str, Enum):
    resnet = "resnet"
    alexnet = "alexnet"


@app.get("/models/{model_name}")
def get_model(model_name: ModelName):
    return {"model": model_name, "message": f"加载 {model_name} 模型"}
```

请求与结果：

- ✅ `GET /models/resnet` → 正常
- ✅ `GET /models/alexnet` → 正常
- ❌ `GET /models/vgg16` → **422 校验错误**

---

## 四、你需要记住的价值

- **类型安全**：告别魔法字符串拼写错误
- **自动校验**：非法值自动拦截
- **文档友好**：Swagger 显示可选值
- **可维护**：集中定义、IDE 自动补全

