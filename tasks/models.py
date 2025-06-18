from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

class Category(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=12,
        validators=[MinLengthValidator(12)],
        editable=False
    )
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = get_random_string(12)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Task(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=12,
        validators=[MinLengthValidator(12)],
        editable=False
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    categories = models.ManyToManyField(Category, blank=True, related_name='tasks')

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = get_random_string(12)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

@receiver(post_save, sender=Task)
def schedule_notification(sender, instance, created, **kwargs):
    if instance.due_date:
        from .tasks import send_notification
        send_notification.apply_async(
            args=[instance.id],
            eta=instance.due_date
        )