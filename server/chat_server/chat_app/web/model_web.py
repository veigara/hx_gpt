import logging
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, HttpResponse
from ..utils import *
from ..service.ai_model import (
    get_model_type as GET_MODEL_TYPE,
    get_all_models as GET_ALL_MODELS,
    get_model_detail as GET_MODEL_DETAIL,
    update_model_detail as UPDATE_MODEL_DETAIL,
    remove_model as REMOVE_MODEL,
)

logger = logging.getLogger("chat_app")


# 获取模型类别
@require_http_methods(["GET"])
def get_all_model_type(request):
    try:
        return JsonResponse(GET_MODEL_TYPE(), safe=False)
    except Exception as e:
        logger.error(print_err(e))
        return HttpResponse(f"Server error occurred:{e}", status=500)


# 获取所有的模型
@require_http_methods(["GET"])
def get_all_models(request):
    try:
        keyword = request.GET.get("keyword")
        return JsonResponse(GET_ALL_MODELS(keyword), safe=False)
    except Exception as e:
        logger.error(print_err(e))
        return HttpResponse(f"Server error occurred:{e}", status=500)


@require_http_methods(["GET"])
def get_model_detail(request):
    """获取模型详情
    params:model_name 模型名称
    return:模型详情
    """
    try:
        model_name = request.GET.get("model_name")
        return JsonResponse(GET_MODEL_DETAIL(model_name), safe=False)
    except Exception as e:
        logger.error(print_err(e))
        return HttpResponse(f"Server error occurred:{e}", status=500)


@csrf_exempt
@require_http_methods(["POST"])
def update_model_detail(request):
    """更新模型详情
    params:model_name 模型名称
    params:model_detail 模型详情
    return:模型详情
    """
    try:
        payload = json.loads(request.body.decode("utf-8"))
        model_key = payload.get("model_key")
        data = payload.get("data")
        return HttpResponse(UPDATE_MODEL_DETAIL(model_key, data))
    except Exception as e:
        logger.error(print_err(e))
        return HttpResponse(f"Server error occurred:{e}", status=500)


@csrf_exempt
@require_http_methods(["POST"])
def add_model(request):
    """添加模型
    params:model_name 模型名称
    params:model_detail 模型详情
    return:模型详情
    """
    return update_model_detail(request)


@csrf_exempt
@require_http_methods(["DELETE"])
def remove_model(request):
    """删除模型
    params:model_name 模型名称
    return:模型详情
    """
    try:
        model_key = request.GET.get("model_key")
        return HttpResponse(REMOVE_MODEL(model_key))
    except Exception as e:
        logger.error(print_err(e))
        return HttpResponse(f"Server error occurred:{e}", status=500)
