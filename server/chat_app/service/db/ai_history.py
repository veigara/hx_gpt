from ...db_models.db_history import AiHistory
from typing import List, Dict, Any
from datetime import datetime
from ...presets import *
import json
from ..db.ai_agent import search_ai_agent_id as SEARCH_AI_AGENT_ID


def save_ai_history(
    title, content, agent_id, all_token_counts, count, user_name
) -> dict:
    """保存聊天记录基本信息"""
    data = AiHistory(
        title=title,
        content=content,
        agent_id=agent_id,
        all_token_counts=all_token_counts,
        count=count,
        user_name=user_name,
    )
    data.save()
    return to_dict(data)


def update_ai_history(
    id, title, content, agent_id, all_token_counts, count, user_name
) -> int:
    """更新聊天记录基本信息"""
    res = AiHistory.objects.filter(id=id).update(
        title=title,
        content=content,
        agent_id=agent_id,
        all_token_counts=all_token_counts,
        count=count,
        user_name=user_name,
        update_time=datetime.now(),
    )

    return res


def update_ai_history_title(id, title, user_name) -> int:
    """更新聊天记录名称"""
    res = AiHistory.objects.filter(id=id).update(
        title=title,
        user_name=user_name,
        update_time=datetime.now(),
    )

    return res


def update_ai_history_content(id, content, user_name) -> int:
    """更新聊天记录内容"""
    res = AiHistory.objects.filter(id=id).update(
        content=content,
        user_name=user_name,
        update_time=datetime.now(),
    )
    return res


def search_ai_history_content(id) -> Any:
    """根据主键搜索聊天记录内容

    Args:
        id (int): 主键

    Returns:
        dict: 聊天记录内容
    """
    data = AiHistory.objects.get(id=id)
    content = json.loads(data.content)
    if not content:
        content = []
    return content


def search_ai_history(user_name: str, title: str = None) -> List[Dict[str, Any]]:
    """根据聊天记录名称搜索聊天记录基本信息

    Args:
        user_name (str): 用户名
        title (str): 聊天记录名称

    Returns:
        List[Dict[str, Any]]: 搜索结果
    """
    try:
        if not user_name or not isinstance(user_name, str):
            return []

        filters = {"user_name": user_name}

        if title and isinstance(title, str):
            filters["title__icontains"] = title.strip()

        results = AiHistory.objects.order_by("-create_time").filter(**filters)

        # 添加字段后，自动转为dict
        datas = list(results)

        if len(datas) == 0:
            return []

        return [to_dict(item) for item in datas]

    except Exception as e:
        raise e


def search_ai_history_id(id) -> dict:
    """根据主键搜索"""
    data = AiHistory.objects.get(id=id)
    return to_dict(data)


def delete_ai_history(id):
    """根据主键删除
    @return int: 删除的行数
    """
    deleted_count, _ = AiHistory.objects.filter(id=id).delete()

    return deleted_count


def update_create_time(id, create_time) -> int:
    """更新创建时间"""
    return AiHistory.objects.filter(id=id).update(create_time=create_time)


def delete_ai_history_all(user_name):
    """根据主键删除
    @return int: 删除的行数
    """
    deleted_count, _ = AiHistory.objects.filter(user_name=user_name).delete()

    return deleted_count


def serarch_ai_history_tokens(id) -> dict:
    """根据主键搜索获取tokens"""
    data = AiHistory.objects.values("id", "count", "all_token_counts").get(id=id)
    return data


def search_ai_history_agent_id(agent_id: str) -> dict:
    """根据角色体id搜索"""
    filters = {"agent_id": agent_id}
    datas = AiHistory.objects.order_by("-create_time").filter(**filters)
    if len(datas) == 0:
        return []

    return [to_dict(item) for item in datas]


def to_dict(data: AiHistory) -> dict:
    if data is None:
        return {}
    content = json.loads(data.content)
    agent_id = data.agent_id
    if agent_id is not None:
        # 查询角色体详情
        agent_data = SEARCH_AI_AGENT_ID(agent_id)
    return {
        "id": data.id,
        "title": data.title,
        "content": content,
        "agent_id": data.agent_id,
        "all_token_counts": data.all_token_counts,
        "count": data.count,
        "user_name": data.user_name,
        "create_time": data.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        "agent_data": agent_data,
    }
