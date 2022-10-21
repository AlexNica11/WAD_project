from django.db import models


class HubPageDataModel(models.Model):
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    date_end = models.CharField(max_length=255, default='empty')
    description = models.TextField(default='empty')
    text = models.TextField()
