from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from ..base_module.base_response import AgentResponse
from django.http import JsonResponse
from ..presets import STANDARD_ERROR_MSG


def jwt_authenticate(request):
    """自定义JWT认证函数"""
    try:
        authenticator = JWTAuthentication()
        auth_tuple = authenticator.authenticate(request)
        if auth_tuple is None:  # 没有携带token的情况
            return None, "未提供认证凭证"
        user, token = auth_tuple
        return user, None
    except AuthenticationFailed as e:
        return None, str(e.detail)
    except Exception as e:
        return None, "认证失败"


def check_permission(view_func):
    """自定义权限装饰器"""

    def wrapper(request, *args, **kwargs):
        user, error = jwt_authenticate(request)

        if not user:
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}{error or '未认证'}"),
                status=401,
                json_dumps_params={"ensure_ascii": False},  # 禁用 ASCII 转义
                content_type="application/json; charset=utf-8",  # 明确指定编码
            )

        if not user.is_active:
            return JsonResponse(
                AgentResponse.fail(fail_msg=f"{STANDARD_ERROR_MSG}账户已禁用"),
                status=403,
                json_dumps_params={"ensure_ascii": False},  # 禁用 ASCII 转义
                content_type="application/json; charset=utf-8",  # 明确指定编码
            )

        # 将用户对象附加到request中
        request.user = user
        return view_func(request, *args, **kwargs)

    return wrapper
