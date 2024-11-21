
from ..models.model import get_default_model,get_model
from ..config import get_default_model_name
from ..utils import *
from ..config import get_default_model_params
from ..models.base_model import ModelType
from django.shortcuts import render,HttpResponse


# 发送对话 chat
def chat_with_model(request):
    if request.method == 'GET':
        # 从 GET 请求的查询参数中获取 input_text
        input_text = request.GET.get('input_text')
        model_name = request.GET.get('model_name')
       
        if input_text:
            if model_name is None:
                model = get_default_model()
            #   model_name = get_default_model_name()
            #   model = get_model(model_name)  
            else:    
                model = get_model(model_name)
            return HttpResponse(model.stream_next_chatbot(input_text))
        else:
            return HttpResponse("Input text is required", status=400)
    else:
        return HttpResponse("Invalid request method", status=405)
