from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=512, unique=True)


class Subscription(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    subscriber = models.CharField(max_length=512, unique=True)
    webhook_endpoint = models.URLField()


class Message(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    payload = models.JSONField()
