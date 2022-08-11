from django.db import models

class User(models.Model):
    username = models.CharField
    password = models.CharField

class Topic(models.Model):
    title = models.CharField
    text = models.CharField
    visible = models.BooleanField(default=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)

class Message(models.Model):
    text = models.CharField
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    visible = models.BooleanField(default=True)
