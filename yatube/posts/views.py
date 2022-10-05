from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from posts.models import Group, Post

LIMIT_POSTS = 10


def index(request: HttpRequest) -> HttpResponse:
    """
    Отрисовка главной страницы с 10 последними статьями.
    Принимает WSGIRequest и возвращает подготовленную
    html страницу с данными.
    """
    posts = Post.objects.all()[:LIMIT_POSTS]
    return render(request, 'posts/index.html', {'posts': posts})


def group_posts(request: HttpRequest, slug: str) -> HttpResponse:
    """
    Отрисовка страницы группы с 10 последними статьями данной группы.
    Принимает WSGIRequest, наименование группы в формате slug
    и возвращает подготовленную html страницу с данными.
    """
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:LIMIT_POSTS]
    return render(
        request, 'posts/group_list.html', {'group': group, 'posts': posts},
    )
