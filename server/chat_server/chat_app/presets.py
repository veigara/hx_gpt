# -*- coding:utf-8 -*-
import os
from pathlib import Path

# ChatGPT 设置
INITIAL_SYSTEM_PROMPT = "You are a helpful assistant."
API_HOST = "api.openai.com"
OPENAI_API_BASE = "https://api.openai.com/v1"
CHAT_COMPLETION_URL = "https://api.openai.com/v1/chat/completions"
IMAGES_COMPLETION_URL = "https://api.openai.com/v1/images/generations"
COMPLETION_URL = "https://api.openai.com/v1/completions"
BALANCE_API_URL = "https://api.openai.com/dashboard/billing/credit_grants"
USAGE_API_URL = "https://api.openai.com/dashboard/billing/usage"
# 聊天记录存放地址
HISTORY_DIR = "history"
# 用户智能体存放地址
AGENT_DIR = "agentmodels"
# 系统默认智能体存放地址
DEFALUE_AGENT_DIR = "chat_server/chat_app/agentmodels"
# 模型配置文件存放地址
MODEL_CONFIG_DIR = "chat_server/chat_app/model_config/model.json"
# 配置文件存放地址
CONFIG_DIR = "chat_server/chat_app/config.json"
# 系统默认用户
SYS_USER_NAME = "system"

# 错误信息
STANDARD_ERROR_MSG = "☹️发生了错误："  # 错误信息的标准前缀
ERROR_RETRIEVE_MSG = "请检查网络连接，或者API-Key是否有效。"
CONNECTION_TIMEOUT_MSG = "连接超时，无法获取对话。"  # 连接超时
READ_TIMEOUT_MSG = "读取超时，无法获取对话。"  # 读取超时


DEFAULT_METADATA = {
    "repo_id": None,  # HuggingFace repo id, used if this model is meant to be downloaded from HuggingFace then run locally
    "model_name": None,  # api model name, used if this model is meant to be used online
    "filelist": None,  # file list in the repo to download, now only support .gguf file
    "description": "",  # description of the model, displayed in the chatbot header when cursor overing the info icon
    "placeholder": {  # placeholder for the model, displayed in the chat area when no message is present
        "slogan": "gpt_default_slogan",
    },
    "model_type": None,  # model type, used to determine the model's behavior. If not set, the model type is inferred from the model name
    "multimodal": False,  # whether the model is multimodal
    "api_host": None,  # base url for the model's api
    "api_key": None,  # api key for the model's api
    "system": INITIAL_SYSTEM_PROMPT,  # system prompt for the model
    "token_limit": 4096,  # context window size
    "single_turn": False,  # whether the model is single turn
    "temperature": 1.0,
    "top_p": 1.0,
    "n_choices": 1,
    "stop": [],
    "max_generation": None,  # maximum token limit for a single generation
    "presence_penalty": 0.0,
    "frequency_penalty": 0.0,
    "logit_bias": None,
    "stream": True,
    "metadata": {},  # additional metadata for the model
}

# Additional metadata for online and local models
# MODEL_METADATA = {
#     "llama-3.2-90b-vision": {
#         "model_name": "llama-3.2-90b-vision-preview",
#         "description": "groq_llama-3.2-90b-vision-preview_description",
#         "token_limit": 8192,
#         "multimodal": True,
#         "model_type": "Groq",
#     },
#     "llama-3.2-90b-text": {
#         "model_name": "llama-3.2-90b-text-preview",
#         "description": "groq_lama-3.2-90b-text-preview_description",
#         "token_limit": 8192,
#         "model_type": "Groq",
#     },
#     # LMStudio 本地模型
#     "Llama-3.1 8B": {
#         "model_name": "meta-llama-3.1-8b-instruct",
#         "description": "meta-llama-3.1-8b",
#         "token_limit": 8192,
#         "model_type": "LMStudio",
#     },
#     "Qwen2.5-Coder 7B": {
#         "model_name": "qwen2.5-coder-7b-instruct",
#         "description": "qwen2.5 代码编程",
#         "token_limit": 8192,
#         "model_type": "LMStudio",
#     },
# }


# ONLINE_MODELS = ["llama-3.2-90b-vision", "llama-3.2-90b-text"]

# LOCAL_MODELS = ["Llama-3.1 8B", "Qwen2.5-Coder 7B"]

# 所有的模型
# MODELS = ONLINE_MODELS + LOCAL_MODELS

DEFAULT_MODEL = 0

# 所有的模型

# 在线搜索格式st 模板
WEBSEARCH_PTOMPT_TEMPLATE = """\

Web search results:

{web_results}
Current date: {current_date}

Instructions: Using the provided web search results, write a comprehensive reply to the given query. Make sure to cite results using [[number](URL)] notation after the reference. If the provided search results refer to multiple subjects with the same name, write separate answers for each subject.
Query: {query}
Reply in Simplified Chinese
"""
