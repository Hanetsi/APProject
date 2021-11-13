from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Blog(models.Model):
    name = models.CharField(max_length=100,unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + " | " +  str(self.date_added.date())

class BlogPost(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    """Unique parmeter makes sure there cannot be two blogs whit same name"""
    blogpost_title = models.CharField(max_length=200, unique=True)
    blogpost_content = models.CharField(max_length=2000)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return self.blogpost_title + " | " + str(self.date_modified.date())
