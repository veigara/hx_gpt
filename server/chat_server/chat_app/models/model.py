import logging
from ..utils import *
from .base_model import BaseLLMModel
from ..presets import *
from ..service.ai_model import get_model_detail, ModelType

logger = logging.getLogger("chat_app")


def get_model(
    model_key, access_key=None, user_name="", history_id=None, agent_id=None
) -> BaseLLMModel:
    msg = f"模型设置为了：{model_key}"
    model = get_model_detail(model_key)
    if model is None:
        raise Exception(f"{STANDARD_ERROR_MSG}: 模型不存在")
    model_type = model["model_type"]

    try:
        if model_type == ModelType.GROQ.value:
            logger.info(f"正在加载Groq模型: {model_key}")
            from .Groq import Groq_Client

            model = Groq_Client(
                model_key,
                None,
                user_name=user_name,
                history_id=history_id,
                agent_id=agent_id,
            )
        elif model_type == ModelType.LMSTUDIO.value:
            logger.info(f"正在加载LMStudio本地模型: {model_key}")
            from .LMStudio import LMStudio_Client

            model = LMStudio_Client(model_key, None, user_name=user_name)
        else:
            raise Exception(f"{STANDARD_ERROR_MSG}: 模型类型【{model_type}】不支持")

        return model
    except Exception as e:
        import traceback

        traceback.print_exc()
        msg = f"{STANDARD_ERROR_MSG}: {e}"
