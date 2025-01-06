# -*- coding:utf-8 -*-
import tiktoken
import traceback
from .presets import *


def construct_text(role, text):
    return {"role": role, "content": text}


def construct_user(text):
    return construct_text("user", text)


def construct_image(path):
    return construct_text("image", path)


def construct_system(text):
    return construct_text("system", text)


def construct_assistant(text):
    return construct_text("assistant", text)


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
