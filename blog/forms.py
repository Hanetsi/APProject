"""Forms for Blog and BlogPost"""
from django import forms

from .models import Blog, BlogPost


class BlogForm(forms.ModelForm):
    """Form for creating or editing blogs."""
    class Meta:
        model = Blog
        fields = ['name', 'description']
        labels = {
            'name': 'Name for new blog',
            'description': 'A short blog description'
        }


class BlogPostForm(forms.ModelForm):
    """Form for creating or editing blogs."""
    class Meta:
        model = BlogPost
        fields = ['title', 'content']
        labels = {
            'title': 'Post title',
            'content': '',
        }

