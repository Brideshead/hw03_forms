from django.urls import path

from posts import views
from posts.apps import PostsConfig

app_name = PostsConfig.name

urlpatterns = [
    path('', views.index, name='index'),
    path('group/<slug:slug>/', views.group_posts, name='group_list'),
]
