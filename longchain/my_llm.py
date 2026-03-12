from langchain_deepseek import ChatDeepSeek

from longchain.env_utils import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

# 两种方式创建大模型对象
# 1. 直接使用模型类
llm = ChatDeepSeek(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
)

# 2. 通过 LangChain 统一通用方式（ChatOpenAI 兼容接口）
# from langchain_openai import ChatOpenAI
# llm = ChatOpenAI(
#     api_key=DEEPSEEK_API_KEY,
#     base_url=DEEPSEEK_BASE_URL,
#     model="deepseek-chat",
# )
