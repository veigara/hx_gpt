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
from chat_app import views
from chat_app.web import chat_web, model_web, config_web, knowledge_web, login_web
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello", views.hello, name="hello"),
    path("favicon.ico", RedirectView.as_view(url="/static/favicon.ico")),
    path("chat", chat_web.chat_with_model, name="chat_with_model"),
    # 获取所有的大模型
    path("models", chat_web.get_all_models, name="get_all_models"),
    # 保存角色体文件
    path("save_agent_file", chat_web.save_agent_file, name="save_agent_file"),
    # 查询当前用户所有角色体文件
    path("get_user_agent", chat_web.get_user_agent, name="get_user_agent"),
    # 查询当前用户的角色体文件详情
    path("get_agent_detail", chat_web.get_agent_detail, name="get_agent_detail"),
    # 删除角色体
    path("del_agent", chat_web.get_del_agent, name="get_del_agent"),
    # 选择角色体
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
    # 获取当前聊天记录的tokens
    path(
        "get_count_tokens",
        chat_web.get_cur_history_counts,
        name="get_cur_history_counts",
    ),
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
    # 上传知识库
    path(
        "knowledge_file/upload", knowledge_web.upload_file, name="knowledge_upload_file"
    ),
    # 查询文件
    path(
        "knowledge_file/search", knowledge_web.search_file, name="knowledge_search_file"
    ),
    # 删除文件
    path("knowledge_file/delete", knowledge_web.del_file, name="knowledge_del_file"),
    # 保存/更新知识库基本信息
    path(
        "knowledge/save_update",
        knowledge_web.save_update_knowledge,
        name="save_update_knowledge",
    ),
    # 搜索知识库
    path("knowledge/search", knowledge_web.search_knowledge, name="search_knowledge"),
    # 删除知识库
    path("knowledge/delete", knowledge_web.del_knowledge, name="del_knowledge"),
    # 检索知识库
    path(
        "knowledge/retrieve",
        knowledge_web.knowledge_retrieve,
        name="knowledge_retrieve",
    ),
    # 下载知识库文件
    path(
        "knowledge/down",
        knowledge_web.down_knowledge_file,
        name="down_knowledge_file",
    ),
    # 上传聊天文件
    path(
        "chat/upload",
        chat_web.upload_file,
        name="chat/upload_file",
    ),
    # 下载聊天文件
    path(
        "chat/down_file",
        chat_web.down_chat_file,
        name="chat/down_chat_file",
    ),
    # 解析聊天文件
    path(
        "chat/parse_file",
        chat_web.parse_chat_file,
        name="chat/parse_chat_file",
    ),
    # 修改聊天记录文件
    path(
        "chat/update_history", chat_web.update_chat_history, name="update_chat_history"
    ),
    # 新建分支聊天
    path(
        "chat/snip_history_build",
        chat_web.snip_chat_history_build,
        name="snip_chat_history_build",
    ),
    # 转为角色体
    path(
        "chat/build_hisorty_to_agent",
        chat_web.build_chat_hisorty_to_agent,
        name="build_chat_hisorty_to_agent",
    ),
    # 登录
    path(
        "chat/login",
        login_web.chat_login,
        name="chat_login",
    ),
    # 注册
    path(
        "chat/register",
        login_web.chat_register,
        name="chat_register",
    ),
    # vue页面
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    re_path(r"^.*/$", TemplateView.as_view(template_name="index.html")),
    # jwt 认证
    path("token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    # 复制聊天记录
    path("chat/copy_history", chat_web.copy_chat_history, name="copy_chat_history"),
]
