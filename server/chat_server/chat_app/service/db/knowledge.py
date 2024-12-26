from ...db_models.db_knowledge import Knowledge
from typing import List, Dict, Any
from datetime import datetime


def save_knowledge(data: Knowledge):
    """保存知识库基本信息
    @param user_name: 用户名
    @param know_name: 知识库名称
    @param index_name: 索引名称
    @param description: 描述
    """

    data.save()
    return to_dict(data)


def update_knowledge(id, know_name, index_name, description, user_name):
    """更新知识库基本信息
    @param user_name: 用户名
    @param know_name: 知识库名称
    @param index_name: 索引名称
    @param description: 描述
    """
    res = Knowledge.objects.filter(id=id).update(
        know_name=know_name,
        index_name=index_name,
        description=description,
        user_name=user_name,
        update_time=datetime.now(),
    )

    return res


def search_knowledge(user_name: str, know_name: str) -> List[Dict[str, Any]]:
    """根据知识库名称搜索知识库基本信息

    Args:
        user_name (str): 用户名
        know_name (str): 知识库名称

    Returns:
        List[Dict[str, Any]]: 搜索结果
    """
    try:
        if not user_name or not isinstance(user_name, str):
            return []

        filters = {"user_name": user_name}
        if know_name and isinstance(know_name, str):
            filters["know_name__icontains"] = know_name.strip()

        results = (
            Knowledge.objects.values(
                "id",
                "know_name",
                "index_name",
                "description",
                "create_time",
                "update_time",
                "user_name",
            )
            .order_by("-create_time")
            .filter(**filters)
        )

        # 添加字段后，自动转为dict
        datas = list(results)

        return datas

    except Exception as e:
        raise e


def search_knowledge_id(id) -> dict:
    """根据主键搜索"""
    data = Knowledge.objects.get(id=id)
    return to_dict(data)


def delete_knowledge(id):
    """根据主键删除
    @return int: 删除的行数
    """
    deleted_count, _ = Knowledge.objects.filter(id=id).delete()

    return deleted_count


def to_dict(data: Knowledge) -> dict:
    if data is None:
        return {}
    return {
        "id": data.id,
        "know_name": data.know_name,
        "index_name": data.index_name,
        "description": data.description,
        "create_time": data.create_time,
        "update_time": data.update_time,
        "user_name": data.user_name,
    }
