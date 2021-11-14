from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from blog.models import Blog, BlogPost


def register(request):
    """Register a new user."""
    if request.method != "POST":
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('blog:home')
    context = {
        'form': form
    }
    return render(request, "registration/register.html", context)


def profile(request, user_id):
    """Shows users profile. View depends on if the user views their own or someone else's profile"""
    user = User.objects.get(id=user_id)
    blogs = Blog.objects.filter(author=user).order_by("date_modified").reverse()
    context = {
        'owner': user,
        'blogs': blogs
    }
    return render(request, "profile.html", context)
