from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from core.utils import paginate
from posts.forms import PostForm
from posts.models import Group, Post, User

LIMIT_POSTS = 10


def index(request: HttpRequest) -> HttpResponse:
    """
    Отрисовка главной страницы с 10 последними статьями.
    Принимает WSGIRequest и возвращает подготовленную
    html страницу с данными.
    """
    page_obj = paginate(Post.objects.select_related('group'), request)
    return render(
        request,
        'posts/index.html',
        {
            'page_obj': page_obj,
        },
    )


def group_posts(request: HttpRequest, slug: str) -> HttpResponse:
    """
    Отрисовка страницы группы с 10 последними статьями данной группы.
    Принимает WSGIRequest, наименование группы в формате slug
    и возвращает подготовленную html страницу с данными.
    """
    group = get_object_or_404(Group, slug=slug)
    page_obj = paginate(group.posts.all(), request)
    return render(
        request,
        'posts/group_list.html',
        {
            'group': group, 'page_obj': page_obj,
        },
    )


def profile(request: HttpRequest, username: str) -> HttpResponse:
    """
    Отрисовка страницы профиля пользователя с информацией
    обо всех постах данного пользователя.
    """
    requested_user = get_object_or_404(User, username=username)
    page_obj = paginate(
        Post.objects.select_related('author').filter(
            author=requested_user,
        ),
        request,
    )
    return render(
        request,
        'posts/profile.html',
        {
            'page_obj': page_obj,
            'profile_user': requested_user,
        },
    )


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    """
    Отрисовка страницы с описанием конкретного выбранного поста.
    """
    unique_post = get_object_or_404(Post, pk=post_id)
    return render(
        request,
        'posts/post_detail.html',
        {
            'unique_post': unique_post,
        },
    )


@login_required
def post_create(request: HttpRequest) -> HttpResponse:
    """
    Отрисовка страницы с окном создания поста.
    Можно указать текст поста и выбрать группу,
    к которой данный пост будет относиться.
    Посты могут создавать только авторизованные пользователи.
    """
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', post.author)

    return render(
        request,
        'posts/create_post.html',
        {
            'form': form, 'is_edit': False,
        },
    )


@login_required
def post_edit(request: HttpRequest, post_id: int) -> HttpResponse:
    """
    Отрисовка страницы для редактирования уже созданного поста.
    Пост может редактировать только авторизованный пользователь.
    Редактировать можно только свои посты.
    """
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id)

    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)

    return render(
        request, 'posts/create_post.html', {'form': form, 'is_edit': True},
    )
