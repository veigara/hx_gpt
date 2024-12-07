import logging
from ..utils import *
from .base_model import BaseLLMModel, ModelType
from ..presets import *

_model_instance = None

# 用户存放的模型实例 <p>{1222:{model_name:LALM_11,model_instance:23445}}</p>
_user_model_instance = {}

logger = logging.getLogger("chat_app")


def get_default_model() -> BaseLLMModel:
    """
    获取模型实例。

    此函数返回一个模型实例，该实例是程序中先前定义的全局变量 _model_instance。
    主要用途是提供一个简单的方法来访问模型实例，而不需要直接访问全局变量。

    返回:
    _model_instance: 模型实例，具体类型取决于 _model_instance 的定义。
    """
    return _model_instance


def set_model(user_name, cur_model_name, new_model):
    """设置全局模型"""
    global _user_model_instance
    _user_model_instance[user_name] = {
        "model_name": cur_model_name,
        "model_instance": new_model,
    }


def get_user_model(user_name, model_name, history_id, agent_id) -> BaseLLMModel:
    """
    根据用户名称和模型名称获取用户模型实例。

    参数:
    - user_name: 用户名称，用于查找用户的模型实例。
    - model_name: 模型名称，用于指定用户当前使用的模型。

    返回:
    - BaseLLMModel: 返回一个基础LLM模型实例，如果找不到或需要更新模型实例，则返回新的模型实例。
    """
    if user_name is None:
        return None

    model_data = _user_model_instance.get(user_name, {})
    cur_model_name = model_data.get("model_name")
    model_instance = model_data.get("model_instance")

    if model_instance is None or (
        model_name is not None and model_name != cur_model_name
    ):
        """重新加载 模型"""
        new_model = get_model(
            model_name=model_name,
            user_name=user_name,
            history_id=history_id,
            agent_id=agent_id,
        )
        set_model(user_name, model_name, new_model)
        return new_model

    return model_instance


# 设置用户模型
def set_user_model(user_name, model):
    global _user_model_instance
    _user_model_instance[user_name] = model


def get_model(
    model_name, access_key=None, user_name="", history_id=None, agent_id=None
) -> BaseLLMModel:
    global _model_instance
    msg = f"模型设置为了：{model_name}"
    model_type = ModelType.get_type(model_name)
    try:
        if model_type == ModelType.Groq:
            logger.info(f"正在加载Groq模型: {model_name}")
            from .Groq import Groq_Client

            model = Groq_Client(
                model_name,
                None,
                user_name=user_name,
                history_id=history_id,
                agent_id=agent_id,
            )
        elif model_type == ModelType.LMStudio:
            logger.info(f"正在加载LMStudio本地模型: {model_name}")
            from .LMStudio import LMStudio_Client

            model = LMStudio_Client(model_name, None, user_name=user_name)

        return model
    except Exception as e:
        import traceback

        traceback.print_exc()
        msg = f"{STANDARD_ERROR_MSG}: {e}"
