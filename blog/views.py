from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Blog, BlogPost, Like
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
    owner = post.blog.author
    likecount = Like.objects.filter(post=post).count()
    context = {
        'post': post,
        'owner': owner,
        'likecount': likecount,
    }
    try:
        # Checks if user has like and sets the context variable accordingly
        user_has_liked = Like.objects.filter(post=post, user=request.user)
        if not user_has_liked:
            context['user_has_liked'] = False
        else:
            context['user_has_liked'] = True
    except TypeError as e:
        # In case user is not logged in, above would give a TypeError.
        # Just default the context variable to False
        context['user_has_liked'] = False
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
            return redirect('users:profile', user_id=request.user.id)
    context = {'form': form}
    return render(request, "new_blog.html", context)


@login_required
def new_post(request, blog_id):
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
            return redirect('blog:blog', blog_id=blog_id)

    context = {
        'blog': blog,
        'form': form
    }
    return render(request, "new_post.html", context)


@login_required
def edit_blog(request, blog_id):
    """View for editing an existing blog."""
    # Fetch blog to be edited
    blog = get_object_or_404(Blog, id=blog_id)

    if blog.author != request.user:
        raise Http404

    if request.method != "POST":
        form = BlogForm(instance=blog)
    else:
        form = BlogForm(instance=blog, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:blog', blog_id=blog.id)
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

    if blog.author != request.user:
        raise Http404

    # If the user has pressed the confirmation button
    if request.method == "POST":
        blog.delete()
        return redirect('users:profile', user_id=request.user.id)
    else:
        context = {'blog': blog}
        return render(request, "confirm_delete_blog.html", context)


@login_required
def edit_post(request, post_id):
    """View for editing a post in a blog."""
    post = get_object_or_404(BlogPost, id=post_id)

    blog = post.blog
    if blog.author != request.user:
        raise Http404

    if request.method != 'POST':
        form = BlogPostForm(instance=post)
    else:
        form = BlogPostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:blogpost', post_id=post.id)

    context = {
        'post': post,
        'blog': blog,
        'form': form
    }
    return render(request, 'edit_post.html', context)


@login_required
def delete_post(request, post_id):
    """View for deleting a post"""
    post = get_object_or_404(BlogPost, id=post_id)
    blog = post.blog

    if blog.author != request.user:
        raise Http404

    if request.method == 'POST':
        post.delete()
        return redirect('blog:blog', blog_id=blog.id)
    else:
        context = {'post': post}
        return render(request, 'confirm_delete_post.html', context)


@login_required
def like(request, post_id):
    """When user likes a post."""
    post = get_object_or_404(BlogPost, id=post_id)
    user = request.user
    # Tries to get like, if it doesn't exist create it.
    new_like, created = Like.objects.get_or_create(post=post, user=user)
    if not created:
        # User had already like and wants to unlike
        new_like.delete()
    # Return user to the post
    return redirect('blog:blogpost', post_id=post.id)



