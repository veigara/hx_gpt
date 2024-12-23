import os
import uuid
import datetime
import json
from ..presets import *


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
    # 保存文件
    save_file(file, user_name, file_id)
    # 保存文件信息
    save_file_data(user_name, knowledge_id, file_id, title, file_type)


def get_file_suffix(original_filename):
    # 提取文件后缀
    file_extension = os.path.splitext(original_filename)
    return file_extension[1]


def save_file(file, user_name, file_id):
    """保存文件
    @param file: 文件对象
    @param user_name: 用户名
    @param file_id: 文件id
    """
    file_path = os.path.join(KNOWLEDGE_UPLOAD_FILE_DIR, user_name, file_id)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
        for chunk in file.chunks():
            f.write(chunk)


def save_file_data(user_name, knowledge_id, file_id, title, file_type):
    """保存文件信息
    @param user_name: 用户名
    @param knowledge_id: 知识库id
    @param file_id: 文件id
    @param title: 文件名
    @param file_type: 文件类型
    """
    file_data = {
        "knowledge_id": knowledge_id,
        "file_id": file_id,
        "title": title,
        "file_type": file_type,
        "create_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    file_path = os.path.join(
        KNOWLEDGE_RECORD_FILE_DIR, user_name, f"{knowledge_id}.json"
    )
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(file_data, f, ensure_ascii=False)
