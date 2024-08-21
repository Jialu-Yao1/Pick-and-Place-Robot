from celery import shared_task


@shared_task()
def automate():
    print("Celery task")
    pass