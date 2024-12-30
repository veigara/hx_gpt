from ...db_models.db_knowledge_file import KnowledgeFile
from typing import List


def save_knowledge_file(
    user_name,
    knowledge_id,
    file_id,
    title,
    file_type,
    file_path,
    file_size,
    file_index_ids: str,
    docment_count,
    index_name,
):
    """保存文件信息
    @param user_name: 用户名
    @param knowledge_id: 知识库id
    @param file_id: 文件id
    @param title: 文件名
    @param file_type: 文件类型
    @param file_path: 文件路径
    @param file_size: 文件大小
    @param file_index_ids: 向量库索引ID
    @param docment_count: 文档数量
    @param index_name: 向量库索引名
    """

    table = KnowledgeFile(
        knowledge_id=knowledge_id,
        file_id=file_id,
        file_path=file_path,
        file_type=file_type,
        file_size=file_size,
        title=title,
        file_index_ids=file_index_ids,
        file_index_name=index_name,
        user_name=user_name,
        docment_count=docment_count,
    )

    table.save()


def search_knowledge_file(user_name, knowledge_id, title) -> List:
    """根据知识库ID搜索知识库文件内容

    Args:
        query (str): 搜索内容
        user_name (str): 用户名
        knowledge_id (str): 知识库ID

    Returns:
        list: 搜索结果
    """
    filter = {"user_name": user_name, "knowledge_id": knowledge_id}
    if title is not None:
        filter["title__icontains"] = title

    results = (
        KnowledgeFile.objects.values(
            "id",
            "title",
            "file_type",
            "file_size",
            "file_index_name",
            "docment_count",
            "create_time",
        )
        .order_by("-create_time")
        .filter(**filter)
    )
    # 添加字段后，自动转为dict
    datas = list(results)

    return datas


def search_knowledge_file_id(id) -> dict:
    """根据主键搜索"""
    data = KnowledgeFile.objects.get(id=id)
    return to_dict(data)


def delete_knowledge_file(id):
    """根据主键删除"""
    deleted_count, _ = KnowledgeFile.objects.filter(id=id).delete()
    return deleted_count


def to_dict(data: KnowledgeFile) -> dict:
    if data is None:
        return {}
    return {
        "id": data.id,
        "knowledge_id": data.knowledge_id,
        "title": data.title,
        "file_id": data.file_id,
        "file_type": data.file_type,
        "file_path": data.file_path,
        "file_index_name": data.file_index_name,
        "file_index_ids": data.file_index_ids,
        "docment_count": data.docment_count,
        "create_time": data.create_time,
        "update_time": data.update_time,
        "user_name": data.user_name,
    }
