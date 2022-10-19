from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from posts.models import Group, Post, User
from posts.forms import PostForm

LIMIT_POSTS = 10


def index(request: HttpRequest) -> HttpResponse:
    """
    Отрисовка главной страницы с 10 последними статьями.
    Принимает WSGIRequest и возвращает подготовленную
    html страницу с данными.
    """
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'posts/index.html',
        {'page_obj': page_obj},
    )


def group_posts(request: HttpRequest, slug: str) -> HttpResponse:
    """
    Отрисовка страницы группы с 10 последними статьями данной группы.
    Принимает WSGIRequest, наименование группы в формате slug
    и возвращает подготовленную html страницу с данными.
    """
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'posts/group_list.html',
        {'group': group, 'page_obj': page_obj},
    )


def profile(request: HttpRequest, username: str) -> HttpResponse:
    """
    Отрисовка страницы профиля пользователя с информацией
    обо всех постах данного пользователя.
    """
    requested_user = User.objects.get(username=username)
    post_list = Post.objects.filter(author=requested_user).all()
    number_of_posts = Post.objects.filter(author=requested_user).count()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'posts/profile.html',
        {
            'page_obj': page_obj,
            'profile_user': requested_user,
            'count_posts_profile': number_of_posts,
        },
    )


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    """
    Отрисовка страницы с описанием конкретного выбранного поста.
    """
    unique_post = Post.objects.get(pk=post_id)
    number_of_posts = Post.objects.filter(author=unique_post.author).count()
    return render(
        request,
        'posts/post_detail.html',
        {
            'unique_post': unique_post,
            'number_of_posts': number_of_posts,
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
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            author = User.objects.get(pk=request.user.id)
            post = Post(
                text=form.cleaned_data['text'],
                author=author,
                group=form.cleaned_data['group'])
            post.save()
            return redirect('posts:profile', author.username)
    else:
        form = PostForm()
    return render(
        request, 'posts/create_post.html', {'form': form, 'is_edit': False},
    )


@login_required
def post_edit(request: HttpRequest, post_id: int) -> HttpResponse:
    """
    Отрисовка страницы для редактирования уже созданного поста.
    Пост может редактировать только авторизованный пользователь.
    Редактировать можно только свои посты.
    """
    unique_post = get_object_or_404(Post, pk=post_id)
    if unique_post.author != request.user:
        return redirect('posts:post_detail', post_id)
    form = PostForm(request.POST or None, instance=unique_post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    return render(
        request, 'posts/create_post.html', {'form': form, 'is_edit': True},
    )
