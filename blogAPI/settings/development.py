from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

ADMIN_ENABLED = True

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

REST_AUTH = {
    'USE_JWT': True,                                        # dj_rest_auth.views.LoginView use JWT
    'JWT_AUTH_HTTPONLY': False,
    'JWT_AUTH_COOKIE': "AUTH",
    'JWT_AUTH_REFRESH_COOKIE': "REFRESH",
    'JWT_AUTH_COOKIE_USE_CSRF': False,
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',  # 디버그 레벨로 설정
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',  # 요청 관련 로그
            'propagate': True,
        },
        'allauth': {
            'handlers': ['console'],
            'level': 'DEBUG',  # Allauth 관련 디버깅 정보
            'propagate': True,
        },
        'django.security': {
            'handlers': ['console'],
            'level': 'DEBUG',  # 보안 관련 로그
            'propagate': True,
        },
        'requests_oauthlib': {
            'handlers': ['console'],
            'level': 'DEBUG',  # OAuth 인증 요청 및 응답 로그
            'propagate': True,
        },
    },
}


# Elasticsearch configuration

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200'
    },
}