from django.urls import path

from audio.views import audio_record


urlpatterns = [
    path('', audio_record),
]
