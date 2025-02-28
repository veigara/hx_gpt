import logging
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, HttpResponse
from ..jwt.permissions import check_permission
from ..utils import *
from ..base_module.base_response import AgentResponse
from ..service.login import login as LOGIN, register as REGISTER

logger = logging.getLogger("chat_app")


@csrf_exempt
@require_http_methods(["POST"])
def chat_login(request):
    """登录
    params:username 用户名
    params:password 密码
    return:token
    """
    try:
        payload = json.loads(request.body.decode("utf-8"))
        username = payload.get("username")
        password = payload.get("password")
        if username is None:
            raise AgentException("PARAM_INVALID", "缺少必要参数username")
        if password is None:
            raise AgentException("PARAM_INVALID", "缺少必要参数password")
        res = LOGIN(username, password)
        return response_server_success(res)
    except Exception as e:
        return response_server_err(e, msg="登录失败")


@csrf_exempt
@require_http_methods(["POST"])
def chat_register(request):
    """注册
    params:model_name 用户名
    params:model_detail 密码
    return:用户详情
    """
    try:
        payload = json.loads(request.body.decode("utf-8"))
        username = payload.get("username")
        password = payload.get("password")
        if username is None:
            raise AgentException("PARAM_INVALID", "缺少必要参数username")
        if password is None:
            raise AgentException("PARAM_INVALID", "缺少必要参数password")
        res = REGISTER(username, password)
        return response_server_success(res)
    except Exception as e:
        return response_server_err(e, msg="注册失败")
