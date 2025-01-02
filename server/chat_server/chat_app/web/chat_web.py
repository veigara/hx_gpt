import requests
from ..models.model import get_model
from ..config import get_default_model_name
from ..utils import *
from ..presets import *
from ..models.base_model import *
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import logging
from django.views.decorators.csrf import csrf_exempt
from ..base_module.base_response import AgentResponse
from ..base_module.agent_exception import AgentException
import json
from ..service.agent import *
from ..service.history import *
from ..cache_utils import *
from ..service.knowledge_se import (
    knowledge_retrieve as KNOWLEDGE_RETRIEVE,
)
from ..service.ai_model import get_all_models as GET_ALL_MODELS

logger = logging.getLogger("chat_app")


# 发送对话 chat
@csrf_exempt
@require_http_methods(["POST"])
def chat_with_model(request):
    try:
        # 从 POST 请求的查询参数中获取 input_text
        payload = json.loads(request.body.decode("utf-8"))
        input_text = payload.get("input_text")
        model_key = payload.get("model_key")
        history_id = payload.get("history_id")
        agent_id = payload.get("agent_id")
        # 知识库
        know_id = payload.get("know_id")
        # 连续对话
        convOff = payload.get("conv_off", True)
        # 在线搜索
        online_search = payload.get("online_search", False)
        user_name = get_user_name(request)
        if input_text is None:
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}输入内容不能为空")
            )
        if model_key is None:
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}请选择模型")
            )
        if history_id is None or history_id == "":
            # 没有选择智能体，要创建一个默认的
            history_id = cretate_new_history(user_name, model_key, input_text)
            agent_data = get_default_agent_data(user_name)
            agent_id = agent_data.get("id")
        model = get_model(
            model_key=model_key,
            user_name=user_name,
            history_id=history_id,
            agent_id=agent_id,
        )

        if model is None:
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}加载{model_key}失败")
            )
        else:
            if know_id:
                # 知识库(优先)
                res = KNOWLEDGE_RETRIEVE(know_id=know_id, input=input_text)
                if res:
                    # 搜索到后直接返回结果
                    input_text = res
            if online_search:
                # 在线搜索
                input_text = model.online_search(input_text)

            if convOff:
                # 连续对话
                response = model.stream_next_chatbot(input_text, history_id)
            else:
                response = model.get_answer_chatbot_at_once(input_text)

            return JsonResponse(AgentResponse.success(data=response))
    except requests.exceptions.ConnectTimeout:
        status_text = STANDARD_ERROR_MSG + CONNECTION_TIMEOUT_MSG + ERROR_RETRIEVE_MSG
        return AgentResponse.fail(fail_msg=status_text)
    except requests.exceptions.ReadTimeout:
        status_text = STANDARD_ERROR_MSG + READ_TIMEOUT_MSG + ERROR_RETRIEVE_MSG
        return AgentResponse.fail(fail_msg=status_text)
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}对话失败")
        )


# 获取所有的模型
@require_http_methods(["GET"])
def get_all_models(request):
    try:
        user_name = get_user_name(request)
        default_model_name = get_default_model_name()
        models = GET_ALL_MODELS(user_name)
        if models is not None:
            for model in models:
                if model.get("model_key") == default_model_name:
                    model["default"] = True

        return JsonResponse(AgentResponse.success(data=models))

    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}获取所有的模型失败")
        )


# 保存智能体文件
@csrf_exempt
@require_http_methods(["POST"])
def save_agent_file(request):
    payload = json.loads(request.body.decode("utf-8"))
    agent_data = payload.get("agent_data")
    user_name = get_user_name(request)
    try:
        save_agent(user_name, agent_data)
        return HttpResponse("Agent file saved successfully")
    except Exception as e:
        logger.error(print_err(e))
        return HttpResponse(f"Server error occurred: {e}", status=500)


# 获取所有的智能体
@require_http_methods(["GET"])
def get_user_agent(request):
    try:
        user_name = get_user_name(request)
        keyword = request.GET.get("keyword")
        agnets = get_user_all_agents(user_name, keyword)
        return HttpResponse(json.dumps(agnets), content_type="application/json")
    except Exception as e:
        logger.error(print_err(e))
        return HttpResponse(f"Server error occurred: {e}", status=500)


# 获取智能体详情
@require_http_methods(["GET"])
def get_agent_detail(request):
    try:
        id = request.GET.get("id")
        # 用户
        user_name = get_user_name(request)
        if id is None:
            return HttpResponse("id is required", status=500)
        detail = load_agent(user_name, id)
        return HttpResponse(json.dumps(detail), content_type="application/json")
    except Exception as e:
        logger.error(print_err(e))
        return HttpResponse(f"Server error occurred: {e}", status=500)


# 删除智能体
@csrf_exempt
@require_http_methods(["DELETE"])
def get_del_agent(request):
    try:
        id = request.GET.get("id")
        user_name = get_user_name(request)
        if id is None:
            return HttpResponse("id is required", status=500)
        del_agent(user_name, id)
        return HttpResponse(True)
    except Exception as e:
        logger.error(print_err(e))
        return HttpResponse(f"Server error occurred: {e}", status=500)


@require_http_methods(["GET"])
def select_agent(request) -> str:
    """选择智能体
     params:id 智能体id
     params:fileUserName 智能体文件用户
    return: 聊天记录id
    """
    try:
        id = request.GET.get("id")
        user_name = get_user_name(request)
        if id is None:
            return HttpResponse("id is required", status=500)
        agent_data = load_agent(user_name, id)
        if agent_data is None:
            return HttpResponse("智能体内容不存在", status=500)
        # 创建聊天记录
        history_id = save_history_agent(user_name, agent_data)

        return HttpResponse(history_id)

    except Exception as e:
        logger.error(print_err(e))
        return HttpResponse(f"Server error occurred: {e}", status=500)


@require_http_methods(["GET"])
def get_historys(request):
    """获取用户的聊天记录
    params:keyword 关键字
    return:聊天记录列表
    """
    try:
        user_name = get_user_name(request)
        keyword = request.GET.get("keyword")
        return HttpResponse(
            json.dumps(get_user_all_history(user_name, keyword)),
            content_type="application/json",
        )
    except Exception as e:
        logger.error(print_err(e))
        return HttpResponse(f"Server error occurred: {e}", status=500)


@require_http_methods(["GET"])
def get_history_detail(request):
    """获取聊天记录详情
    params:id 聊天记录id
    return:聊天记录详情
    """
    try:
        id = request.GET.get("id")
        user_name = get_user_name(request)
        if id is None:
            return HttpResponse("id is required", status=500)
        detail = load_history(user_name, id)
        # 将聊天记录加载到上下文中
        clear_history_global(user_name)
        set_history_global(user_name, detail.get("content", []))
        return HttpResponse(json.dumps(detail), content_type="application/json")
    except Exception as e:
        logger.error(print_err(e))
        return HttpResponse(f"Server error occurred: {e}", status=500)


@require_http_methods(["DELETE"])
@csrf_exempt
def del_user_history(request):
    """删除聊天记录
    params:id 聊天记录id
    return:删除结果
    """
    try:
        id = request.GET.get("id")
        user_name = get_user_name(request)
        if id is None:
            return HttpResponse("id is required", status=500)
        del_history(user_name, id)
        return HttpResponse(True)
    except Exception as e:
        logger.error(print_err(e))


@csrf_exempt
@require_http_methods(["POST"])
def rename_user_history(request):
    """重命名聊天记录
    params:id 聊天记录id
    params:new_title 新标题
    return:重命名结果
    """
    try:
        payload = json.loads(request.body.decode("utf-8"))
        id = payload.get("id")
        new_title = payload.get("new_title")
        user_name = get_user_name(request)
        if id is None:
            return HttpResponse("id is required", status=500)
        if new_title is None:
            return HttpResponse("new_title is required", status=500)
        rename_history(user_name, id, new_title)
        return HttpResponse(True)
    except Exception as e:
        logger.error(print_err(e))
        return HttpResponse(f"Server error occurred: {e}", status=500)


@csrf_exempt
@require_http_methods(["POST"])
def top_user_history(request):
    """置顶聊天记录
    params:id 聊天记录id
    return:置顶结果
    """
    try:
        payload = json.loads(request.body.decode("utf-8"))
        id = payload.get("id")
        user_name = get_user_name(request)
        if id is None:
            return HttpResponse("id is required", status=500)
        top_history(user_name, id)
        return HttpResponse(True)
    except Exception as e:
        logger.error(print_err(e))
        return HttpResponse(f"Server error occurred: {e}", status=500)


@csrf_exempt
@require_http_methods(["POST"])
def clear_history_context(request):
    """清空上下文
    params:history_id 聊天记录id
    return:
    """
    try:
        payload = json.loads(request.body.decode("utf-8"))
        id = payload.get("id")
        user_name = get_user_name(request)
        if id is None:
            return HttpResponse("id is required", status=500)

        clear_context(user_name, id)
        return HttpResponse(True)
    except Exception as e:
        logger.error(print_err(e))
        return HttpResponse(f"Server error occurred: {e}", status=500)


@csrf_exempt
@require_http_methods(["POST"])
def clear_history_all(request):
    """清空所有聊天记录文件
    params:history_id 聊天记录id
    return:
    """
    try:
        user_name = get_user_name(request)

        clear_all_history(user_name)
        return HttpResponse(True)
    except Exception as e:
        logger.error(print_err(e))
        return HttpResponse(f"Server error occurred: {e}", status=500)


class ModelData:
    def __init__(self, label, model_name, description, model_type):
        self.label = label
        # 模型名称
        self.model_name = model_name
        # 模型描述
        self.description = description
        # 默认模型
        self.default = False
        self.model_type = model_type

    def to_dict(self):
        return {
            "label": self.label,
            "model_name": self.model_name,
            "description": self.description,
            "model_type": self.model_type,
        }

    def set_default(self, isDefault):
        """设置默认模型"""
        self.default = isDefault
