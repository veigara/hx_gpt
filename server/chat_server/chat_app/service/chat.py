
from ..models.model import get_default_model,get_user_model
from ..config import get_default_model_name
from ..utils import *
from ..config import get_default_model_params
from ..models.base_model import ModelType
from django.shortcuts import render,HttpResponse
from django.views.decorators.http import require_http_methods
import logging
from django.views.decorators.csrf import csrf_exempt
import json
from .agent import *
logger = logging.getLogger('chat_app')




# 发送对话 chat
@csrf_exempt
@require_http_methods(["POST"])
def chat_with_model(request):
    try: 
        # 从 POST 请求的查询参数中获取 input_text
        payload = json.loads(request.body.decode('utf-8'))
        input_text = payload.get('input_text')
        model_name = payload.get('model_name')
        user_name = get_user_name(request)
        if input_text is None:
            return HttpResponse("input_text text is required", status=500)
        if model_name is None:
            return HttpResponse("model_name text is required", status=500)
        
        model = get_user_model(user_name,model_name)
        if model is None:
            return HttpResponse(f"{model_name} load error", status=500)
        else:
            return HttpResponse(model.stream_next_chatbot(input_text))
    except Exception as e:
        logger.error(f"Server error occurred: {e}")
        return HttpResponse(f"Server error occurred:{e}", status=500)
    
# 获取所有的模型
@require_http_methods(["GET"])
def get_all_models(request):
    try:
        MODEL_METADATA =get_default_model_params()
        default_model_name = get_default_model_name()
        if MODEL_METADATA is not None:
            model_data_list = []
            for key,value in MODEL_METADATA.items():
                model_name = value['model_name']
                model_data = ModelData(
                            label=key,
                            model_name=model_name,
                            description=value['description']
                        ).to_dict()
                if key == default_model_name:
                    model_data['default'] = True
                    
                model_data_list.append(model_data)
            
            # 将列表转换为 JSON 格式并返回
            return HttpResponse(json.dumps(model_data_list), content_type='application/json')               
    except Exception as e:
        logger.error(f"Server error occurred: {e}")
        return HttpResponse(f"Server error occurred: {e}", status=500) 

# 保存智能体文件
@csrf_exempt
@require_http_methods(["POST"])
def save_agent_file(request):
    payload = json.loads(request.body.decode('utf-8'))
    agent_data = payload.get('agent_data')
    user_name = get_user_name(request)
    try:
        save_agent(user_name,agent_data)
        return HttpResponse("Agent file saved successfully")
    except Exception as e:
        logger.error(f"Server error occurred: {e}")
        return HttpResponse(f"Server error occurred: {e}", status=500)       

# 获取所有的智能体
@require_http_methods(["GET"])
def get_user_agent(request):
    try:
        user_name = get_user_name(request)
        keyword = request.GET.get('keyword')
        agnets = get_user_all_agents(user_name,keyword)
        return HttpResponse(json.dumps(agnets), content_type='application/json')               
    except Exception as e:
        logger.error(f"Server error occurred: {e}")
        return HttpResponse(f"Server error occurred: {e}", status=500) 

# 获取智能体详情
@require_http_methods(["GET"])
def get_agent_detail(request):
    try:
        id = request.GET.get('id')
        # 文件权限用户
        file_user_name = request.GET.get('fileUserName')
        if id is None: 
            return HttpResponse("id is required", status=500)
        detail = load_agent(file_user_name,id)
        return HttpResponse(json.dumps(detail), content_type='application/json')               
    except Exception as e:
        logger.error(f"Server error occurred: {e}")
        return HttpResponse(f"Server error occurred: {e}", status=500) 
    
 
 # 删除智能体
@csrf_exempt
@require_http_methods(["DELETE"])
def get_del_agent(request):
    try:
        id = request.GET.get('id')
        user_name = get_user_name(request)
        if id is None: 
            return HttpResponse("id is required", status=500)
        del_agent(user_name,id)
        return HttpResponse(True)               
    except Exception as e:
        logger.error(f"Server error occurred: {e}")
        return HttpResponse(f"Server error occurred: {e}", status=500)       
 
    
class ModelData:
    def __init__(self,label,model_name,description):
        self.label = label
        # 模型名称
        self.model_name = model_name
        # 模型描述
        self.description = description
        # 默认模型
        self.default = False

    def to_dict(self):
        return {
            'label': self.label,
            'model_name': self.model_name,
            'description': self.description,
        }
        
    def set_default(self,isDefault):
        """设置默认模型"""
        self.default = isDefault        

