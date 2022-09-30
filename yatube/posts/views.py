from django.shortcuts import render, get_object_or_404
from .models import Post, Group

# Константа устанавливающая количество постов на странице.
LIMIT_POSTS = 10


def index(request):
    """
    Отрисовка главной страницы с 10 последними статьями.
    Принимает WSGIRequest и возвращает подготовленную
    html страницу с данными.
    """
    template = 'posts/index.html'
    posts = Post.objects.order_by('-pub_date')[:LIMIT_POSTS]
    context = {'posts': posts}
    return render(request, template, context)


def group_posts(request, slug):
    """
    Отрисовка страницы группы с 10 последними статьями данной группы.
    Принимает WSGIRequest, наименование группы в формате slug
    и возвращает подготовленную html страницу с данными.
    """
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[
        :LIMIT_POSTS
    ]

    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)
