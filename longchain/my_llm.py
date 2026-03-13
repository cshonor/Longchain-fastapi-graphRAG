import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_deepseek import ChatDeepSeek

# 加载 .env（与 env_utils 同级目录）
load_dotenv(Path(__file__).parent / ".env", override=True)

# ========== 核心配置（请替换为你自己的 API Key） ==========
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "你的 DeepSeek API 密钥")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
# ========================================================

# 两种方式创建大模型对象
# 1. 直接使用模型类（推荐新手先使用这种方式，更直观）
deepseek_llm = ChatDeepSeek(
    api_key=DEEPSEEK_API_KEY,      # API 密钥，用于身份认证
    base_url=DEEPSEEK_BASE_URL,    # API 请求地址，默认即可，代理/中转时需修改
    model="deepseek-chat",         # 模型名：deepseek-chat 对话模型，deepseek-reasoner 推理模型
    temperature=0.7,               # 随机性，0-1 之间，值越高回答越灵活
)

# 2. 通过 LangChain 统一通用方式 init_chat_model（兼容多厂商模型时推荐）
llm_unified = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
)

# __name__ 是 Python 内置属性：直接运行本文件时为 "__main__"，被 import 时为模块名；据此区分执行/导入
if __name__ == "__main__":
    # 方式1：调用直接创建的模型
    resp = deepseek_llm.invoke("你好，请介绍一下自己")
    print("=== 直接调用 ChatDeepSeek 结果 ===")
    print(f"返回类型：{type(resp)}")  # 类型是 AIMessage
    print(f"回答内容：{resp.content}\n")

    # 方式2：调用统一初始化的模型（效果一致）
    resp_unified = llm_unified.invoke("你好，用一句话介绍 DeepSeek 模型")
    print("=== 统一方式 init_chat_model 结果 ===")
    print(f"回答内容：{resp_unified.content}")
