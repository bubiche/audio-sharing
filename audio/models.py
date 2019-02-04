from django.db import models
from django.core.validators import URLValidator
from django.conf import settings

import uuid
from queued_storage.backends import QueuedStorage

from commons.custom_model_fields import VariableStorageFileField


def get_default_storage():
    if settings.DEBUG:
        return None

    return QueuedStorage(
        'django.core.files.storage.FileSystemStorage',
        'storages.backends.dropbox.DropBoxStorage', task='queued_storage.tasks.TransferAndDelete')


class AudioUpload(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    # either an uploaded file or a url
    storage = get_default_storage()
    file = VariableStorageFileField(upload_to='audio_records', blank=True, null=True, storage=storage)
    direct_url = models.TextField(validators=[URLValidator()], blank=True, null=True)  # I just prefer this to URLField :/
