import os
import uuid
import logging
import datetime
from ..presets import *
from ..db_models.db_knowledge_file import KnowledgeFile
from django.db import transaction
from typing import List
from .db.knowledge_file import *
from .db.knowledge import *
from ..utils import *
from ..base_module.agent_exception import AgentException
from .knowledge_stores import add_stores as ADD_STORES
from .knowledge_redis import (
    del_keys as REDIS_DEL_KEYS,
    search_text as REDIS_SEARCH_TEXT,
)

logger = logging.getLogger("chat_app")


def upload_file(user_name, knowledge_id, file, file_config: dict):
    """上传文件
    @param user_name: 用户名
    @param knowledge_id: 知识库id
    @param file: 文件对象
    @param file_config: 文件配置
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
            # 查询知识库基本信息
            index_name = search_knowledge_id(knowledge_id)["index_name"]
            # 保存文件
            save_file(file, file_path)
            # 保存到向量库
            doc_data = ADD_STORES(file_path, file_type, index_name, file_config, title)
            document_count = doc_data["document_count"]
            document_ids = doc_data["document_ids"]
            # 入库
            save_knowledge_file(
                user_name,
                knowledge_id,
                file_id,
                title,
                file_type,
                file_path,
                file_size_mb,
                document_ids,
                document_count,
                index_name,
            )
            logger.info(f"{user_name}上传文件成功")
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
            # 删除向量数据
            ids = detail["file_index_ids"]
            index_name = detail["file_index_name"]
            if ids is not None:
                ids = ids.split(",")
                REDIS_DEL_KEYS(index_name, ids)
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


def knowledge_retrieve(know_id, input) -> str:
    """知识库检索
    @param know_id: 知识库id
    @param input: 用户输入
    @return: 返回知识库检索结果pronmpt
    """
    try:
        # 查询知识库基本信息
        detail = search_knowledge_id(know_id)
        if detail is None:
            raise AgentException("知识库不存在")
        # 查询知识库文件
        index_name = detail["index_name"]

        list = REDIS_SEARCH_TEXT(index_name, input)
        # 直接返回结果
        if list is not None:
            list = [item["content"] for item in list]
        else:
            return None

        # reference_results = add_source_numbers(list, use_source=False)
        today = datetime.today().strftime("%Y-%m-%d")
        real_input = (
            KNOWLEDGE_PROMPT_TEMPLATE.replace("{current_date}", today)
            .replace("{query_str}", input)
            .replace("{context_str}", "\n\n".join(list))
        )

        return real_input
    except Exception as e:
        logger.error(f"知识库检索失败: {e}")
        raise AgentException("知识库检索失败")
