import os
import commentjson as json
import logging
from .presets import *
from .service.ai_model import get_model_name_list, get_model_data
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


def get_default_model_params():
    # 设置模型默认参数,并获取模型数据
    model_data = get_model_data()
    _model_metadata = {}
    if model_data is None:
        raise RuntimeError("模型数据不存在，请检查模型文件")
    for k, v in model_data.items():
        temp_dict = DEFAULT_METADATA.copy()
        temp_dict.update(v)
        _model_metadata[k] = temp_dict
    return _model_metadata


def get_default_model_name() -> str:
    # 设置默认model
    default_model_name = default_model()
    MODELS = get_model_name_list()
    default_model_index = DEFAULT_MODEL
    try:
        if default_model_name in MODELS:
            default_model_index = MODELS.index(default_model_name)

        return MODELS[default_model_index]
    except ValueError:
        logger.error(
            "你填写的默认模型"
            + default_model
            + "不存在！请从下面的列表中挑一个填写："
            + str(MODELS)
        )
        return MODELS[DEFAULT_MODEL]
