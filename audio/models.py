from django.db import models
from django.core.validators import URLValidator
from django.conf import settings

import uuid
import types
from queued_storage.backends import QueuedStorage

from commons.custom_model_fields import VariableStorageFileField


def get_accessed_time(self, name):
    """
    Django +1.10
    Returns the last accessed time (as datetime object) of the file
    specified by name.
     :param name: file name
    :type name: str
    :rtype: :class:`~python:datetime.datetime`
    """
    return self.get_storage(name).accessed_time(name)


def get_created_time(self, name):
    """
    Django +1.10
    Returns the creation time (as datetime object) of the file
    specified by name.
     :param name: file name
    :type name: str
    :rtype: :class:`~python:datetime.datetime`
    """

    return self.get_storage(name).created_time(name)


def get_modified_time(self, name):
    """
    Django +1.10
    Returns the last modified time (as datetime object) of the file
    specified by name.
     :param name: file name
    :type name: str
    :rtype: :class:`~python:datetime.datetime`
    """

    return self.get_storage(name).modified_time(name)


def generate_filename(self, filename):
    return self.get_storage(filename).generate_filename(filename)


def get_default_storage():
    if settings.DEBUG:
        return None

    storage = QueuedStorage(
        'django.core.files.storage.FileSystemStorage',
        'storages.backends.dropbox.DropBoxStorage', task='queued_storage.tasks.TransferAndDelete')

    storage.get_accessed_time = types.MethodType(get_accessed_time, storage)
    storage.get_created_time = types.MethodType(get_created_time, storage)
    storage.get_modified_time = types.MethodType(get_modified_time, storage)
    storage.generate_filename = types.MethodType(generate_filename, storage)
    return storage


class AudioUpload(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    # either an uploaded file or a url
    storage = get_default_storage()
    file = VariableStorageFileField(upload_to='audio_records', blank=True, null=True, storage=storage)
    direct_url = models.TextField(validators=[URLValidator()], blank=True, null=True)  # I just prefer this to URLField :/
