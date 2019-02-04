from .base import *
import os


DEBUG = False
ALLOWED_HOSTS = ['chuc-be-ngu-ngon.herokuapp.com']

DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
DROPBOX_OAUTH2_TOKEN = os.environ.get('DROPBOX_OAUTH2_TOKEN', '')
DROPBOX_ROOT_PATH = '/dropbox_api_storage'
