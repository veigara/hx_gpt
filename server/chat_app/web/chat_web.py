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
from django.http import StreamingHttpResponse
import json
from ..service.agent import *
from ..service.history import *
from ..service.knowledge_se import (
    knowledge_retrieve as KNOWLEDGE_RETRIEVE,
)
from ..service.ai_model import get_all_models as GET_ALL_MODELS
from ..service.chat_file import (
    upload_file as CHAT_UPLOAD_FILE,
    down_file as CHAT_DOWN_FILE,
    parse_file_to_text as CHAT_PARSE_FILE,
)

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
        # 文件地址
        file_path = payload.get("file_path")
        # 文件名称
        file_name = payload.get("file_name")
        # 解析文件名称
        parse_file_id = payload.get("parse_file_id")
        # 知识库
        know_id = payload.get("know_id")
        # 连续对话
        convOff = payload.get("conv_off", True)
        # 在线搜索
        online_search = payload.get("online_search", False)
        user_name = get_user_name(request)
        if input_text is None:
            fail_msg = f"{STANDARD_ERROR_MSG}输入内容不能为空"
            return StreamingHttpResponse(
                error_stream(fail_msg), status=500, content_type="application/json"
            )
        if model_key is None:
            fail_msg = f"{STANDARD_ERROR_MSG}请选择模型"
            return StreamingHttpResponse(
                error_stream(fail_msg), status=500, content_type="application/json"
            )
        if history_id is None or history_id == "":
            # 没有选择角色体，要创建一个默认的
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
            fail_msg = f"{STANDARD_ERROR_MSG}加载{model_key}失败"
            return StreamingHttpResponse(
                error_stream(fail_msg), status=500, content_type="application/json"
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
                response = model.stream_next_chatbot(
                    input_text, history_id, file_path, file_name, parse_file_id
                )
            else:
                response = model.get_answer_chatbot_at_once(
                    input_text, file_path, file_name, parse_file_id
                )

            return response
    except requests.exceptions.ConnectTimeout:
        status_text = STANDARD_ERROR_MSG + CONNECTION_TIMEOUT_MSG + ERROR_RETRIEVE_MSG
        return StreamingHttpResponse(
            error_stream(status_text), status=500, content_type="application/json"
        )
    except requests.exceptions.ReadTimeout:
        status_text = STANDARD_ERROR_MSG + READ_TIMEOUT_MSG + ERROR_RETRIEVE_MSG
        return StreamingHttpResponse(
            error_stream(status_text), status=500, content_type="application/json"
        )
    except Exception as e:
        logger.error(print_err(e))

        # 返回500错误和错误信息
        fail_msg = f"{STANDARD_ERROR_MSG}对话失败,{e}"
        return StreamingHttpResponse(
            error_stream(fail_msg), status=500, content_type="application/json"
        )


def error_stream(fail_msg):
    yield json.dumps({"error": str(fail_msg)}).encode("utf-8")
    yield b"\n"  # 可以在这里添加额外的信息或格式化输出


# 获取所有的模型
@require_http_methods(["GET"])
def get_all_models(request):
    try:
        user_name = get_user_name(request)
        default_model_key = get_default_model_name()
        models = GET_ALL_MODELS(user_name)
        if models is not None:
            for model in models:
                if model.get("model_key") == default_model_key:
                    model["default"] = True

        return JsonResponse(AgentResponse.success(data=models))

    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}获取所有的模型失败")
        )


# 保存角色体文件
@csrf_exempt
@require_http_methods(["POST"])
def save_agent_file(request):
    payload = json.loads(request.body.decode("utf-8"))
    agent_data = payload.get("agent_data")
    user_name = get_user_name(request)
    try:
        json_data = json.loads(agent_data)
        id = json_data.get("id")
        if not id:
            datas = save_agent(user_name, json_data)
        else:
            datas = update_agent(user_name, json_data)
        return JsonResponse(AgentResponse.success(data=datas))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}保存角色体文件失败")
        )


# 获取所有的角色体
@require_http_methods(["GET"])
def get_user_agent(request):
    try:
        user_name = get_user_name(request)
        keyword = request.GET.get("keyword")
        agnets = get_user_all_agents(user_name, keyword)

        return JsonResponse(AgentResponse.success(data=agnets))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}获取所有的角色体失败")
        )


# 获取角色体详情
@require_http_methods(["GET"])
def get_agent_detail(request):
    try:
        id = request.GET.get("id")
        # 用户
        user_name = get_user_name(request)
        if id is None:
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}角色体id不能为空")
            )
        detail = load_agent(user_name, id)
        return JsonResponse(AgentResponse.success(data=detail))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}获取所有的角色体失败")
        )


# 删除角色体
@csrf_exempt
@require_http_methods(["DELETE"])
def get_del_agent(request):
    try:
        id = request.GET.get("id")
        user_name = get_user_name(request)
        if id is None:
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}角色体id不能为空")
            )
        # 查询角色体关联的历史记录
        historys = get_historys_by_agent_id(id)
        if len(historys) > 0:
            titles = [item.get("title") for item in historys]
            del_titles = ",".join(titles)
            return JsonResponse(
                AgentResponse.fail(
                    fail_msg=f"{STANDARD_ERROR_MSG}删除失败,请先删除一下聊天记录:【{del_titles}】"
                )
            )
        del_agent(user_name, id)
        return JsonResponse(AgentResponse.success(data=True))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}删除角色体失败")
        )


@require_http_methods(["GET"])
def select_agent(request) -> str:
    """选择角色体
     params:id 角色体id
     params:fileUserName 角色体文件用户
    return: 聊天记录id
    """
    try:
        id = request.GET.get("id")
        user_name = get_user_name(request)
        if id is None:
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}角色体id不能为空")
            )
        agent_data = load_agent(user_name, id)
        if agent_data is None:
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}角色体内容不能为空")
            )
        # 创建聊天记录
        history_id = save_history_agent(user_name, agent_data)

        return JsonResponse(AgentResponse.success(data=history_id))

    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}删除角色体失败")
        )


@require_http_methods(["GET"])
def get_historys(request):
    """获取用户的聊天记录
    params:keyword 关键字
    return:聊天记录列表
    """
    try:
        user_name = get_user_name(request)
        keyword = request.GET.get("keyword")
        data = get_user_all_history(user_name, keyword)
        return JsonResponse(AgentResponse.success(data=data))

    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}获取用户的聊天记录失败")
        )


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
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}聊天记录id不能为空")
            )
        data = load_history(id)
        return JsonResponse(AgentResponse.success(data=data))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}获取聊天记录详情失败")
        )


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
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}聊天记录id不能为空")
            )
        del_history(user_name, id)
        return JsonResponse(AgentResponse.success(data=True))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}删除聊天记录失败")
        )


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
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}聊天记录id不能为空")
            )
        if new_title is None:
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}重命名标题不能为空")
            )
        rename_history(user_name, id, new_title)
        return JsonResponse(AgentResponse.success(data=True))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}重命名聊天记录失败")
        )


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
        if id is None:
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}聊天记录id不能为空")
            )
        top_history(id)
        return JsonResponse(AgentResponse.success(data=True))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}重命名聊天记录失败")
        )


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
        if id is None or id == "":
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}聊天记录id不能为空")
            )
        clear_context(user_name, id)
        return JsonResponse(AgentResponse.success(data=True))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}清空当前聊天记录失败")
        )


@csrf_exempt
@require_http_methods(["POST"])
def clear_history_all(request):
    """清空所有聊天记录
    params:history_id 聊天记录id
    return:
    """
    try:
        user_name = get_user_name(request)

        clear_all_history(user_name)
        return JsonResponse(AgentResponse.success(data=True))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}清空所有聊天记录失败")
        )


@require_http_methods(["GET"])
def get_cur_history_counts(request):
    """获取当前聊天记录的token"""
    try:
        id = request.GET.get("id")
        data = get_count_tokens(id)
        return JsonResponse(AgentResponse.success(data=data))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(
                fail_msg=f"{STANDARD_ERROR_MSG}获取当前聊天记录的token失败"
            )
        )


@csrf_exempt
@require_http_methods(["POST"])
def upload_file(request):
    try:
        user_name = get_user_name(request)
        uploaded_file = request.FILES["file"]

        files = CHAT_UPLOAD_FILE(user_name, uploaded_file)
        return JsonResponse(
            AgentResponse.success(
                data={
                    "status": "success",
                    "file_path": files["file_path"],
                    "file_name": files["file_name"],
                }
            )
        )
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}上传文件失败")
        )


@require_http_methods(["GET"])
def down_chat_file(request):
    """下载文件"""
    try:
        file_path = request.GET.get("file_path")
        file_name = request.GET.get("file_name")
        response = CHAT_DOWN_FILE(file_name, file_path)
        return response
    except AgentException as e:
        return JsonResponse(AgentResponse.fail(fail_msg=e.message))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}下载聊天文件失败")
        )


@csrf_exempt
@require_http_methods(["POST"])
def parse_chat_file(request):
    """解析文件"""
    try:
        user_name = get_user_name(request)
        payload = json.loads(request.body.decode("utf-8"))
        file_path = payload.get("file_path")
        file_name = payload.get("file_name")
        model_key = payload.get("model_key")
        if file_path is None:
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}文件路径不能为空")
            )
        if file_name is None:
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}文件名称不能为空")
            )
        if model_key is None:
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}模型名称不能为空")
            )
        res = CHAT_PARSE_FILE(
            user_name=user_name,
            file_path=file_path,
            file_name=file_name,
            model_key=model_key,
        )
        return JsonResponse(AgentResponse.success(data=res))
    except AgentException as e:
        return JsonResponse(AgentResponse.fail(fail_msg=e.message))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(
                fail_msg=f"{STANDARD_ERROR_MSG}解析聊天文件失败,原因：{str(e.message)}"
            )
        )


@csrf_exempt
@require_http_methods(["POST"])
def update_chat_history(request):
    """
    修改历史记录
    """
    try:
        user_name = get_user_name(request)
        payload = json.loads(request.body.decode("utf-8"))
        history_id = payload.get("history_id")
        contents_str = payload.get("contents_str")
        if user_name is None:
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}用户名称不能为空")
            )

        if history_id is None:
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}聊天记录id不能为空")
            )

        if contents_str is None:
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}聊天内容字不能为空")
            )
        # 将json字符串转成list
        contents = json.loads(contents_str)

        update_history_id(user_name, history_id, contents)

        return JsonResponse(AgentResponse.success(data={}))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}修改聊天记录失败")
        )


@csrf_exempt
@require_http_methods(["POST"])
def snip_chat_history_build(request) -> dict:
    """
    新建分支聊天
    """
    try:
        user_name = get_user_name(request)
        payload = json.loads(request.body.decode("utf-8"))
        history_id = payload.get("history_id")
        contents_str = payload.get("contents_str")
        if user_name is None:
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}用户名称不能为空")
            )

        if history_id is None:
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}聊天记录id不能为空")
            )

        if contents_str is None:
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}聊天内容字不能为空")
            )
        # 将json字符串转成list
        contents = json.loads(contents_str)

        res = snip_history_build(user_name, history_id, contents)

        return JsonResponse(AgentResponse.success(data=res))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}新建分支聊天失败")
        )


@csrf_exempt
@require_http_methods(["POST"])
def build_chat_hisorty_to_agent(request):
    """
    将当前历史记录转为角色体
    """
    try:
        user_name = get_user_name(request)
        payload = json.loads(request.body.decode("utf-8"))
        history_id = payload.get("history_id")
        agent_title = payload.get("agent_title")
        if user_name is None:
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}用户名称不能为空")
            )

        if history_id is None:
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}聊天记录id不能为空")
            )

        if agent_title is None:
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}标题内容不能为空")
            )

        build_hisorty_to_agent(user_name, agent_title, history_id)

        return JsonResponse(AgentResponse.success(data={}))
    except Exception as e:
        logger.error(print_err(e))
        return JsonResponse(
            AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}转为角色体失败")
        )


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
