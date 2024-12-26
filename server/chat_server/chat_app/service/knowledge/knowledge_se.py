import os
import uuid
from ...presets import *
from ...db_models.db_knowledge_file import KnowledgeFile
from django.db import transaction
from typing import List
from ..db.knowledge_file import *
from ..db.knowledge import *
from ...base_module.agent_exception import AgentException


def upload_file(user_name, knowledge_id, file):
    """上传文件
    @param user_name: 用户名
    @param knowledge_id: 知识库id
    @param file: 文件对象
    """
    file_extension = os.path.splitext(file.name)
    title = file_extension[0]
    file_type = file_extension[1]
    id = str(uuid.uuid4()).replace("-", "")
    file_id = f"{id}{file_type}"
    file_size_mb = "{:.2f}".format(file.size / 1024 / 1024)
    # 保存文件
    file_path = os.path.join(KNOWLEDGE_UPLOAD_FILE_DIR, user_name, file_id)
    try:
        with transaction.atomic():
            # 保存文件
            save_file(file, file_path)
            # 入库
            save_knowledge_file(
                user_name,
                knowledge_id,
                file_id,
                title,
                file_type,
                file_path,
                file_size_mb,
            )

    except Exception as e:
        # 处理异常，可以记录日志或返回错误信息
        print(f"Error uploading file: {e}")
        # 文件系统中的文件会自动删除，但可以手动删除以确保一致性
        if os.path.exists(file_path):
            os.remove(file_path)
        raise e


def get_file_suffix(original_filename):
    # 提取文件后缀
    file_extension = os.path.splitext(original_filename)
    return file_extension[1]


def save_file(file, file_path):
    """保存文件
    @param file: 文件对象
    @param file_path:文件路径
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
        for chunk in file.chunks():
            f.write(chunk)


def delete_file(id):
    """删除文件
    @param id: 主键id
    """
    try:
        with transaction.atomic():
            detail = search_knowledge_file_id(id)
            if detail is None:
                return
            file_path = detail["file_path"]
            res = delete_knowledge_file(id)
            if res < 0:
                raise Exception("删除文件失败")

            # 删除文件
            os.remove(os.path.join(file_path))
    except Exception as e:
        raise e


def save_knowledge_data(user_name, know_name, index_name, description):
    """保存知识库
    @param data: 知识库对象
    """
    try:
        with transaction.atomic():
            # 保存知识库
            knowledge = Knowledge(
                user_name=user_name,
                know_name=know_name,
                index_name=index_name,
                description=description,
            )
            return save_knowledge(knowledge)
    except Exception as e:
        raise e


def update_knowledge_data(id, know_name, index_name, description, user_name):
    """更新知识库"""
    try:
        with transaction.atomic():
            # 更新知识库
            res = update_knowledge(id, know_name, index_name, description, user_name)
            if res > 0:
                return search_knowledge_id(id)
            else:
                raise AgentException("更新失败")
    except Exception as e:
        raise e


def search_knowledge_data(user_name: str, know_name: str) -> List[Dict[str, Any]]:
    """搜索知识库
    @param user_name: 用户名
    @param know_name: 知识库名称
    """
    return search_knowledge(user_name, know_name)


def delete_knowledge_data(user_name, id) -> bool:
    """删除知识库
    @param id: 主键id
    """
    try:
        with transaction.atomic():
            # 先查询知识库的文件是否都删除
            files = search_knowledge_file(user_name, id, None)
            if len(files) > 0:
                raise AgentException("请先删除知识库下的文件")
            # 删除知识库
            res = delete_knowledge(id)
            if res > 0:
                return True
            else:
                raise AgentException("删除知识库失败")

    except Exception as e:
        raise e
