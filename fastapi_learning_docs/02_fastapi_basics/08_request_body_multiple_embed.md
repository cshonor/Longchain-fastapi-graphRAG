# Request Body：多个模型、包一层 key、Body 里的简单类型

在 **Request Body** 里，除了「一个 `BaseModel` 对应一整段 JSON」之外，常见还有三件事：**多个模型一起传**、**单个模型但外层多包一层 key**、**在同一段 JSON 里再传一个简单字段（int/str 等）**。

---

## 1. 多个 Body 参数（两个模型一起传）

```python
async def update_item(item_id: int, item: Item, user: User):
    ...
```

前端（或客户端）发送的 JSON **最外层**要按**参数名**分成多个 key：

```json
{
  "item": { "name": "...", "price": 1.0 },
  "user": { "username": "..." }
}
```

FastAPI 会按参数名把每一段注入对应的 `BaseModel`。

---

## 2. 单个模型，但外层包了一层 key → `embed=True`

若前端发的是：

```json
{
  "item": {
    "name": "..."
  }
}
```

而不是把字段直接放在根上：

```json
{
  "name": "...",
  "price": 1.0
}
```

则要在后端声明时加上 **`embed=True`**：

```python
item: Item = Body(..., embed=True)
```

这样 OpenAPI 与校验规则才会和「多包一层 `item`」的 JSON 一致。

---

## 3. Body 里再传一个简单值（int / str）→ 必须用 `Body(...)`

例如同一段 JSON 里既有两个对象，又有一个单独字段：

```json
{
  "item": { ... },
  "user": { ... },
  "importance": 5
}
```

后端里 **`importance` 必须显式标成 Body**，否则 FastAPI 会把它当成 **Query**，就错了：

```python
importance: int = Body(...)
```

（是否必填用 `Body(...)` vs `Body(5)` 等区分。）

---

## 一句话总结

| 场景 | 做法 |
|------|------|
| 多个模型 | 根 JSON 多个 key，与函数参数名一致 |
| 单模型外包一层 key | `Body(..., embed=True)` |
| JSON 里单独一个标量 | `Body(...)`，不能省略 |

---

## 上一章与下一章

- 上一章：[Request Body 基础（一个 Pydantic 模型）](./07_request_body.md)
- 再往后：接口上的校验规则、字段描述、`Field` 等，属于在「能收 Body」之上的增强。
