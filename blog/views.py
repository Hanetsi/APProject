from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Blog, BlogPost
from .forms import BlogForm, BlogPostForm


def home(request):
    """Homepage"""
    # Show the last 5 blogs modified.
    recent_blogs = Blog.objects.all().order_by('date_modified').reverse()[:5]
    context = {'recent_blogs': recent_blogs}
    return render(request, "home.html", context)


def blog(request, blog_id):
    """View for a single blog"""
    blog = get_object_or_404(Blog, id=blog_id)
    posts = BlogPost.objects.all().filter(blog=blog).order_by('date_modified').reverse()
    context = {
        'owner': blog.author,
        'blog': blog,
        'posts': posts
    }
    return render(request, "blog.html", context)


def all_blogs(request):
    """View for listing all blogs."""
    blogs = Blog.objects.all().order_by('date_modified').reverse()
    context = {'blogs': blogs}
    return render(request, "all_blogs.html", context)

def blog_post(request, post_id):
    """View for a single post"""
    post = get_object_or_404(BlogPost, id=post_id)
    context = {'post': post}
    return render(request, "post.html", context)


@login_required
def new_blog(request):
    """View for creating a new blog."""
    if request.method != "POST":
        form = BlogForm()
    else:
        form = BlogForm(data=request.POST)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.author = request.user
            new_blog.save()
            return redirect('users:profile', user_id = request.user.id)
    context = {'form': form}
    return render(request, "new_blog.html", context)

@login_required
def new_post(request,blog_id):
    """View for adding a new post to a existing blog."""
    blog = Blog.objects.get(id=blog_id)

    if request.method != 'POST':
        form = BlogPostForm()
    else:
        form = BlogPostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.blog = blog
            new_post.save()
            return redirect('blog:blog',blog_id=blog_id)

    context = {'blog':blog, 'form':form }
    return render(request, "new_post.html" ,context)

@login_required
def edit_blog(request, blog_id):
    """View for editing an existing blog."""
    # Fetch blog to be edited
    blog = get_object_or_404(Blog, id=blog_id)

    if request.method != "POST":
        form = BlogForm(instance=blog)
    else:
        form = BlogForm(instance=blog, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:profile', user_id=request.user.id)
    context = {
        'form': form,
        'blog': blog,
        }
    return render(request, "edit_blog.html", context)


@login_required
def delete_blog(request, blog_id):
    """View for deleting a blog."""
    # Fetch blog in question
    blog = get_object_or_404(Blog, id=blog_id)
    # If the user has pressed the confirmation button
    if request.method == "POST":
        blog.delete()
        return redirect('users:profile', user_id=request.user.id)
    else:
        context = {'blog': blog}
        return render(request, "confirm_delete_blog.html", context)
