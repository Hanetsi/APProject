from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import Http404
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


@login_required
def delete_user(request, user_id):
    """View for deleting user's profile"""
    # Fetch user in question
    user = get_object_or_404(User, id=user_id)
    # Check if user is logged in with the user they are trying to delete.
    if user != request.user:
        raise Http404
    # If the user has pressed the confirmation button
    if request.method == "POST":
        user.delete()
        return redirect('blog:home')
    else:
        context = {'user': user}
        return render(request, "confirm_delete_user.html", context)
