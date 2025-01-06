from ...db_models.db_agent import AiAgent
from typing import List, Dict, Any
from datetime import datetime
from ...presets import *
from ..ai_model import get_model_detail as GET_MODEL_DETAIL
import json


def save_ai_agent(
    title,
    content,
    model_key,
    temperature,
    top_p,
    max_tokens,
    presence_penalty,
    frequency_penalty,
    user_icon,
    assistant_icon,
    user_name,
):
    """保存智能体基本信息"""
    data = AiAgent(
        title=title,
        content=content,
        model_key=model_key,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty,
        user_icon=user_icon,
        assistant_icon=assistant_icon,
        user_name=user_name,
    )
    data.save()
    return to_dict(data)


def update_ai_agent(
    id,
    title,
    content,
    model_key,
    temperature,
    top_p,
    max_tokens,
    presence_penalty,
    frequency_penalty,
    user_icon,
    assistant_icon,
    user_name,
):
    """更新智能体基本信息"""
    res = AiAgent.objects.filter(id=id).update(
        title=title,
        content=content,
        model_key=model_key,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty,
        user_icon=user_icon,
        assistant_icon=assistant_icon,
        user_name=user_name,
        update_time=datetime.now(),
    )

    return res


def search_ai_agent(user_name: str, title: str = None) -> List[Dict[str, Any]]:
    """根据智能体名称搜索智能体基本信息

    Args:
        user_name (str): 用户名
        title (str): 智能体名称

    Returns:
        List[Dict[str, Any]]: 搜索结果
    """
    try:
        if not user_name or not isinstance(user_name, str):
            return []

        filters = {"user_name__in": [user_name, SYS_USER_NAME]}

        # 或者搜索admin

        if title and isinstance(title, str):
            filters["title__icontains"] = title.strip()

        results = AiAgent.objects.order_by("-create_time").filter(**filters)

        # 添加字段后，自动转为dict
        datas = list(results)

        if len(datas) == 0:
            return []

        return [to_dict(item) for item in datas]

    except Exception as e:
        raise e


def search_ai_agent_id(id) -> dict:
    """根据主键搜索"""
    data = AiAgent.objects.get(id=id)
    return to_dict(data)


def delete_ai_agent(id) -> int:
    """根据主键删除
    @return int: 删除的行数
    """
    deleted_count, _ = AiAgent.objects.filter(id=id).delete()

    return deleted_count


def search_system_agent() -> dict:
    """获取系统智能体"""
    results = AiAgent.objects.filter(user_name=SYS_USER_NAME).order_by("create_time")
    # 添加字段后，自动转为dict
    datas = list(results)
    if len(datas) == 0:
        return []

    return [to_dict(item) for item in datas]


def to_dict(data: AiAgent) -> dict:
    if data is None:
        return {}
    content = json.loads(data.content)
    model_key = data.model_key
    user_name = data.user_name
    model_name = None
    if model_key is not None:
        model = GET_MODEL_DETAIL(model_key=model_key)
        if model is not None and len(model) > 0:
            model_name = model[0]["model_name"]
    return {
        "id": data.id,
        "title": data.title,
        "content": content,
        "model_key": data.model_key,
        "model_name": model_name,
        "temperature": float(data.temperature),
        "top_p": float(data.top_p),
        "max_tokens": data.max_tokens,
        "presence_penalty": float(data.presence_penalty),
        "frequency_penalty": float(data.frequency_penalty),
        "user_icon": data.user_icon,
        "assistant_icon": data.assistant_icon,
        "user_name": data.user_name,
        "create_time": data.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        "count": len(content),
        "model_name": model_name,
    }
