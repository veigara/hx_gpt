"""
WSGI config for chat_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from chat_app.initialize import initialize_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_server.settings')

# 初始化服务
initialize_model()


application = get_wsgi_application()
