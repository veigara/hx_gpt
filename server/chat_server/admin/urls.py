"""chat_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from chat_app import views
from chat_app.web import chat_web, model_web, config_web

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello", views.hello, name="hello"),
    path("chat", chat_web.chat_with_model, name="chat_with_model"),
    # 获取所有的大模型
    path("models", chat_web.get_all_models, name="get_all_models"),
    # 保存智能体文件
    path("save_agent_file", chat_web.save_agent_file, name="save_agent_file"),
    # 查询当前用户所有智能体文件
    path("get_user_agent", chat_web.get_user_agent, name="get_user_agent"),
    # 查询当前用户的智能体文件详情
    path("get_agent_detail", chat_web.get_agent_detail, name="get_agent_detail"),
    # 删除智能体
    path("del_agent", chat_web.get_del_agent, name="get_del_agent"),
    # 选择智能体
    path("select_agent", chat_web.select_agent, name="select_agent"),
    # 获取聊天记录
    path("get_historys", chat_web.get_historys, name="get_historys"),
    # 获取聊天记录详情
    path("get_history_detail", chat_web.get_history_detail, name="get_history_detail"),
    # 删除聊天记录
    path("del_history", chat_web.del_user_history, name="del_user_history"),
    # 重命名聊天记录
    path("rename_history", chat_web.rename_user_history, name="rename_user_history"),
    # 置顶聊天记录
    path("top_history", chat_web.top_user_history, name="top_user_history"),
    # 清空上下文
    path(
        "clear_history_context",
        chat_web.clear_history_context,
        name="clear_history_context",
    ),
    # 清空所有聊天记录文件
    path("clear_history_all", chat_web.clear_history_all, name="clear_history_all"),
    # 获取模型类别
    path("get_model_type", model_web.get_all_model_type, name="get_all_model_type"),
    # 获取所有的模型
    path("get_all_models", model_web.get_all_models, name="get_all_models"),
    # 获取模型详情
    path("get_model_detail", model_web.get_model_detail, name="get_model_detail"),
    # 删除模型
    path("remove_model", model_web.remove_model, name="remove_model"),
    # 更新模型详情
    path("update_model", model_web.update_model_detail, name="update_model_detail"),
    # 添加模型
    path("add_model", model_web.add_model, name="add_model"),
    # 获取配置信息
    path("get_config", config_web.get_config, name="get_config"),
    # 更新配置信息
    path("update_config", config_web.update_config, name="update_config"),
]
