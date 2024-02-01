from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Section(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Topic(models.Model):
    title = models.CharField(max_length=255)
    section = models.ForeignKey('Section', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Message(models.Model):
    content = models.TextField()
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    ratings = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.created_by.username}'s message in {self.topic.title}"
    
class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} to {self.recipient.username} at {self.created_at}"
    

class Attachment(models.Model):
    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} - {self.uploaded_by.username} at {self.uploaded_at}"
    
class Rating(models.Model):
    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} rated {self.message.id} with {self.value}"
    

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} subscribed to {self.topic.title}"
    
class MessageRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} rated {self.message.content} ({self.rating})"
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.message}"
    
