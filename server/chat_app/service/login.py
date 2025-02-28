from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from ..utils import AgentException
from django.contrib.auth import get_user_model
from django.db import IntegrityError


def login(username, password) -> dict:
    """
    使用JWT进行用户登录认证
    Args:
        username: 用户名
        password: 密码
    Returns:
        Response: 包含access/refresh token或错误信息的响应
    """
    serializer = TokenObtainPairSerializer(
        data={"username": username, "password": password}
    )

    try:
        serializer.is_valid(raise_exception=True)
    except Exception as e:
        raise AgentException("PARAM_INVALID", "无效的凭证，请检查用户名或密码")

    return serializer.validated_data


# 注册用户
def register(username, password) -> dict:
    """注册新用户
    Args:
        username: 用户名(需唯一)
        password: 密码
    Returns:
        dict: 包含用户基础信息的字典
    """
    User = get_user_model()

    try:
        # 使用Django的安全创建方法（自动哈希密码）
        user = User.objects.create_user(
            username=username, password=password  # 自动进行密码哈希
        )
    except IntegrityError:
        raise AgentException("PARAM_INVALID", "用户名已被注册")
    except Exception as e:
        raise AgentException("SYSTEM_ERROR", f"用户注册失败: {str(e)}")

    # 返回标准化用户信息
    return {
        "id": user.id,
        "username": user.username,
        "is_active": user.is_active,
        "date_joined": user.date_joined.isoformat(),
    }
