import json
from ..presets import *
import logging
from ..utils import *
from .db.ai_agent import (
    search_ai_agent as SEARCH_AI_AGENT,
    search_ai_agent_id as SEARCH_AI_AGENT_ID,
    update_ai_agent as UPDATE_AI_AGENT,
    save_ai_agent as SAVE_AI_AGENT,
    delete_ai_agent as DELETE_AI_AGENT,
    search_system_agent as SEARCH_SYSTEM_AGENT,
)

logger = logging.getLogger("chat_app")


def save_agent(user_name, agent_data: dict) -> None:
    """保存角色体文件"""
    if agent_data is not None:
        datas = SAVE_AI_AGENT(**buildSaveParams(user_name, agent_data))
        return datas

    return None


def update_agent(user_name, agent_data: dict) -> None:
    """修改角色体文件"""
    if agent_data is not None:
        res = UPDATE_AI_AGENT(**buildUpdateParams(user_name, agent_data))
        if res < 1:
            raise AgentException("INTERNAL_ERROR", "修改角色体失败")

    return None


def buildSaveParams(user_name, agent_data):
    """构建新增参数"""
    return {
        "title": agent_data.get("title"),
        "content": json.dumps(agent_data.get("content", [])),
        "model_key": agent_data.get("model_key"),
        "temperature": agent_data.get("temperature"),
        "top_p": agent_data.get("top_p"),
        "max_tokens": agent_data.get("max_tokens"),
        "presence_penalty": agent_data.get("presence_penalty"),
        "frequency_penalty": agent_data.get("frequency_penalty"),
        "user_icon": agent_data.get("user_icon"),
        "assistant_icon": agent_data.get("assistant_icon"),
        "user_name": user_name,
    }


def buildUpdateParams(user_name, agent_data):
    """构建更新参数"""
    return {
        "id": agent_data.get("id"),
        "title": agent_data.get("title"),
        "content": json.dumps(agent_data.get("content", [])),
        "model_key": agent_data.get("model_key"),
        "temperature": agent_data.get("temperature"),
        "top_p": agent_data.get("top_p"),
        "max_tokens": agent_data.get("max_tokens"),
        "presence_penalty": agent_data.get("presence_penalty"),
        "frequency_penalty": agent_data.get("frequency_penalty"),
        "user_icon": agent_data.get("user_icon"),
        "assistant_icon": agent_data.get("assistant_icon"),
        "user_name": user_name,
    }


def load_agent(user_name, id) -> str:
    """从文件目录中获取角色体文件的内容"""
    data = SEARCH_AI_AGENT_ID(id)

    return data


def get_user_all_agents(user_name, keyword=None):
    """
    获取当前用户所有角色体文件

    根据用户名称和关键词获取用户的所有角色体文件列表如果关键词不为空，则使用关键词过滤角色体列表

    参数:
    user_name (str): 用户名称
    keyword (str): 用于搜索角色体标题的关键词

    返回:
    list: 包含角色体信息的字典列表，每个字典包含角色体的标题和ID
    """
    try:
        agent_list = SEARCH_AI_AGENT(user_name, title=keyword)
        if agent_list is None or len(agent_list) == 0:
            return []
        else:
            for agent_data in agent_list:
                agent_data["edit"] = user_name == agent_data.get("user_name")

            return agent_list
    except Exception as e:
        # 抛出异常
        logger.error(print_err(e))
        raise AgentException("INTERNAL_ERROR", "获取当前用户所有角色体失败")


def del_agent(user_name, id) -> None:
    """删除角色体文件"""
    res = DELETE_AI_AGENT(id)
    if res < 1:
        raise AgentException("INTERNAL_ERROR", "删除角色体失败")


def get_default_agent_data(user_name):
    """获取默认的角色体数据"""
    datas = SEARCH_SYSTEM_AGENT()
    if len(datas) > 0:
        return datas[0]
    return None
