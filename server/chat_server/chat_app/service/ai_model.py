"""模型设置"""

from enum import Enum
from typing import List
from functools import lru_cache
from ..presets import *
from .db.ai_model import (
    search_ai_model as SEARCH_AI_MODEL,
    update_ai_model as UPDATE_AI_MODEL,
    delete_ai_model as DELETE_AI_MODEL,
    save_ai_model as SAVE_AI_MODEL,
)
from ..base_module.agent_exception import AgentException


def get_model_type() -> list:
    """获取模型类型"""
    return ModelType.get_all_categories()


def get_all_models(user_name, model_name=None) -> list:
    """获取所有模型名称"""
    all = SEARCH_AI_MODEL(user_name=user_name, model_name=model_name)
    if all is not None and len(all) > 0:
        return all
    return []


def covert_model_data(key, model_data):
    """将模型数据转换为需要的格式"""
    return {
        "model_key": key,
        "model_name": model_data.get("model_name"),
        "description": model_data.get("description"),
        "model_type": model_data.get("model_type"),
        "multimodal": model_data.get("multimodal"),
        "max_content_len": model_data.get("max_content_len"),
    }


@lru_cache()
def get_model_detail(user_name=None, model_key=None) -> List[dict]:
    """获取模型详情"""
    data = SEARCH_AI_MODEL(user_name=user_name, model_key=model_key)
    if data is not None:
        return data
    else:
        return []


def update_model_detail(user_name, model_detail) -> None:
    """更新模型详情"""
    res = UPDATE_AI_MODEL(**buildUpdateParams(user_name, model_detail))
    if res < 1:
        raise AgentException("更新模型详情")
    # 清空缓存的结果
    get_model_detail.cache_clear()  # 清除所有缓存


def buildUpdateParams(user_name, model_detail):
    """构建更新参数"""
    return {
        "id": model_detail.get("id"),
        "model_key": model_detail.get("model_key"),
        "model_name": model_detail.get("model_name"),
        "description": model_detail.get("description"),
        "model_type": model_detail.get("model_type"),
        "multimodal": model_detail.get("multimodal"),
        "max_content_len": model_detail.get("max_content_len"),
        "user_name": user_name,
    }


def remove_model(id):
    """删除模型"""
    res = DELETE_AI_MODEL(id)
    if res < 1:
        raise AgentException("删除模型详情")


def get_model_name_list(user_name):
    """获取模型名称列表"""
    all = SEARCH_AI_MODEL(user_name=user_name)
    return [item.get("model_key") for item in all]


def save_model(user_name, model_data):
    """保存模型数据"""
    res = SAVE_AI_MODEL(**buildSaveParams(user_name, model_data))
    if not res:
        raise AgentException("保存模型数据失败")


def buildSaveParams(user_name, model_detail):
    """构建新增参数"""
    return {
        "model_key": model_detail.get("model_key"),
        "model_name": model_detail.get("model_name"),
        "description": model_detail.get("description"),
        "model_type": model_detail.get("model_type"),
        "multimodal": model_detail.get("multimodal"),
        "max_content_len": model_detail.get("max_content_len"),
        "user_name": user_name,
    }


class ModelType(Enum):
    """模型类别"""

    GROQ = "Groq"
    LMSTUDIO = "LMStudio"
    QWEN = "Qwen"
    SPARK = "Spark"

    @classmethod
    def get_all_categories(cls):
        return [type.value for type in ModelType]
