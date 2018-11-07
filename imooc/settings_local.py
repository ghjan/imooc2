# _*_ coding: utf-8 _*_

import datetime
import os

print('enter settings_local')

try:
    DB_HOST = 'localhost'
    DB_PASSWORD = '123456'

    print('DB_HOST:', DB_HOST)
    print('DB_PASSWORD:', DB_PASSWORD)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': "imooc",
            "USER": "root",
            "PASSWORD": DB_PASSWORD,
            "HOST": DB_HOST,
        }
    }
except Exception as e:
    print('settings_local,exception', e)
    import traceback

    print(traceback.print_exc())
