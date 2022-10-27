from django.db import models


class HubPageDataModel(models.Model):
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    date = models.DateTimeField(['%Y-%m-%d %H:%M'], max_length=255)
    date_end = models.DateTimeField(['%Y-%m-%d %H:%M'], max_length=255, default='empty')
    description = models.TextField(default='empty')

    def __str__(self):
        return self.title


class ChatMessages(models.Model):
    messageText = models.TextField()
    user = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    room_id = models.CharField(max_length=255)

    def __str__(self):
        return self.messageText