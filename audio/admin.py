from django.contrib import admin
from audio.models import AudioUpload


@admin.register(AudioUpload)
class AudioUploadAdmin(admin.ModelAdmin):
    list_display = ('audio_uuid', 'name')
    search_fields = ['name']
