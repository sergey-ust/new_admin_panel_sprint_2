"""Project Database settings."""

import os

_DB_DEFAULT_IP = '127.0.0.1'
_DB_DEFAULT_PORT = 5432

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', _DB_DEFAULT_IP),
        'PORT': os.environ.get('DB_PORT', _DB_DEFAULT_PORT),
        'OPTIONS': {
            # Add our 'content' schem
            'options': '-c search_path=public,content',
        },
    },
}
