from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)      #unique=True, - will enforce the uniqueness of the field at the database level.
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics')     #ForeignKey field. It will create a link between the models and create a proper relationship at the database level. The ForeignKey field expects a positional parameter with the reference to the model it will relate to.
    starter = models.ForeignKey(User, related_name='topics')    #The related_name parameter will be used to create a reverse relationship where the Board instances will have access a list of Topic instances that belong to it.

    def __str__(self):
        return self.subject

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts')
    updated_by = models.ForeignKey(User, null=True, related_name='+')       #related_name='+'. This instructs Django that we don’t need this reverse relationship, so it will ignore it.

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)
