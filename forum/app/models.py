from django.db import models

class User(models.Model):
    username = models.CharField(max_length=20, default='')
    password = models.CharField(max_length=20, default='')
    moderator = models.BooleanField(default=False)

class Topic(models.Model):
    title = models.CharField(max_length=100, default='')
    text = models.CharField(max_length=1000, default='')
    visible = models.BooleanField(default=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)

class Message(models.Model):
    text = models.CharField(max_length=1000, default='')
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    visible = models.BooleanField(default=True)
