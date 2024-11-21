# -*- coding:utf-8 -*-
import os
from pathlib import Path

CHATGLM_MODEL = None
CHATGLM_TOKENIZER = None
LLAMA_MODEL = None
LLAMA_INFERENCER = None
GEMMA_MODEL = None
GEMMA_TOKENIZER = None

# ChatGPT 设置
INITIAL_SYSTEM_PROMPT = "You are a helpful assistant."
API_HOST = "api.openai.com"
OPENAI_API_BASE = "https://api.openai.com/v1"
CHAT_COMPLETION_URL = "https://api.openai.com/v1/chat/completions"
IMAGES_COMPLETION_URL = "https://api.openai.com/v1/images/generations"
COMPLETION_URL = "https://api.openai.com/v1/completions"
BALANCE_API_URL="https://api.openai.com/dashboard/billing/credit_grants"
USAGE_API_URL="https://api.openai.com/dashboard/billing/usage"
HISTORY_DIR = Path("history")
HISTORY_DIR = "history"
TEMPLATES_DIR = "templates"

# 错误信息
STANDARD_ERROR_MSG = "☹️发生了错误："  # 错误信息的标准前缀
GENERAL_ERROR_MSG = "获取对话时发生错误，请查看后台日志"
ERROR_RETRIEVE_MSG = "请检查网络连接，或者API-Key是否有效。"
CONNECTION_TIMEOUT_MSG = "连接超时，无法获取对话。"  # 连接超时
READ_TIMEOUT_MSG = "读取超时，无法获取对话。"  # 读取超时
PROXY_ERROR_MSG = "代理错误，无法获取对话。"  # 代理错误
SSL_ERROR_PROMPT = "SSL错误，无法获取对话。"  # SSL 错误
NO_APIKEY_MSG = "API key为空，请检查是否输入正确。" # API key 长度不足 51 位
NO_INPUT_MSG = "请输入对话内容。"  # 未输入对话内容
BILLING_NOT_APPLICABLE_MSG = "账单信息不适用" # 本地运行的模型返回的账单信息

TIMEOUT_STREAMING = 60  # 流式对话时的超时时间
TIMEOUT_ALL = 200  # 非流式对话时的超时时间
ENABLE_STREAMING_OPTION = True  # 是否启用选择选择是否实时显示回答的勾选框
ENABLE_LLM_NAME_CHAT_OPTION = True  # 是否启用选择是否使用LLM模型的勾选框
CONCURRENT_COUNT = 100 # 允许同时使用的用户数量

SIM_K = 5
INDEX_QUERY_TEMPRATURE = 1.0


ONLINE_MODELS = [
    "Groq 3.2 90B_vision",
    "Groq 3.2 90B"
]

LOCAL_MODELS = [
    "Llama-3.1 8B",
    "Qwen2.5-Coder 7B"
]

DEFAULT_METADATA = {
    "repo_id": None, # HuggingFace repo id, used if this model is meant to be downloaded from HuggingFace then run locally
    "model_name": None, # api model name, used if this model is meant to be used online
    "filelist": None, # file list in the repo to download, now only support .gguf file
    "description": "", # description of the model, displayed in the chatbot header when cursor overing the info icon
    "placeholder": { # placeholder for the model, displayed in the chat area when no message is present
        "slogan": "gpt_default_slogan",
    },
    "model_type": None, # model type, used to determine the model's behavior. If not set, the model type is inferred from the model name
    "multimodal": False, # whether the model is multimodal
    "api_host": None, # base url for the model's api
    "api_key": None, # api key for the model's api
    "system": INITIAL_SYSTEM_PROMPT, # system prompt for the model
    "token_limit": 4096, # context window size
    "single_turn": False, # whether the model is single turn
    "temperature": 1.0,
    "top_p": 1.0,
    "n_choices": 1,
    "stop": [],
    "max_generation": None, # maximum token limit for a single generation
    "presence_penalty": 0.0,
    "frequency_penalty": 0.0,
    "logit_bias": None,
    "stream": True,
    "metadata": {} # additional metadata for the model
}

# Additional metadata for online and local models
MODEL_METADATA = {
    "Groq 3.2 90B_vision": {
        "model_name": "llama-3.2-90b-vision-preview",
        "description": "groq_llama-3.2-90b-vision-preview_description",
        "token_limit": 8192,
        "multimodal": True,
        "model_type": "Groq"
    },
    "Groq 3.2 90B": {
        "model_name": "llama-3.2-90b-text-preview",
        "description": "groq_lama-3.2-90b-text-preview_description",
        "token_limit": 8192,
        "model_type": "Groq"
    },
    
    # LMStudio 本地模型
    "Llama-3.1 8B": {
        "model_name": "meta-llama-3.1-8b-instruct",
        "description": "meta-llama-3.1-8b",
        "token_limit": 8192,
        "model_type": "LMStudio"
    },
    "Qwen2.5-Coder 7B": {
        "model_name": "qwen2.5-coder-7b-instruct",
        "description": "qwen2.5 代码编程",
        "token_limit": 8192,
        "model_type": "LMStudio"
    },

}


MODELS = ONLINE_MODELS + LOCAL_MODELS

DEFAULT_MODEL = 0

RENAME_MODEL = 0