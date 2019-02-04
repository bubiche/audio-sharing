from .base import *
from .base import INSTALLED_APPS
import os

from queued_storage.backends import QueuedStorage


DEBUG = False
ALLOWED_HOSTS = ['chuc-be-ngu-ngon.herokuapp.com']


# Dropbox storage settings
DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
DROPBOX_OAUTH2_TOKEN = os.environ.get('DROPBOX_OAUTH2_TOKEN', '')
DROPBOX_ROOT_PATH = '/dropbox_api_storage'


# Caches
CACHES = {
    'default': {
        'BACKEND': 'django_bmemcached.memcached.BMemcached',
        'LOCATION': os.environ.get('MEMCACHEDCLOUD_SERVERS').split(','),
        'OPTIONS': {
            'username': os.environ.get('MEMCACHEDCLOUD_USERNAME'),
            'password': os.environ.get('MEMCACHEDCLOUD_PASSWORD')
        }
    }
}


# Queued storage settings
INSTALLED_APPS = INSTALLED_APPS + ['queued_storage']
QUEUED_STORAGE_RETRIES = 2
QUEUED_STORAGE_RETRY_DELAY = 60
