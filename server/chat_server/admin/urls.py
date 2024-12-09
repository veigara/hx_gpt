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
from chat_app.service import chat

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello", views.hello, name="hello"),
    path("chat", chat.chat_with_model, name="chat_with_model"),
    # 获取所有的大模型
    path("models", chat.get_all_models, name="get_all_models"),
    # 保存智能体文件
    path("save_agent_file", chat.save_agent_file, name="save_agent_file"),
    # 查询当前用户所有智能体文件
    path("get_user_agent", chat.get_user_agent, name="get_user_agent"),
    # 查询当前用户的智能体文件详情
    path("get_agent_detail", chat.get_agent_detail, name="get_agent_detail"),
    # 删除智能体
    path("del_agent", chat.get_del_agent, name="get_del_agent"),
    # 选择智能体
    path("select_agent", chat.select_agent, name="select_agent"),
    # 获取历史记录
    path("get_historys", chat.get_historys, name="get_historys"),
    # 获取历史记录详情
    path("get_history_detail", chat.get_history_detail, name="get_history_detail"),
    # 删除历史记录
    path("del_history", chat.del_user_history, name="del_user_history"),
    # 重命名历史记录
    path("rename_history", chat.rename_user_history, name="rename_user_history"),
    # 置顶历史记录
    path("top_history", chat.top_user_history, name="top_user_history"),
]
