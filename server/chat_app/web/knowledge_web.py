import logging
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import StreamingHttpResponse
from ..utils import *
from ..presets import *
from ..base_module.base_response import AgentResponse
from ..base_module.agent_exception import AgentException
from ..service.knowledge_se import (
    upload_file as UPLOAD_FILE,
    search_knowledge_file as SEARCH_KNOWLEDGE_FILE,
    delete_file as DELETE_FILE,
    save_knowledge_data as SAVE_KNOWLEDGE_DATA,
    search_knowledge_data as SEARCH_KNOWLEDGE_DATA,
    update_knowledge_data as UPDATE_KNOWLEDGE_DATA,
    delete_knowledge_data as DELETE_KNOWLEDGE_DATA,
    knowledge_retrieve as KNOWLEDGE_RETRIEVE,
    down_file as DOWN_FILE,
)
from ..models.model import get_model

logger = logging.getLogger("chat_app")


@csrf_exempt
@require_http_methods(["POST"])
def upload_file(request):
    try:
        user_name = get_user_name(request)
        uploaded_file = request.FILES["file"]
        knowledge_id = request.POST.get("id")
        #  文件配置
        file_config = request.POST.get("file_config")
        file_config = json.loads(file_config) if file_config else {}
        UPLOAD_FILE(user_name, knowledge_id, uploaded_file, file_config)
        return JsonResponse(AgentResponse.success(data={"status": "success"}))
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


@csrf_exempt
@require_http_methods(["POST"])
def knowledge_retrieve(request):
    """检索知识库"""
    try:
        payload = json.loads(request.body.decode("utf-8"))
        model_name = payload.get("model_name")
        know_id = payload.get("know_id")
        search_text = payload.get("search_text")

        if not model_name or not know_id or not search_text:
            raise AgentException("检索失败,请选择模型和知识库")
        user_name = get_user_name(request)
        model = get_model(
            model_key=model_name,
            user_name=user_name,
        )
        # 知识库检索
        real_input = KNOWLEDGE_RETRIEVE(know_id=know_id, input=search_text)
        if not real_input:
            raise AgentException("暂未检索到知识库内容")

        answer = model.get_answer_chatbot_at_once(real_input)
        return answer
    except AgentException as e:
        return StreamingHttpResponse(
            error_stream(e.message), status=500, content_type="application/json"
        )
    except Exception as e:
        logger.error(print_err(e))
        # 返回500错误和错误信息
        fail_msg = f"{STANDARD_ERROR_MSG}检索失败,{e}"

        return StreamingHttpResponse(
            error_stream(fail_msg), status=500, content_type="application/json"
        )


def error_stream(fail_msg):
    yield json.dumps({"error": str(fail_msg)}).encode("utf-8")
    yield b"\n"  # 可以在这里添加额外的信息或格式化输出


@require_http_methods(["GET"])
def down_knowledge_file(request):
    """下载知识库文件"""
    try:
        id = request.GET.get("id")
        response = DOWN_FILE(id)
        return response
    except AgentException as e:
        return JsonResponse(AgentResponse.fail(fail_msg=e.message))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}下载知识库文件失败")
        )
