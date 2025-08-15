from django.db import models
from rest_framework.views import APIView


# Create your models here.
class Feed(models.Model):
    content       = models.TextField()
    image         = models.TextField()
    email         = models.EmailField()

class Like(models.Model):
    feed_id = models.IntegerField()
    email = models.EmailField()
    is_like = models.BooleanField()


class Reply(models.Model):
    feed_id = models.IntegerField()
    email = models.EmailField()
    reply_content = models.TextField()

class Bookmark(models.Model):
    feed_id = models.IntegerField()
    email = models.EmailField()
    is_marked = models.BooleanField()


