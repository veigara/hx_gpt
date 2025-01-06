import logging
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, HttpResponse
from ..utils import *
from ..base_module.base_response import AgentResponse
from ..service.ai_model import (
    get_model_type as GET_MODEL_TYPE,
    get_all_models as GET_ALL_MODELS,
    get_model_detail as GET_MODEL_DETAIL,
    update_model_detail as UPDATE_MODEL_DETAIL,
    remove_model as REMOVE_MODEL,
    save_model as SAVE_MODEL,
)

logger = logging.getLogger("chat_app")


# 获取模型类别
@require_http_methods(["GET"])
def get_all_model_type(request):
    try:
        return JsonResponse(AgentResponse.success(data=GET_MODEL_TYPE()))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}获取模型类别失败")
        )


# 获取所有的模型
@require_http_methods(["GET"])
def get_all_models(request):
    try:
        keyword = request.GET.get("keyword")
        user_name = get_user_name(request)
        return JsonResponse(
            AgentResponse.success(data=GET_ALL_MODELS(user_name, keyword))
        )
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}获取所有的模型失败")
        )


@require_http_methods(["GET"])
def get_model_detail(request):
    """获取模型详情
    params:model_key 模型名称
    return:模型详情
    """
    try:
        user_name = get_user_name(request)
        model_key = request.GET.get("model_key")
        return JsonResponse(
            AgentResponse.success(data=GET_MODEL_DETAIL(user_name, model_key))
        )
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}获取模型详情失败")
        )


@csrf_exempt
@require_http_methods(["POST"])
def update_model_detail(request):
    """更新模型详情
    params:model_name 模型名称
    params:model_detail 模型详情
    return:模型详情
    """
    try:
        user_name = get_user_name(request)
        payload = json.loads(request.body.decode("utf-8"))
        data = payload.get("data")
        if data is None:
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}模型数据不能为空")
            )
        UPDATE_MODEL_DETAIL(user_name, data)
        return JsonResponse(AgentResponse.success(data=data))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}模型操作失败")
        )


@csrf_exempt
@require_http_methods(["POST"])
def add_model(request):
    """添加模型
    params:model_name 模型名称
    params:model_detail 模型详情
    return:模型详情
    """
    try:
        user_name = get_user_name(request)
        payload = json.loads(request.body.decode("utf-8"))
        data = payload.get("data")
        if data is None:
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}模型数据不能为空")
            )
        data = SAVE_MODEL(user_name, data)
        return JsonResponse(AgentResponse.success(data=data))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}添加模型失败")
        )


@csrf_exempt
@require_http_methods(["DELETE"])
def remove_model(request):
    """删除模型
    params:model_name 模型名称
    return:模型详情
    """
    try:
        id = request.GET.get("id")
        REMOVE_MODEL(id)
        return JsonResponse(AgentResponse.success(data={"id": id}))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}删除模型失败")
        )
