from typing import List
import json
import datetime
import logging
from ..presets import *
from ..utils import *
from .agent import *
from ..config import *
from ..base_module.agent_exception import AgentException
from .db.ai_history import (
    search_ai_history as SEARCH_AI_HISTORY,
    search_ai_history_id as SEARCH_AI_HISTORY_ID,
    delete_ai_history as DELETE_AI_HISTORY,
    update_ai_history_title as UPDATE_AI_HISTORY_TITLE,
    update_create_time as UPDATE_CREATE_TIME,
    save_ai_history as SAVE_AI_HISTORY,
    delete_ai_history_all as DELETE_AI_HISTORY_ALL,
    update_ai_history_content as UPDATE_AI_HISTORY_CONTENT,
    search_ai_history_content as SEARCH_AI_HISTORY_CONTENT,
    update_ai_history as UPDATE_AI_HISTORY,
    serarch_ai_history_tokens as SERARCH_AI_HISTORY_TOKENS,
)

logger = logging.getLogger("chat_app")


def get_user_all_history(user_name, keyword):
    """
    获取当前用户所有聊天记录文件

    根据用户名称和关键词获取用户的所有聊天记录文件列表如果关键词不为空，则使用关键词过滤聊天记录列表

    参数:
    user_name (str): 用户名称
    keyword (str): 用于搜索聊天记录标题的关键词

    返回:
    list: 包含聊天记录信息的字典列表，每个字典包含聊天记录的标题和ID
    """
    return SEARCH_AI_HISTORY(user_name, title=keyword)


def load_history(id) -> str:
    """通过id获取聊天记录详情"""
    return SEARCH_AI_HISTORY_ID(id)


def rename_history(user_name, id, new_title) -> None:
    """重命名聊天记录"""
    res = UPDATE_AI_HISTORY_TITLE(id, new_title, user_name)
    if res < 1:
        raise AgentException("重命名聊天记录失败")


def del_history(user_name, id) -> None:
    """删除聊天记录"""
    res = DELETE_AI_HISTORY(id)
    if res < 1:
        raise AgentException("删除聊天记录失败")


def cretate_new_history(user_name, model_name, input_str) -> str:
    """创建新的聊天记录,没有智能体
    params:input_str 用户输入
    return:history_id 聊天记录id
    """
    agent_data = get_default_agent_data(user_name)
    if agent_data is None:
        raise Exception("系统没有智能体,请先设置智能体")
    agent_data["history_title"] = input_str[:20]
    agent_data["model_name"] = model_name

    return save_history_agent(user_name, agent_data)


def save_history(user_name, history_data) -> dict:
    """保存聊天记录文件"""
    # 聊天记录名称
    title = history_data.get("title")
    if title is None:
        raise "聊天记录名称不能为空"
    return SAVE_AI_HISTORY(**buildSaveParams(user_name, history_data))


def update_history_all(user_name, history_data) -> int:
    res = UPDATE_AI_HISTORY(**buildUpdateParams(user_name, history_data))
    if res < 1:
        raise AgentException("更新聊天记录失败")
    return res


def buildSaveParams(user_name, history_data):
    """构建新增参数"""
    return {
        "title": history_data.get("title"),
        "content": json.dumps(history_data.get("content", [])),
        "agent_id": history_data.get("agent_id"),
        "all_token_counts": history_data.get("all_token_counts"),
        "count": history_data.get("count"),
        "user_name": user_name,
    }


def buildUpdateParams(user_name, history_data):
    """构建新增参数"""
    return {
        "id": history_data.get("id"),
        "title": history_data.get("title"),
        "content": json.dumps(history_data.get("content", [])),
        "agent_id": history_data.get("agent_id"),
        "all_token_counts": history_data.get("all_token_counts"),
        "count": history_data.get("count"),
        "user_name": user_name,
    }


def save_history_agent(user_name, agentData) -> str:
    """从智能体中创建聊天记录"""
    agent_title = agentData.get("title", "新的聊天")
    history_title = agentData.get("history_title")
    title = (
        agent_title if history_title is None or history_title == "" else history_title
    )
    history = agentData.get("content", [])
    agent_id = agentData.get("id")

    # 对话条数
    count = len(history)
    all_token_counts = count_user_history_token(history)
    history_data = {
        "title": title,
        "content": history,
        "agent_id": agent_id,
        "all_token_counts": all_token_counts,
        "count": count,
    }
    res = save_history(user_name, history_data)
    id = res.get("id", None)
    if not id:
        raise AgentException("创建聊天记录失败")

    return res.get("id", None)


def count_user_history_token(contents) -> int:
    """统计聊天记录的token数
    params: contents: [{"role": "user", "content": "示例：我很开心，因为今天出去玩了"}, {"role": "assistant", "content": "用文言文表达输入的内容"}]
    """
    total = 0
    if contents is None:
        return total
    user_contents = [content.get("content") for content in contents]

    for content in user_contents:
        if content is None:
            continue
        if isinstance(content, list):
            # 判断是数组
            for item in content:
                if item.get("type") == "text":
                    total += count_token(item["text"])
        else:
            total += count_token(content)

    return total


def update_history_content(user_name, id, content) -> None:
    """更新聊天记录内容"""
    res = UPDATE_AI_HISTORY_CONTENT(id, json.dumps(content), user_name)
    if res < 1:
        raise AgentException("更新聊天记录失败")


def get_history_content(id) -> List:
    """获取聊天记录内容"""
    return SEARCH_AI_HISTORY_CONTENT(id)


def update_history(user_name, history_id, contents: list) -> None:
    """修改聊天记录，对话防止超限,在以前的记录省增加
    history_id(str):id 聊天记录id
    content([]):当前对话
    max_content_len(int) 最大上下文
    """
    try:
        history_data = load_history(history_id)
        if history_data is None:
            raise AgentException(f"聊天记录不存在,id={history_id}")
        count = history_data.get("count", 0)
        all_token_counts = history_data.get("all_token_counts", 0)
        content_data = history_data.get("content", [])
        history_data["count"] = int(count) + len(contents)
        cur_chat_token = count_user_history_token(contents)
        history_data["all_token_counts"] = int(all_token_counts) + cur_chat_token
        content_data.extend(contents)

        # 保存
        update_history_all(user_name, history_data)

    except Exception as e:
        logger.error(print_err(e))
        raise AgentException(f"{STANDARD_ERROR_MSG}:修改聊天记录失败")


def top_history(history_id) -> None:
    """置顶聊天记录"""
    res = UPDATE_CREATE_TIME(history_id, datetime.datetime.now())
    if res < 1:
        raise AgentException("置顶聊天记录失败")


def clear_all_history(user_name) -> None:
    """删除所有聊天记录"""
    res = DELETE_AI_HISTORY_ALL(user_name)
    if res < 1:
        raise AgentException("删除所有聊天记录失败")


def clear_context(user_name, history_id) -> None:
    """清空上下文"""
    history_data = load_history(history_id)
    if history_data is None:
        raise AgentException(f"聊天记录不存在,id={history_id}")
    if not history_data:
        return
    agent_data = history_data.get("agent_data", "{}")
    content_data = agent_data.get("content", [])
    history_data["content"] = content_data
    history_data["count"] = len(content_data)
    history_data["all_token_counts"] = count_user_history_token(content_data)

    # 更新聊天记录
    update_history_all(user_name, history_data)


def get_count_tokens(history_id) -> dict:
    """获取当前聊天记录的tokens和count"""
    return SERARCH_AI_HISTORY_TOKENS(history_id)


def update_history_id(user_name, history_id, contents: list) -> None:
    """
    根据id更新聊天记录，直接覆盖原内容，并重新计算token和对话数量
    @param user_name: 用户名
    @param history_id: 聊天记录id
    @param contents: 替换的对话内容
    @return: None
    """
    history_data = load_history(history_id)
    if history_data is None:
        raise AgentException(f"聊天记录不存在,id={history_id}")
    # 对话条数
    history_data["count"] = len(contents)
    # 对话token
    history_data["all_token_counts"] = count_user_history_token(contents)
    # 将原来历史记录替换
    history_data["content"] = contents

    update_history_all(user_name, history_data)


def snip_history_build(user_name, history_id, contents: list) -> dict:
    """
    以这个新的消息内容为基准，按照以前的参数新建一个聊天记录
    @param user_name: 用户名
    @param history_id: 聊天记录id
    @param contents: 对话内容
    @return: None
    """
    history_data = load_history(history_id)
    if history_data is None:
        raise AgentException(f"聊天记录不存在,id={history_id}")
    # 对话条数
    history_data["count"] = len(contents)
    # 对话token
    history_data["all_token_counts"] = count_user_history_token(contents)
    # 将原来历史记录替换
    history_data["content"] = contents
    title = history_data.get("title")
    history_data["title"] = f"{title}-Branched"
    history_data["id"] = None

    return save_history(user_name, history_data)
