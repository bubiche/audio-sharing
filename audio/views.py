from django.shortcuts import render


def audio_record(request):
    return render(request, 'audio/audio_record.html')
