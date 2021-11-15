"""blog app's url configs"""
from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path('', views.home, name="home"),
    path('blog/<int:blog_id>', views.blog, name="blog"),
    path('all_blogs/', views.all_blogs, name="all_blogs"),
    path('blogpost/<int:post_id>', views.blog_post, name="blogpost"),
    path('new_blog/', views.new_blog, name="new_blog"),
    path('edit_blog/<int:blog_id>', views.edit_blog, name="edit_blog"),
    path('delete_blog/<int:blog_id>', views.delete_blog, name="delete_blog"),
    path('new_post/<int:blog_id>', views.new_post, name="new_post"),
    path('edit_post/<int:post_id>', views.edit_post, name="edit_post"),
    path('delete_post/<int:post_id>', views.delete_post, name="delete_post"),
    path('like/<int:post_id>', views.like, name="like_post"),
]
