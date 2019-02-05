from django.db import models
from django.core.validators import URLValidator
from django.conf import settings

import uuid
from s3direct.fields import S3DirectField


class AudioUpload(models.Model):
    audio_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, db_index=True)

    # either an uploaded file or a url
    # dest is 1 of the destinations in settings.S3DIRECT_DESTINATIONS
    s3_file = S3DirectField(dest='my_s3_destination', blank=True, null=True)  # this will actually store just the direct url to the file on s3
    direct_url = models.TextField(validators=[URLValidator()], blank=True, null=True)  # I just prefer this to URLField :/
