# FastAPI Query 参数附加信息（`Query(...)`）

这章讲 **Query 参数（URL `?xxx=`）的“附加信息”**：用 `Query(...)` 给查询参数加**校验规则、文档说明、别名、废弃标记**等。

---

## 1. 作用

使用 `Query` 为查询参数提供：

- 校验规则（长度、正则/模式、必填等）
- 接口文档说明（title/description）
- 参数别名（alias）
- 标记废弃（deprecated）

---

## 2. 基本用法

```python
from fastapi import Query
```

- 可选参数：

```python
q: str | None = Query(None)
```

- 带默认值：

```python
q: str = Query("default")
```

- 必填参数：

```python
q: str = Query(...)
```

---

## 3. 常用校验参数

- `min_length`：最小长度
- `max_length`：最大长度
- `pattern`：正则模式（更推荐；部分旧资料写 `regex`）
- `title` / `description`：接口文档说明
- `deprecated`：标记参数废弃
- `alias`：参数别名（支持如 `item-query` 这种非 Python 合法变量名）

示例：

```python
q: str | None = Query(
    None,
    alias="item-query",
    title="Query string",
    description="Search query",
    min_length=3,
    max_length=50,
    pattern="^fixedquery$",
    deprecated=True,
)
```

---

## 4. 列表参数（多值 query）

接收 `?q=1&q=2&q=3`：

```python
from fastapi import Query

q: list[str] | None = Query(None)
```

带默认值列表：

```python
q: list[str] = Query(["foo", "bar"])
```

如果直接写成 `list`，会丢失元素类型信息（不推荐）：

```python
q: list | None = Query(None)
```

