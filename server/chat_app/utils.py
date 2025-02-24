# -*- coding:utf-8 -*-
import tiktoken
import traceback
from .presets import *
import base64
from urllib.parse import urljoin
from langchain.docstore.document import Document
from typing import List


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
    user_name = request.headers.get("authorization")
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
