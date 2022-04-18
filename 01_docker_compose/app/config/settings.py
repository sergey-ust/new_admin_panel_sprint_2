"""Project settings."""

import os

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

DEBUG = os.environ.get('DEBUG', False) == 'True'

include(
    'components/base.py',
    'components/database.py',
    'components/local.py',
    'components/apps.py',
)
if DEBUG and os.environ.get('SQL_LOGGING', False) == 'True':
    include('components/log.py')

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['127.0.0.1']

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
            'django.contrib.auth.password_validation.' +
            'UserAttributeSimilarityValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = [
    "127.0.0.1",
]
