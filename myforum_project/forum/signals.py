from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MessageRating, Notification

@receiver(post_save, sender=MessageRating)
def create_notification(sender, instance, **kwargs):
    if instance.user != instance.message.created_by:
        message = f"Your message in topic '{instance.message.topic.title}' was rated {instance.rating} by {instance.user.username}."
        Notification.objects.create(user=instance.message.created_by, message=message)