"""
WSGI config for chat_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import nltk

from django.core.wsgi import get_wsgi_application
from chat_app.initialize import initialize_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat_server.settings")

# 初始化服务
# initialize_model()

# 添加nltk目录
# 获取上级目录
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 上级目录下的chat_app/libs/nltk_data目录
nltk_data_dir = os.path.join(parent_dir, "chat_app/libs/nltk_data")

nltk.data.path.append(nltk_data_dir)

application = get_wsgi_application()
