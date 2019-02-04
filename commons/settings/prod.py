from .base import *
import os


DEBUG = False
ALLOWED_HOSTS = ['chuc-be-ngu-ngon.herokuapp.com']

DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
DROPBOX_OAUTH2_TOKEN = os.environ.get('DROPBOX_OAUTH2_TOKEN', '')
DROPBOX_ROOT_PATH = '/dropbox_api_storage'

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
