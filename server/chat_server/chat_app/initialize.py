from django.core.management.base import BaseCommand
import logging

from .models.model import get_model
from .config import get_default_model_name

logger = logging.getLogger('chat_app')

def initialize_model():
    """初始化模型"""
    pass
     # 设置默认model
    model_name = get_default_model_name()

    model = get_model(model_name=model_name)
    logger.info("Model instance: " + str(model))
       
