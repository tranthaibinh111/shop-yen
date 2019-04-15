from celery import shared_task


@shared_task
def hello():
    print("Hello there!")


@shared_task
def test2():
    print("Binh-TT")
