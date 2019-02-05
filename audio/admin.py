from django.contrib import admin
from audio.models import AudioUpload, AudioFile


@admin.register(AudioUpload)
class AudioUploadAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name')
    search_fields = ['name']


@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'mime_type')
