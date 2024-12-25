import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import HttpResponse
from ..utils import *
from ..presets import *
from ..service.knowledge.knowledge import upload_file as UPLOAD_FILE

logger = logging.getLogger("chat_app")


@csrf_exempt
@require_http_methods(["POST"])
def upload_file(request):
    try:
        user_name = get_user_name(request)
        uploaded_file = request.FILES["file"]
        knowledge_id = request.POST.get("id")

        UPLOAD_FILE(user_name, knowledge_id, uploaded_file)
        return JsonResponse({"status": "success"})
    except Exception as e:
        logger.error(print_err(e))
        return HttpResponse(f"Server error occurred:{e}", status=500)
