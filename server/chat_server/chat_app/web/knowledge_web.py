import logging
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import HttpResponse
from ..utils import *
from ..presets import *
from ..base_module.base_response import AgentResponse
from ..base_module.agent_exception import AgentException
from ..service.knowledge.knowledge_se import (
    upload_file as UPLOAD_FILE,
    search_knowledge_file as SEARCH_KNOWLEDGE_FILE,
    delete_file as DELETE_FILE,
    save_knowledge_data as SAVE_KNOWLEDGE_DATA,
    search_knowledge_data as SEARCH_KNOWLEDGE_DATA,
    update_knowledge_data as UPDATE_KNOWLEDGE_DATA,
    delete_knowledge_data as DELETE_KNOWLEDGE_DATA,
)


logger = logging.getLogger("chat_app")


@csrf_exempt
@require_http_methods(["POST"])
def upload_file(request):
    try:
        user_name = get_user_name(request)
        uploaded_file = request.FILES["file"]
        knowledge_id = request.POST.get("id")

        UPLOAD_FILE(user_name, knowledge_id, uploaded_file)
        return JsonResponse({"status": "success"})
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}上传文件失败")
        )


@require_http_methods(["GET"])
def search_file(request):
    try:
        user_name = get_user_name(request)
        knowledge_id = request.GET.get("knowledge_id")
        title = request.GET.get("title")
        if not knowledge_id:
            result = []
        else:
            result = SEARCH_KNOWLEDGE_FILE(user_name, knowledge_id, title)

        return JsonResponse(AgentResponse.success(data=result))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}搜索文件失败")
        )


@csrf_exempt
@require_http_methods(["DELETE"])
def del_file(request):
    try:
        id = request.GET.get("id")
        result = DELETE_FILE(id)

        return JsonResponse(AgentResponse.success(data=result))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}删除文件失败")
        )


@csrf_exempt
@require_http_methods(["POST"])
def save_update_knowledge(request):
    """更新/保存知识库"""
    try:
        payload = json.loads(request.body.decode("utf-8"))
        id = payload.get("id")
        know_name = payload.get("know_name")
        index_name = payload.get("index_name")
        description = payload.get("description")
        user_name = get_user_name(request)

        if not user_name or not know_name or not index_name:
            return JsonResponse(AgentResponse.fail(fail_msg="Missing required fields"))
        if not id:
            # 保存知识库
            res = SAVE_KNOWLEDGE_DATA(user_name, know_name, index_name, description)
        else:
            # 更新知识库
            res = UPDATE_KNOWLEDGE_DATA(
                id, know_name, index_name, description, user_name
            )

        return JsonResponse(AgentResponse.success(data=res))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}保存知识库失败")
        )


@require_http_methods(["GET"])
def search_knowledge(request):
    """搜索知识库"""
    try:
        user_name = get_user_name(request)
        know_name = request.GET.get("know_name")
        result = SEARCH_KNOWLEDGE_DATA(user_name, know_name)

        return JsonResponse(AgentResponse.success(data=result))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}搜索知识库失败")
        )


@csrf_exempt
@require_http_methods(["DELETE"])
def del_knowledge(request):
    try:
        id = request.GET.get("id")
        user_name = get_user_name(request)
        result = DELETE_KNOWLEDGE_DATA(user_name, id)

        return JsonResponse(AgentResponse.success(data=result))
    except AgentException as e:
        return JsonResponse(AgentResponse.fail(fail_msg=e.message))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}删除知识库失败")
        )
