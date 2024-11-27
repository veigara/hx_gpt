# -*- coding:utf-8 -*-
import tiktoken

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
    user_name = request.headers.get('authorization')
    return user_name or ""
        
    