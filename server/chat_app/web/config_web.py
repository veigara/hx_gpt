import logging
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, HttpResponse
from ..utils import *
from ..jwt.permissions import check_permission
from ..service.config import get_config as GET_CONFIG, update_config as UPDATE_CONFIG

logger = logging.getLogger("chat_app")


@require_http_methods(["GET"])
@check_permission
def get_config(request):
    """获取项目配置文件内容"""
    try:
        return response_server_success(GET_CONFIG())
    except Exception as e:
        return response_server_err(e, msg="获取项目配置文件失败")


@csrf_exempt
@require_http_methods(["POST"])
@check_permission
def update_config(request):
    """更新项目配置文件内容"""
    try:
        payload = json.loads(request.body.decode("utf-8"))
        data = payload.get("data")

        return response_server_success(UPDATE_CONFIG(data))
    except Exception as e:
        return response_server_err(e, msg="更新项目配置文件失败")
