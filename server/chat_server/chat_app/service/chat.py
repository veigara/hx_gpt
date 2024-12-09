from ..models.model import get_model
from ..config import get_default_model_name
from ..utils import *
from ..config import get_default_model_params
from ..models.base_model import *
from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_http_methods
import logging
from django.views.decorators.csrf import csrf_exempt
import json
from .agent import *
from .history import *
from ..cache_utils import *

logger = logging.getLogger("chat_app")


# 发送对话 chat
@csrf_exempt
@require_http_methods(["POST"])
def chat_with_model(request):
    try:
        # 从 POST 请求的查询参数中获取 input_text
        payload = json.loads(request.body.decode("utf-8"))
        input_text = payload.get("input_text")
        model_name = payload.get("model_name")
        history_id = payload.get("history_id")
        agent_id = payload.get("agent_id")
        user_name = get_user_name(request)
        if input_text is None:
            return HttpResponse("input_text text is required", status=500)
        if model_name is None:
            return HttpResponse("model_name text is required", status=500)
        if history_id is None or history_id == "":
            # 没有选择智能体，要创建一个默认的
            history_id = cretate_new_history(user_name, model_name, input_text)
            agent_data = get_default_agent_data(user_name)
            agent_id = agent_data.get("id")
        model = get_model(
            model_name=model_name,
            user_name=user_name,
            history_id=history_id,
            agent_id=agent_id,
        )

        if model is None:
            return HttpResponse(f"{model_name} load error", status=500)
        else:
            return HttpResponse(
                model.stream_next_chatbot(input_text, history_id, agent_id)
            )
    except Exception as e:
        logger.error(print_err(e))
        return HttpResponse(f"Server error occurred:{e}", status=500)


# 获取所有的模型
@require_http_methods(["GET"])
def get_all_models(request):
    try:
        MODEL_METADATA = get_default_model_params()
        default_model_name = get_default_model_name()
        if MODEL_METADATA is not None:
            model_data_list = []
            for key, value in MODEL_METADATA.items():
                model_name = value["model_name"]
                model_data = ModelData(
                    label=key,
                    model_name=model_name,
                    description=value["description"],
                    model_type=value["model_type"],
                ).to_dict()
                if key == default_model_name:
                    model_data["default"] = True

                model_data_list.append(model_data)

            # 将列表转换为 JSON 格式并返回
            return HttpResponse(
                json.dumps(model_data_list), content_type="application/json"
            )
    except Exception as e:
        logger.error(print_err(e))
        return HttpResponse(f"Server error occurred: {e}", status=500)


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
    return: 历史记录id
    """
    try:
        id = request.GET.get("id")
        user_name = get_user_name(request)
        if id is None:
            return HttpResponse("id is required", status=500)
        agent_data = load_agent(user_name, id)
        if agent_data is None:
            return HttpResponse("智能体内容不存在", status=500)
        # 创建历史记录
        history_id = save_history_agent(user_name, agent_data)

        return HttpResponse(history_id)

    except Exception as e:
        logger.error(print_err(e))
        return HttpResponse(f"Server error occurred: {e}", status=500)


@require_http_methods(["GET"])
def get_historys(request):
    """获取用户的历史记录
    params:keyword 关键字
    return:历史记录列表
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
    """获取历史记录详情
    params:id 历史记录id
    return:历史记录详情
    """
    try:
        id = request.GET.get("id")
        user_name = get_user_name(request)
        if id is None:
            return HttpResponse("id is required", status=500)
        detail = load_history(user_name, id)
        # 将历史记录加载到上下文中
        clear_history_global(user_name)
        set_history_global(user_name, detail.get("content", []))
        return HttpResponse(json.dumps(detail), content_type="application/json")
    except Exception as e:
        logger.error(print_err(e))
        return HttpResponse(f"Server error occurred: {e}", status=500)


@require_http_methods(["DELETE"])
@csrf_exempt
def del_user_history(request):
    """删除历史记录
    params:id 历史记录id
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
    """重命名历史记录
    params:id 历史记录id
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
    """置顶历史记录
    params:id 历史记录id
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
