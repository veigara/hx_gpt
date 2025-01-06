import logging
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, HttpResponse
from ..utils import *

from ..service.config import get_config as GET_CONFIG, update_config as UPDATE_CONFIG

logger = logging.getLogger("chat_app")


@require_http_methods(["GET"])
def get_config(request):
    """获取项目配置文件内容"""
    try:
        return JsonResponse(GET_CONFIG(), safe=False)
    except Exception as e:
        logger.error(print_err(e))
        return HttpResponse(f"Server error occurred:{e}", status=500)


@csrf_exempt
@require_http_methods(["POST"])
def update_config(request):
    """更新项目配置文件内容"""
    try:
        payload = json.loads(request.body.decode("utf-8"))
        data = payload.get("data")

        return HttpResponse(UPDATE_CONFIG(data))
    except Exception as e:
        logger.error(print_err(e))
        return HttpResponse(f"Server error occurred:{e}", status=500)
