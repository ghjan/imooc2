"""
Django settings for imooc project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '123456')

# Build paths inside the imooc like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, os.path.join(BASE_DIR, 'imooc'))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'external_data'))
sys.path.insert(0, os.path.join(BASE_DIR, 'libs'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-3b$%7hb72t34xbe@m3h%y_0jt#*ob*(f(7kw*#6bh(s*av661'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['www.davidzhang.xin', '106.14.202.116', 'localhost', '0.0.0.0']

AUTHENTICATION_BACKENDS = (
    'users.authentication.CustomBackend',  # 支持用户名/邮箱/手机号码登录
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'xadmin',
    'captcha',
    'crispy_forms',
    'reversion',
    'pure_pagination',

    "users",
    "courses",
    "organization",
    "operation",
]
AUTH_USER_MODEL = "users.UserProfile"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'imooc.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "imooc",
        "USER": "root",
        "PASSWORD": DB_PASSWORD,
        "HOST": DB_HOST,
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'  # ''en-us'

TIME_ZONE = 'Asia/Shanghai'  # 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False  # 是否utc时间（数据库模型）

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'common_static'),
                    # os.path.join(BASE_DIR, 'media'),
                    )

# media
MEDIA_URL = '/media/'  # 这个是在浏览器上访问该上传文件的url的前缀
MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace("\\", "/")

EMAIL_HOST = "smtp.sina.com"
EMAIL_PORT = 25
EMAIL_HOST_USER = 'cajan2@sina.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = False
DEFAULT_CHARSET = 'utf-8'
EMAIL_FROM = EMAIL_HOST_USER

PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 10,
    'MARGIN_PAGES_DISPLAYED': 2,

    'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}

try:
    from .settings_local import *
except Exception as e:
    print(e)
