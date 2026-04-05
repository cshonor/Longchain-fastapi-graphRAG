"""
PromptTemplate / ChatPromptTemplate + LCEL — 对应 05_prompt_template.md

在仓库根目录执行（便于加载 .env）:
  python langchain-learning-notes/02_langchain_first_experience/demo_prompt_template.py

无需 Key 的部分: f-string 对比、format / format_messages（本地即可看输出）。
可选链式调用（需环境变量）:
  DASHSCOPE_API_KEY  — PromptTemplate | Tongyi
  DEEPSEEK_API_KEY   — ChatPromptTemplate | ChatDeepSeek

依赖: pip install -r requirements.txt
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
try:
    from dotenv import load_dotenv

    load_dotenv(_ROOT / ".env")
except ImportError:
    pass


def demo_fstring_vs_template() -> None:
    product = "保温杯"
    s_f = f"给生产 {product} 的公司取一个好听的名字。"

    from langchain_core.prompts import PromptTemplate

    p = PromptTemplate.from_template("给生产 {product} 的公司取一个好听的名字。")
    s_t = p.format(product=product)

    print("[1] f-string vs PromptTemplate.format")
    print("  f-string :", s_f)
    print("  template :", s_t)
    print()


def demo_format_messages() -> None:
    from langchain_core.prompts import ChatPromptTemplate

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个专业的 {role}，只回答 {language} 问题。"),
            ("human", "{question}"),
        ]
    )
    msgs = chat_prompt.format_messages(
        role="Python 工程师",
        language="中文",
        question="如何高效学习 Python？",
    )
    print("[2] ChatPromptTemplate.format_messages（无网络）")
    for i, m in enumerate(msgs):
        print(f"  [{i}] {type(m).__name__}: {m.content!r}")
    print()


def demo_chain_prompt_tongyi() -> None:
    key = os.environ.get("DASHSCOPE_API_KEY")
    if not key:
        print("[3] PromptTemplate | Tongyi — 跳过：未设置 DASHSCOPE_API_KEY\n")
        return

    try:
        from langchain_community.llms.tongyi import Tongyi
    except ImportError:
        print("[3] PromptTemplate | Tongyi — 跳过：未安装 langchain-community\n")
        return

    from langchain_core.prompts import PromptTemplate

    prompt = PromptTemplate.from_template(
        "你是起名助手。产品：{product}。请只给出 3 个公司名，逗号分隔，不要其它解释。"
    )
    llm = Tongyi(api_key=key)
    chain = prompt | llm
    text = chain.invoke({"product": "保温杯"})
    print("[3] LCEL: PromptTemplate | Tongyi（补全 LLM，输入为 str）")
    print("  输出:", text)
    print()


def demo_chain_chat_deepseek() -> None:
    key = os.environ.get("DEEPSEEK_API_KEY")
    if not key:
        print("[4] ChatPromptTemplate | ChatDeepSeek — 跳过：未设置 DEEPSEEK_API_KEY\n")
        return

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_deepseek import ChatDeepSeek

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个助手，围绕 {topic} 帮助用户。回答简洁。"),
            ("human", "{content}"),
        ]
    )
    llm = ChatDeepSeek(model="deepseek-chat", api_key=key)
    chain = prompt | llm
    result = chain.invoke(
        {"topic": "创意生成", "content": "给杯子公司起 3 个名字，逗号分隔。"}
    )
    print("[4] LCEL: ChatPromptTemplate | ChatDeepSeek（ChatModel，输入为消息列表）")
    print("  输出类型:", type(result).__name__)
    print("  内容:", getattr(result, "content", result))
    print()


def main() -> None:
    os.chdir(_ROOT)
    print("工作目录:", _ROOT)
    print("对应笔记: langchain-learning-notes/02_langchain_first_experience/05_prompt_template.md")
    print("-" * 60)
    demo_fstring_vs_template()
    demo_format_messages()
    demo_chain_prompt_tongyi()
    demo_chain_chat_deepseek()


if __name__ == "__main__":
    main()
