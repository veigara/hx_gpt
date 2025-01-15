"""
Django settings for admin project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import sys
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "$cn%qo*8$x)4h3_kj#!+kh&96g^nqs=6a@$vu&tr&yqy-k6av!"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "chat_app",
    "corsheaders",
]

MIDDLEWARE = [
    "log_request_id.middleware.RequestIDMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "admin.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "web")],  # 配置模板查找路径
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "admin.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "hx_gpt",
        "USER": "root",  # 数据库用户名
        "PASSWORD": "123456",  # 数据库密码
        "HOST": "192.168.0.147",  # 数据库主机地址
        "PORT": "3306",  # 数据库端口号
        # 'OPTIONS': {
        #     'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        # },
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

# LANGUAGE_CODE = "en-us"
# TIME_ZONE = "Asia/Shanghai"  # 根据你的实际时区进行设置
# 不使用时区UTC
USE_TZ = False

USE_I18N = True

USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"

# 静态文件在开发过程中的查找目录
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "web"),
    os.path.join(BASE_DIR, "web/static"),
]

# 收集静态文件后的存放目录
STATIC_ROOT = BASE_DIR / "staticfiles"

# 如果在 Windows 上运行，导入 colorama
LOG_REQUEST_ID_HEADER = "HTTP_X_REQUEST_ID"
GENERATE_REQUEST_ID_IF_NOT_IN_HEADER = True
REQUEST_ID_RESPONSE_HEADER = "TRACE-ID"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "simple": {"format": "%(levelname)s %(message)s"},
        "color": {
            "()": "colorlog.ColoredFormatter",
            # 日志格式，重点是%(request_id)s， 其他按照自己喜好来
            "format": "%(green)s%(asctime)s [%(request_id)s] %(name)s %(log_color)s%(levelname)s [pid:%(process)d][threadid:%(thread)d] "
            "[%(filename)s->%(funcName)s:%(lineno)s] %(cyan)s%(message)s",
        },
    },
    "filters": {
        "request_id": {"()": "log_request_id.filters.RequestIDFilter"},
    },
    "handlers": {
        "null": {
            "level": "DEBUG",
            "class": "logging.NullHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "color",
            "filters": ["request_id"],
        },
        "filelog": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "color",
            "filename": "./webapp.log",
            "when": "midnight",
            "backupCount": 5,
            "filters": ["request_id"],
        },
    },
    "loggers": {
        "django": {
            "handlers": ["null"],
            "propagate": True,
            "level": "INFO",
        },
        "django.request": {
            "handlers": ["console", "filelog"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console", "filelog"],
            "level": "DEBUG",
        },
        "webapp": {
            "handlers": ["console", "filelog"],
            "propagate": True,
            "level": "INFO",
        },
        "chat_app": {
            "handlers": ["console"],
            "propagate": True,
            "level": "DEBUG",
        },
    },
}

# 允许所有源，生产环境中建议指定具体的源
CORS_ORIGIN_ALLOW_ALL = True
# 或者指定允许的源
# CORS_ORIGIN_WHITELIST = [
#     'http://localhost:3000',
#     'https://yourdomain.com'
# ]

# 允许特定的HTTP方法
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

# 允许特定的HTTP头：
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
