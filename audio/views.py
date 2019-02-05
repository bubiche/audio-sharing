from django.shortcuts import render
from django.http import HttpResponse

from audio.models import AudioUpload


def audio_record(request):
    return render(request, 'audio/audio_record.html')


def audio_playback(request, audio_uuid):
    try:
        audio_upload = AudioUpload.objects.filter(audio_uuid=audio_uuid).first()
        if not audio_upload:
            return HttpResponse('Sorry, I don\'t have what you are looking for')
    except Exception:
        return HttpResponse('This path leads to nowhere')

    audio_url = audio_upload.s3_file or audio_upload.direct_url
    if not audio_url:
        return HttpResponse('It seems what you are looking for is removed :/')

    return render(request, 'audio/audio_playback.html', {
        'audio_url': audio_url,
        'audio_name': audio_upload.name
    })
