"""项目配置文件在线设置"""

import json
import os
from ..presets import *


def get_config() -> dict:
    """获取配置文件"""
    return get_config_data()


def update_config(data):
    """更新配置文件"""
    save_config(data)


def get_config_data():
    """获取配置数据"""
    config_path = os.path.join(CONFIG_DIR)
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        if data is None:
            data = {}
        return data


def save_config(data):
    if data is None:
        return
    """写入配置数据到文件"""
    config_path = os.path.join(CONFIG_DIR)
    # 写入文件
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
