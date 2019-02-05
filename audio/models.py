from django.db import models
from django.core.validators import URLValidator
from django.conf import settings

import uuid
import types
from queued_storage.backends import QueuedStorage
from db_file_storage.model_utils import delete_file, delete_file_if_needed

from commons.custom_model_fields import VariableStorageFileField


'''
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


def storage_save(self, name, content, max_length=None):
    """
    Saves the given content with the given name using the local
    storage. If the :attr:`~queued_storage.backends.QueuedStorage.delayed`
    attribute is ``True`` this will automatically call the
    :meth:`~queued_storage.backends.QueuedStorage.transfer` method
    queuing the transfer from local to remote storage.
    :param name: file name
    :type name: str
    :param content: content of the file specified by name
    :type content: :class:`~django:django.core.files.File`
    :rtype: str
    """
    cache_key = self.get_cache_key(name)
    cache.set(cache_key, False)

    # Use a name that is available on both the local and remote storage
    # systems and save locally.
    name = self.get_available_name(name)
    try:
        name = self.local.save(name, content, max_length=max_length)
    except TypeError:
        # Django < 1.10
        name = self.local.save(name, content)

    # Pass on the cache key to prevent duplicate cache key creation,
    # we save the result in the storage to be able to test for it
    if not self.delayed:
        self.result = self.transfer(name, cache_key=cache_key)
    return name
'''


def get_default_storage():
    if settings.DEBUG:
        return None

    # save to database first then upload to dropbox in background worker
    storage = QueuedStorage(
        'db_file_storage.storage.DatabaseFileStorage',
        'storages.backends.dropbox.DropBoxStorage', task='queued_storage.tasks.TransferAndDelete')

    # storage.get_accessed_time = types.MethodType(get_accessed_time, storage)
    # storage.get_created_time = types.MethodType(get_created_time, storage)
    # storage.get_modified_time = types.MethodType(get_modified_time, storage)
    # storage.generate_filename = types.MethodType(generate_filename, storage)
    # storage.save = types.MethodType(storage_save, storage)
    return storage


class AudioUpload(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    # either an uploaded file or a url
    storage = get_default_storage()
    file = VariableStorageFileField(upload_to='audio.AudioFile/content/file_name/mime_type', blank=True, null=True, storage=storage)
    direct_url = models.TextField(validators=[URLValidator()], blank=True, null=True)  # I just prefer this to URLField :/

    def save(self, *args, **kwargs):
        delete_file_if_needed(self, 'file')
        super(AudioUpload, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(AudioUpload, self).delete(*args, **kwargs)
        delete_file(self, 'file')


class AudioFile(models.Model):
    content = models.TextField()
    file_name = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=50)
