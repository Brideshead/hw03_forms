from django.contrib import admin
from django.urls import include, path

from posts.apps import PostsConfig

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls', namespace=PostsConfig.name)),
    path('auth/', include('users.urls', namespace='auth')),
    path('auth/', include('django.contrib.auth.urls')),
    path('about/', include('about.urls', namespace='about')),
]
