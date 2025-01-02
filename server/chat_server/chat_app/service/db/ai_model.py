from ...db_models.db_model import AiModel
from typing import List, Dict, Any
from datetime import datetime


def save_ai_model(
    model_key,
    model_name,
    description,
    model_type,
    multimodal,
    max_content_len,
    user_name,
):
    """保存模型基本信息"""
    data = AiModel(
        model_key=model_key,
        model_name=model_name,
        description=description,
        model_type=model_type,
        multimodal=multimodal,
        max_content_len=max_content_len,
        user_name=user_name,
    )
    data.save()
    return to_dict(data)


def update_ai_model(
    id,
    model_key,
    model_name,
    description,
    model_type,
    multimodal,
    max_content_len,
    user_name,
):
    """更新模型基本信息"""
    res = AiModel.objects.filter(id=id).update(
        model_key=model_key,
        model_name=model_name,
        description=description,
        model_type=model_type,
        multimodal=multimodal,
        max_content_len=max_content_len,
        user_name=user_name,
        update_time=datetime.now(),
    )

    return res


def search_ai_model(
    user_name: str, model_name: str = None, model_key=None
) -> List[Dict[str, Any]]:
    """根据模型名称搜索模型基本信息

    Args:
        user_name (str): 用户名
        know_name (str): 模型名称

    Returns:
        List[Dict[str, Any]]: 搜索结果
    """
    try:
        if not user_name or not isinstance(user_name, str):
            return []

        filters = {"user_name": user_name}
        if model_name and isinstance(model_name, str):
            filters["model_name__icontains"] = model_name.strip()

        if model_key and isinstance(model_key, str):
            filters["model_key__icontains"] = model_key.strip()

        results = (
            AiModel.objects.values(
                "id",
                "model_key",
                "model_name",
                "description",
                "model_type",
                "multimodal",
                "max_content_len",
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


def search_ai_model_id(id) -> dict:
    """根据主键搜索"""
    data = AiModel.objects.get(id=id)
    return to_dict(data)


def delete_ai_model(id):
    """根据主键删除
    @return int: 删除的行数
    """
    deleted_count, _ = AiModel.objects.filter(id=id).delete()

    return deleted_count


def to_dict(data: AiModel) -> dict:
    if data is None:
        return {}
    return {
        "id": data.id,
        "model_key": data.model_key,
        "model_name": data.model_name,
        "description": data.description,
        "model_type": data.model_type,
        "multimodal": data.multimodal,
        "max_content_len": data.max_content_len,
        "create_time": data.create_time,
        "update_time": data.update_time,
        "user_name": data.user_name,
    }
