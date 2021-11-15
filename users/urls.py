"""users url configs"""
from django.urls import path, include
from . import views
app_name = "users"
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('delete_user/<int:user_id>', views.delete_user, name='delete_user')
]
