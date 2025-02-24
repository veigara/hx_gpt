# -*- coding:utf-8 -*-
import os
from pathlib import Path

# ChatGPT 设置
INITIAL_SYSTEM_PROMPT = "You are a helpful assistant."
# qwen
QWEN_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
# 讯飞星火
SPARK_BASE_URL = "https://spark-api-open.xf-yun.com/v1"


# 配置文件存放地址
CONFIG_DIR = "chat_app/config.json"
# 系统默认用户
SYS_USER_NAME = "system"
# 知识库上传文件地址
KNOWLEDGE_UPLOAD_FILE_DIR = "knowledge/upload_file"
# 对话上传文件地址
CHAT_UPLOAD_FILE_DIR = "chat/upload_file"
# 对话解析文件地址
CHAT_PARSE_FILE_DIR = "chat/parse_file"

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

# 知识库检索格式st
KNOWLEDGE_PROMPT_TEMPLATE = """\
Context information is below.
---------------------
{context_str}
---------------------
Current date: {current_date}.
Using the provided context information, write a comprehensive reply to the given query.
If the provided context information refer to multiple subjects with the same name, write separate answers for each subject and put this select detail context information at the end in the form.
Use prior knowledge only if the given context didn't provide enough information.
 
Answer the question: {query_str}
Reply in Simplified Chinese
"""
