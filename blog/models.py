from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    """Model for a blog. Blog will consist of posts with many to one relationship."""
    name = models.CharField(max_length=100, unique=True, default="")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " | " + str(self.date_added.date())


class BlogPost(models.Model):
    """Model of a post in a blog."""
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    """Unique parameter makes sure there cannot be two blogs with same name"""
    title = models.CharField(max_length=200, unique=True, default="")
    content = models.TextField(default="")
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + " | " + str(self.date_modified.date())
