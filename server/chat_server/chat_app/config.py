import os
import commentjson as json
import logging
from .presets import *


logger = logging.getLogger('chat_app')

# 添加一个统一的config文件，避免文件过多造成的疑惑（优先级最低）
# 同时，也可以为后续支持自定义功能提供config的帮助
# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 构建 config.json 的绝对路径
config_path = os.path.join(BASE_DIR, 'chat_app','config.json')

if os.path.exists(config_path):
    with open(config_path, "r", encoding='utf-8') as f:
        config = json.load(f)
else:
    config = {}

groq_api_key = config.get("groq_api_key", "")
os.environ["GROQ_API_KEY"] = groq_api_key

lmstudio_host = config.get("lmstudio_host", "")
os.environ["LMSTUDIO_HOST"] = lmstudio_host
lmstudio_api_key = config.get("lmstudio_api_key", "")
os.environ["LMSTUDIO_API_KEY"] = lmstudio_api_key

# 设置默认的模型参数
def set_default_model_params() -> None:
    # 声明 MODEL_METADATA 是全局变量
    global MODEL_METADATA 
    _model_metadata = {}
    for k, v in MODEL_METADATA.items():
        temp_dict = DEFAULT_METADATA.copy()
        temp_dict.update(v)
        _model_metadata[k] = temp_dict
    
    MODEL_METADATA = _model_metadata

def get_default_model_params():
    return MODEL_METADATA

def get_default_model_name() -> str:
    # 设置默认model
    default_model = config.get("default_model", "GPT-4o-mini")
    try:
        if default_model in MODELS:
            DEFAULT_MODEL = MODELS.index(default_model)
        else:
            DEFAULT_MODEL = MODELS.index(next((k for k, v in MODEL_METADATA.items() if v.get("model_name") == default_model), None))
        logger.info("默认模型设置为了：" + str(MODELS[DEFAULT_MODEL]))
        
        return MODELS[DEFAULT_MODEL]
    except ValueError:
        logger.error("你填写的默认模型" + default_model + "不存在！请从下面的列表中挑一个填写：" + str(MODELS))
        return MODELS[DEFAULT_MODEL]

