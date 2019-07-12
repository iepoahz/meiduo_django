"""
Django settings for meiduo_mall project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys
import djcelery

#todo 项目路径
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#todo 更改python解释器导包路径，从应用文件夹apps导包  无
sys.path.insert(0,os.path.join(BASE_DIR,"apps"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '453!mx7@o^!k8#=)s@xr@j=o3=32=y0o-*me=pfvv#lt+8^abp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#todo 添加后端接口地址
ALLOWED_HOSTS = ["api.meiduo.com","127.0.0.1"]


# Application definition

#todo 注册应用
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',   #注册rest_framework应用,后期调用API web测试
    'corsheaders',  #跨域请求第三方库django-cors-headers==2.4.0
    'users.apps.UsersConfig', #子应用users
    'verifications.apps.VerificationsConfig', #子应用verifications
    'djcelery' #异步任务队列



]
#todo 中间件设置
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',#跨域请求第三方库django-cors-headers==2.4.0
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#todo 主url控制配置
ROOT_URLCONF = 'meiduo_mall.urls'

#todo 模板配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'meiduo_mall.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
#todo 数据库配置
DATABASES = {
    'default': {
        #默认配置
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # todo mysql配置
        'ENGINE':'django.db.backends.mysql', #引擎
        'HOST':'127.0.0.1',
        'PORT':3306,
        'USER':'root',
        'PASSWORD':'mysql',
        'NAME':'meiduo_mall',
    }
}
#todo Redis数据库配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",#后端
        "LOCATION": "redis://127.0.0.1/1",#地址
        "OPTIONS": {   #选择
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 子应用 verifications  图片验证码  短信验证码
    "verify_codes": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

#todo session配置
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = 'session' #缓存别名
# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
#todo 语言
LANGUAGE_CODE = 'zh-hans'


#todo 时区
TIME_ZONE = 'Asia/Shanghai'


#todo 日志配置
LOGGING ={
    'version':1,
    'disable_existing_loggers':False,
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/meiduo.log"),  # 日志文件的位置 '/project/django/meiduo_mall/logs/meiduo.log'
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'DEBUG',  # 日志器接收的最低日志级别
        },
    },
}

#todo 异常配置
REST_FRAMEWORK = {
    "EXCEPTION_HANDLER":"meiduo_mall.utils.exceptions.exception_handler",
}


#todo 添加白名单
CORS_ORIGIN_WHITELIST = (
    "127.0.0.1:8080",
    "localhost:8080",
    "www.meiduo.com:8080",
    "www.wurenlingyu.cn:8080",
    "127.0.0.1:8000",
    "api.meiduo.com:8000"
)

#todo 允许携带COOKIE
CORS_ALLOW_CREDENTIALS = True

#todo django  认证系统使用的模型类
AUTH_USER_MODEL ="users.User"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

#todo 静态文件配置
STATIC_URL = '/static/'  #url路径
STATICFILES_DIRS = [  #文件路径
    os.path.join(BASE_DIR, 'front_end'), #'.../meiduo_mall/meiduo_mall/front_end'
]

#todo celery 异步任务队列

djcelery.setup_loader()
# 任务队列 broker_url
BROKER_URL= "redis://127.0.0.1/14"
# 异步结果 result_backend
CELERY_RESULT_BACKEND = "redis://127.0.0.1/15"