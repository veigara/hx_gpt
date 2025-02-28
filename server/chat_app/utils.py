# -*- coding:utf-8 -*-
import tiktoken
import traceback
import logging
from .presets import *
import base64
from urllib.parse import urljoin
from langchain.docstore.document import Document
from typing import List
from django.http import JsonResponse
from .base_module.base_response import AgentResponse

logger = logging.getLogger("chat_app")


def construct_text(role, text):
    return {"role": role, "content": text}


def construct_image_url(role, image_path, text):
    image_64 = get_image_base64(image_path)
    return {
        "role": role,
        "content": [
            {"type": "text", "text": text},
            {"type": "image_url", "image_url": {"url": image_64}},
        ],
    }


def construct_user(text):
    return construct_text("user", text)


def construct_user_image(image_path, text):
    return construct_image_url("user", image_path, text)


def construct_image(path):
    return construct_text("image_url", path)


def construct_system(text):
    return construct_text("system", text)


def construct_assistant(text):
    return construct_text("assistant", text)


def construct_file(file_name, file_path):
    """增加一个文件名称的内容"""
    return {"type": "file", "file": file_name, "file_path": file_path}


def count_token(input_str):
    encoding = tiktoken.get_encoding("cl100k_base")
    length = len(encoding.encode(input_str))
    return length


# 从请求头中中获取用户名
def get_user_name(request) -> str:
    user_name = request.user.username
    return user_name or ""


def count_token(input_str):
    """计算输入字符串的token数"""
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(input_str)
    return len(tokens)


def print_err(error: Exception) -> str:
    # 打印详细的错误信息和堆栈跟踪
    error_message = f"{STANDARD_ERROR_MSG}:"
    stack_trace = traceback.format_exc()
    return f"{error_message} {stack_trace}"


def add_source_numbers(lst, source_name="Source", use_source=True):
    if use_source:
        return [
            f'[{idx+1}]\t "{item[0]}"\n{source_name}: {item[1]}'
            for idx, item in enumerate(lst)
        ]
    else:
        return [f'[{idx+1}]\t "{item}"' for idx, item in enumerate(lst)]


def get_image_base64(path):
    """
    将本地图片文件转换为 base64 格式的 URL。

    Args:
        path (str): 本地图片文件路径。

    Returns:
        str: base64 格式的图片 URL。
    """
    # 读取图片文件
    with open(path, "rb") as image_file:
        # 将图片文件转换为 base64 格式
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

        # 构造 base64 格式的图片 URL
        image_url = f"data:image/{get_image_type(path)};base64,{image_base64}"

        return image_url


def get_image_type(path):
    """
    获取图片文件类型。

    Args:
        path (str): 本地图片文件路径。

    Returns:
        str: 图片文件类型（如：jpg、png、gif 等）。
    """
    # 获取文件后缀
    file_suffix = path.split(".")[-1].lower()

    # 根据文件后缀判断图片类型
    if file_suffix in ["jpg", "jpeg"]:
        return "jpeg"
    elif file_suffix == "png":
        return "png"
    elif file_suffix == "gif":
        return "gif"
    else:
        raise ValueError(f"不支持的图片类型：{file_suffix}")


def get_file_type(path):
    # 获取文件后缀
    file_suffix = path.split(".")[-1].lower()
    return file_suffix


def is_file_image(path):
    # 判断是不是图片
    file_suffix = get_file_type(path)
    if file_suffix in ["jpg", "jpeg", "png", "gif"]:
        return True
    else:
        return False


def covert_document_to_text(documents: List[Document]) -> str:
    """
    将Document列表转换为文本
    """
    texts = []
    for doc in documents:
        texts.append(doc.page_content)
    return "".join(texts)


def response_server_err(e: Exception, msg: str) -> JsonResponse:
    """构建错误信息返回
    @e: 异常信息
    @msg: 错误信息
    """
    logger.error(print_err(e))
    return JsonResponse(
        AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}{str}"),
        status=500,
        json_dumps_params={"ensure_ascii": False},  # 禁用 ASCII 转义
        content_type="application/json; charset=utf-8",  # 明确指定编码
    )


# 在 base_module/agent_exception.py 中定义错误类型
class ErrorCode:
    """错误码与状态码映射类"""

    _ERROR_MAP = {
        # 错误类型               (状态码, 错误信息)
        "PARAM_INVALID": (400, "请求参数无效"),
        "AUTH_FAILED": (401, "认证失败"),
        "PERMISSION_DENIED": (403, "权限不足"),
        "RESOURCE_NOT_FOUND": (404, "资源不存在"),
        "INTERNAL_ERROR": (500, "服务器内部错误"),
        "THIRD_PARTY_ERROR": (503, "服务暂不可用"),
    }

    @classmethod
    def get_status_info(cls, error_code: str) -> tuple:
        """获取错误码对应的状态信息"""
        return cls._ERROR_MAP.get(error_code, (500, "未知错误"))


# 修改 AgentException 类携带错误码
class AgentException(Exception):
    """业务异常基类"""

    def __init__(self, error_code: str, detail: str = ""):
        self.error_code = error_code
        self.detail = detail
        status, message = ErrorCode.get_status_info(error_code)
        self.status_code = status
        self.message = f"{message}：{detail}" if detail else message
        super().__init__(self.message)


# 修改 utils.py 中的错误处理函数
def response_server_err(e: Exception | AgentException, msg: str = "") -> JsonResponse:
    """统一错误响应处理"""
    # 记录日志
    logger.error(f"{msg} 错误详情：{print_err(e)}")

    # 处理自定义异常
    if isinstance(e, AgentException):
        status_code = e.status_code
        error_msg = f"{STANDARD_ERROR_MSG}{e.message}"
    # 处理系统内置异常
    else:
        status_code = 500
        error_msg = f"{STANDARD_ERROR_MSG}：系统异常:{msg} 错误详情：{str(e)}"

    return JsonResponse(
        AgentResponse.fail(fail_msg=error_msg),
        status=status_code,
        json_dumps_params={"ensure_ascii": False},
        content_type="application/json; charset=utf-8",
    )


def response_server_success(data: object):
    """成功响应"""
    return JsonResponse(
        AgentResponse.success(data=data),
        status=200,
        json_dumps_params={"ensure_ascii": False},
        content_type="application/json; charset=utf-8",
    )
