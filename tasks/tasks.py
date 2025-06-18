from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Task

@shared_task
def send_notification(task_id):
    task = Task.objects.get(id=task_id)
    subject = f'Напоминание: {task.title}'
    message = f'У вас запланирована задача: {task.title}\nОписание: {task.description}'
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [task.user.email],
        fail_silently=False,
    )