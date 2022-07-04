"""Defines URL patterns for blogs."""

from django.urls import path, include
from . import views

app_name = 'blogs'
urlpatterns = [
    # Home page when not logged in
    path('', views.index, name='index'), # New

    # Home page when logged in
    path('homepage/', views.homepage, name='homepage'), # New

    # Page for adding a new blog post
    path('new_post/', views.new_post, name='new_post'),

    # Page for edditing a post.
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
]