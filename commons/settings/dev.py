from .base import *
from celery import current_app


# allow other devices in the same network to access dev site
ALLOWED_HOSTS = ['*']
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}


# in dev mode, just run background tasks synchronously
CELERY_ALWAYS_EAGER = True
current_app.conf.CELERY_ALWAYS_EAGER = True

# https://github.com/celery/django-celery/issues/75
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
current_app.conf.CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
