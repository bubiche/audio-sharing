from celery import shared_task


@shared_task
def test_background_task():
    print('Async worker is alive!')
