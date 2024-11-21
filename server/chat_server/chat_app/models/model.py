import logging
from ..utils import *
from .base_model import BaseLLMModel, ModelType
from ..presets import *

_model_instance = None

logger = logging.getLogger('chat_app')

def get_default_model() -> BaseLLMModel:
    """
    获取模型实例。
    
    此函数返回一个模型实例，该实例是程序中先前定义的全局变量 _model_instance。
    主要用途是提供一个简单的方法来访问模型实例，而不需要直接访问全局变量。
    
    返回:
    _model_instance: 模型实例，具体类型取决于 _model_instance 的定义。
    """
    return _model_instance

def set_model(new_model):
    """设置全局模型"""
    global _model_instance
    _model_instance = new_model

def get_model(
    model_name,
    access_key=None,
    user_name="",
) -> BaseLLMModel:
    global _model_instance
    msg = f"模型设置为了：{model_name}"
    model_type = ModelType.get_type(model_name)
    try:
        if model_type == ModelType.Groq:
            logger.info(f"正在加载Groq模型: {model_name}")
            from .Groq import Groq_Client
            model = Groq_Client(model_name, access_key, user_name=user_name)
        elif model_type == ModelType.LMStudio:
            logger.info(f"正在加载LMStudio本地模型: {model_name}")
            from .LMStudio import LMStudio_Client
            model = LMStudio_Client(model_name, None, user_name=user_name)
            
        _model_instance = model
        return model    
    except Exception as e:
        import traceback
        traceback.print_exc()
        msg = f"{STANDARD_ERROR_MSG}: {e}"              