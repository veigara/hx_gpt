import os
import logging
import uuid
from ..presets import *
from django.http import FileResponse
from django.utils.encoding import escape_uri_path
from ..base_module.agent_exception import AgentException
from ..config import get_default_model_params
from ..utils import *
from ..service.knowledge_stores import parse_file as PARSE_FILE

logger = logging.getLogger("chat_app")


def upload_file(user_name, file) -> dict:
    """上传文件
    @param user_name: 用户名
    @param knowledge_id: 知识库id
    @param file: 文件对象
    @param file_config: 文件配置
    @return: file_path 文件地址
    """
    file_extension = os.path.splitext(file.name)
    title = file_extension[0]
    file_type = file_extension[1]
    id = str(uuid.uuid4()).replace("-", "")
    file_id = f"{id}{file_type}"
    # 保存文件
    file_path = os.path.join(CHAT_UPLOAD_FILE_DIR, user_name, file_id)
    save_file(file, file_path)

    return {"file_path": file_path, "file_name": file.name}


def save_file(file, file_path) -> str:
    """保存文件
    @param file: 文件对象
    @param file_path:文件路径
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
        for chunk in file.chunks():
            f.write(chunk)


def down_file(file_name, file_path) -> FileResponse:
    """下载文件
    @param id: 主键id
    """
    try:
        # 读取文件内容
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, "rb"))
            response["Content-Type"] = "application/octet-stream"
            # 文件名为中文时无法识别，使用escape_uri_path处理
            response["Content-Disposition"] = (
                "attachment; " "filename*=UTF-8''{}".format(escape_uri_path(file_name))
            )
            return response
        else:
            raise AgentException("文件路径不存在")
    except Exception as e:
        logger.error("文件下载时发生错误", e)
        raise AgentException("文件下载失败")


def parse_file_to_text(user_name, file_path, file_name, model_key) -> dict:
    """
    解析文件
    @param user_name: 用户名
    @param file_path: 文件路径
    @param model_key: 模型key
    @return 文件内容的id
    """
    try:
        # 查找模型是不是视觉模型
        config = get_default_model_params(user_name, model_key)
        # 视觉模型
        model_multimodal = config["multimodal"]
        # 判断是不是图片
        imag_flag = is_file_image(file_path)
        if model_multimodal == True and imag_flag == True:
            # 是视觉模型模型,且为图片，不做解析
            return {"parse": False, "multimodal": True}
        file_type = get_file_type(file_path)
        file_config = {
            "max_length": 750,
            "overlap_length": 150,
            "text_splitter": "2",
            "char_separators": "/n/n",
            "recursive_separators": "/n/n,/n, ,",
        }
        documents = PARSE_FILE(file_path, "." + file_type, file_config, file_name)
        text = covert_document_to_text(documents)

        file_id = uuid.uuid4().hex
        parse_file_name = f"{file_id}.txt"
        user_dir = os.path.join(CHAT_PARSE_FILE_DIR, user_name)
        target_path = os.path.join(user_dir, parse_file_name)
        os.makedirs(user_dir, exist_ok=True)
        # 写入文件内容
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(text)

        return {"parse": True, "file_name": parse_file_name}
    except Exception as e:
        # 可根据实际需求添加日志记录
        logger.error("文件解析失败", e)
        raise AgentException({"parse": False, "error_msg": f"文件解析失败:{str(e)}"})
