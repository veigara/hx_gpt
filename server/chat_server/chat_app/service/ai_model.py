"""模型设置"""

import os
import json
from enum import Enum
from ..presets import *


def get_model_type() -> list:
    """获取模型类型"""
    return ModelType.get_all_categories()


def get_all_models(keyword) -> list:
    """获取所有模型名称"""
    josn_data = get_model_data()
    if keyword is not None:
        datas = [
            covert_model_data(key, value)
            for key, value in josn_data.items()
            if keyword.lower() in key.lower()
        ]
        return datas
    if josn_data is not None:
        datas = [covert_model_data(key, value) for key, value in josn_data.items()]
        return datas
    else:
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


def get_model_detail(model_name) -> dict:
    """获取模型详情"""
    josn_data = get_model_data()
    if josn_data is not None:
        return josn_data.get(model_name)
    else:
        return {}


def update_model_detail(model_name, model_detail):
    """更新模型详情"""
    josn_data = get_model_data()
    josn_data[model_name] = model_detail

    save_model(josn_data)


def remove_model(model_name):
    """删除模型"""
    josn_data = get_model_data()
    josn_data.pop(model_name)

    save_model(josn_data)


def get_model_name_list():
    """获取模型名称列表"""
    return [model_key for model_key in get_model_data()]


def get_model_data():
    """获取模型数据"""
    model_config_path = os.path.join(MODEL_CONFIG_DIR)
    with open(model_config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_model(model_data):
    """写入模型数据到文件"""
    model_config_path = os.path.join(MODEL_CONFIG_DIR)
    # 写入文件
    with open(model_config_path, "w", encoding="utf-8") as f:
        json.dump(model_data, f, ensure_ascii=False, indent=4)


class ModelType(Enum):
    """模型类别"""

    GROQ = "Groq"
    LMSTUDIO = "LMStudio"

    @classmethod
    def get_all_categories(cls):
        return [type.value for type in ModelType]
