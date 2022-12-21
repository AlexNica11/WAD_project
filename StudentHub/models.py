from django.db import models
from django.contrib.auth.models import User


class HubPageDataModel(models.Model):
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    date = models.DateTimeField(['%Y-%m-%d %H:%M'], max_length=255)
    date_end = models.DateTimeField(['%Y-%m-%d %H:%M'], max_length=255, default='2000-01-01 10:10')
    description = models.TextField(default='empty')

    @property
    def ending_date(self):
        return self.date_end

    def __str__(self):
        return self.title


class ChatMessages(models.Model):
    messageText = models.TextField()
    user = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    room_id = models.CharField(max_length=255)
    hubpagedatamodel = models.ForeignKey(HubPageDataModel, on_delete=models.CASCADE, null=False, default=0)

    def __str__(self):
        return self.messageText


class Contacts(models.Model):
    full_name = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=12)
    dev_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default=0)

    def __str__(self):
        return self.full_name


class Questions(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField(default='empty')
    date = models.DateTimeField(['%Y-%m-%d %H:%M'], max_length=255)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default=0)
    contact_id = models.ForeignKey(Contacts, on_delete=models.CASCADE, null=False, default=0)
