import os
import commentjson as json
import logging
from .presets import *
from .service.ai_model import get_model_name_list, get_model_detail
from .service.config import *

logger = logging.getLogger("chat_app")


def groq_api_key():
    return get_config_data().get("groq_api_key", "")


def lmstudio_url():
    return get_config_data().get("lmstudio_url", "")


def lmstudio_api_key():
    return get_config_data().get("lmstudio_api_key", "")


def default_model():
    return get_config_data().get("default_model", "")


def qwen_api_key():
    return get_config_data().get("qwen_api_key", "")


def spark_api_key():
    return get_config_data().get("spark_api_key", "")


def redis_url():
    return get_config_data().get("redis_url", "")


def embedding_address():
    return get_config_data().get("embedding", "")


def get_default_model_params(user_name, model_key) -> dict:
    """
    获取模型的默认参数

    """
    # 设置模型默认参数
    model_data = get_model_detail(user_name, model_key)
    if model_data is not None:
        model_data = model_data[0]
        temp_dict = DEFAULT_METADATA.copy()
        temp_dict.update(model_data)
        return temp_dict

    return None


def get_default_model_name() -> str:
    # 设置默认model
    return default_model()
