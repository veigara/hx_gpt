import logging
from ..utils import *
from .base_model import BaseLLMModel, ModelType
from ..presets import *

_model_instance = None

# 用户存放的模型实例 <p>{1222:{model_name:LALM_11,model_instance:23445}}</p>
_user_model_instance = {}

logger = logging.getLogger("chat_app")


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
