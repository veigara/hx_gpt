
from ..models.model import get_default_model,get_model
from ..config import get_default_model_name
from ..utils import *
from ..config import get_default_model_params
from ..models.base_model import ModelType
from django.shortcuts import render,HttpResponse
import logging
from django.views.decorators.csrf import csrf_exempt
import json

logger = logging.getLogger('chat_app')




# 发送对话 chat
@csrf_exempt
def chat_with_model(request):
    if request.method == 'POST':
        try: 
            # 从 POST 请求的查询参数中获取 input_text
            payload = json.loads(request.body.decode('utf-8'))
            input_text = payload.get('input_text')
            model_name = payload.get('model_name')
        
            if input_text:
                if model_name is None:
                    model = get_default_model()
                else:    
                    model = get_model(model_name)
                return HttpResponse(model.stream_next_chatbot(input_text))
            else:
                return HttpResponse("Input text is required", status=500)
        except Exception as e:
            logger.error(f"Server error occurred: {e}")
            return HttpResponse(f"Server error occurred:{e}", status=500)
    else:
        return HttpResponse("Invalid request method", status=405)
    
# 获取所有的模型
def get_all_models(request):
    if request.method == 'GET':
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
    else:
        return HttpResponse("Invalid request method", status=405)




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

