# Python 协程（一）概述

> 本文整理自网络公开教程，用于与 [LEARNING_GUIDE.md](../../LEARNING_GUIDE.md) 第一阶段对照阅读；代码示例请在本地虚拟环境中运行，第三方库需自行安装。

---

## 一、协程介绍

**协程**（Coroutine），又称微线程或纤程，是一种**用户态**的轻量级调度单位，是实现多任务的一种方式。其本质仍运行在**单个线程**内，通过程序逻辑控制「在哪些代码块之间切换执行顺序」。

更直观的说法：

- 线程里有许多**子程序**（函数）。
- 子程序 A 执行到某处可以**中断**，切换到子程序 B。
- 在合适时机再切回 A，从**上次中断处**继续执行。

这种「协作式」的切换过程，就是常说的协程。

---

## 二、用 `yield`（生成器）实现协作式切换

在 Python 中，**生成器**与 `yield` 可以表达「暂停、恢复」的执行流，从而在函数之间切换控制权。写法相对底层、易读性一般，现代项目更常用 `asyncio`（见第五节）。

延伸阅读（yield 与协程思路）：

- [CSDN：Python yield 与协程相关笔记](https://blog.csdn.net/weixin_41599977/article/details/93656042)

---

## 三、Greenlet 模块

**Greenlet** 用 C 实现协程切换，可在**任意函数**之间切换，而不必先把函数写成 generator。

安装：

```bash
pip install greenlet
```

示例（**人工**切换）：

```python
from greenlet import greenlet
import time


def task_1():
    while True:
        print("--This is task 1!--")
        g2.switch()
        time.sleep(0.5)


def task_2():
    while True:
        print("--This is task 2!--")
        g1.switch()
        time.sleep(0.5)


if __name__ == "__main__":
    g1 = greenlet(task_1)
    g2 = greenlet(task_2)
    g1.switch()
```

输出会交替打印两个任务；切换点由代码显式 `switch()` 控制。

---

## 四、Gevent 模块

**Gevent** 基于 greenlet，在**遇到可被 monkey patch 识别的 I/O** 时**自动**切换任务，减少手写 `switch()`。

安装：

```bash
pip install gevent
```

### 基本用法

```python
import gevent


def eat(name):
    print("%s eat 1" % name)
    gevent.sleep(2)
    print("%s eat 2" % name)


def play(name):
    print("%s play 1" % name)
    gevent.sleep(1)
    print("%s play 2" % name)


g1 = gevent.spawn(eat, "egon")
g2 = gevent.spawn(play, "egon")
gevent.joinall([g1, g2])
```

说明：

- `gevent.sleep` 模拟可被 gevent 识别的阻塞；若使用原生 `time.sleep` 等，需 **monkey patch**。
- `join` / `joinall` 用于等待协程结束；若某任务较长且不 `join`，主程序可能提前退出导致任务未跑完。

### Monkey patch（让 `time.sleep`、`socket` 等可被调度）

```python
from gevent import monkey

monkey.patch_all()  # 尽量放在文件靠前、在 import 可能阻塞的模块之前

import gevent
import time


def eat():
    print("eat food 1")
    time.sleep(2)
    print("eat food 2")


def play():
    print("play 1")
    time.sleep(1)
    print("play 2")


g1 = gevent.spawn(eat)
g2 = gevent.spawn(play)
gevent.joinall([g1, g2])
print("主")
```

要点：**只有被 gevent 识别为 I/O 等待的路径才会触发切换**；若全是 CPU 密集且无等待，则近似串行，协程优势不明显。

---

## 五、Python 3.x 协程与 asyncio

### 1. 早期风格：`@asyncio.coroutine` 与 `yield from`（Python 3.4+）

```python
import asyncio


@asyncio.coroutine
def get_body(i):
    print(f"start{i}")
    yield from asyncio.sleep(1)
    print(f"end{i}")


loop = asyncio.get_event_loop()
tasks = [get_body(i) for i in range(5)]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
```

多个任务会交错 `start` / `end`；`asyncio.sleep` 让出控制权给事件循环。

### 2. 推荐风格：`async` / `await`（Python 3.5+）

把装饰器协程改为原生协程函数：用 **`async def`** 定义，用 **`await`** 等待可等待对象。

```python
import asyncio


async def get_body(i):
    print(f"start{i}")
    await asyncio.sleep(1)
    print(f"end{i}")


async def main():
    await asyncio.gather(*(get_body(i) for i in range(5)))


if __name__ == "__main__":
    asyncio.run(main())
```

**Python 3.7+** 推荐使用 **`asyncio.run(...)`** 作为程序入口：创建事件循环、运行主协程、结束时关闭循环。尽量在整个进程内只作为**顶层入口**调用一次（具体场景可按框架要求调整）。

### 3. 协程对象不能直接「运行」

```python
import asyncio


async def work(x):
    for _ in range(3):
        print("Work {} is running ..".format(x))


coroutine_1 = work(1)  # 这是协程对象，不是函数调用结果

# 方式一（显式循环）：
loop = asyncio.get_event_loop()
result = loop.run_until_complete(coroutine_1)
print(result)  # 若无 return，一般为 None

# 方式二（推荐，3.7+）：
# asyncio.run(work(1))
```

### asyncio 协程的几条结论

1. `async def` 得到的是**协程对象**，需交给**事件循环**驱动执行。
2. 同一时刻在单线程内**只执行一个**协程片段；并发感来自**让出等待**（I/O、sleep 等），不是多核并行。
3. 若 `await` 后面是**同步阻塞**且很重的 CPU 工作，会卡住整个循环——应放到线程池/进程池或改写为异步 API。
4. 协程仍在**单线程**模型下协作，不等同于利用多核的**并行**（parallel）。

---

## 六、为什么要使用协程

CPython 有 **GIL**，多线程在 CPU 密集型场景下往往无法真正并行多核执行，且线程切换有成本。

协程常见优势（概括）：

1. **调度由程序结构表达**（`await`、事件循环），模型相对清晰。
2. 相比频繁操作系统线程切换，协作式切换开销通常更小（视场景而定）。
3. 单线程内共享状态，可减少部分锁的需求（但仍需注意逻辑正确性与异步安全）。

典型适用场景：**高并发 I/O**（如爬虫、网关、大量连接等待）、与 **FastAPI/Starlette** 等异步栈配合。CPU 密集任务仍应考虑多进程或 native 扩展。

---

## 参考链接

- [简书：Python 协程相关](https://www.jianshu.com/p/334388949ac9)
- [CSDN：yield 与协程](https://blog.csdn.net/weixin_41599977/article/details/93656042)
- [CSDN：Python 协程笔记](https://blog.csdn.net/weixin_44251004/article/details/86594117)
- [博客园：协程相关](https://www.cnblogs.com/cheyunhua/p/11017057.html)
- [博客园：Python 之协程](https://www.cnblogs.com/russellyoung/p/python-zhi-xie-cheng.html)
- [博客园：协程笔记](https://www.cnblogs.com/dbf-/p/11143349.html)

---

## 与后续章节

下一主题建议：**Python 协程（二）Asyncio 入门**（可与官方文档 [asyncio](https://docs.python.org/3/library/asyncio.html) 对照）。

原文脉络参考：博客园「麦克煎蛋」《Python协程(一) 概述》（2020-08-14）。
