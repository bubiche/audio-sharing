from django.urls import path

from audio.views import audio_record, audio_playback


urlpatterns = [
    path('', audio_record),
    path('play/<slug:audio_uuid>/', audio_playback),
]
