from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    """
    Модель для хранения данных сообществ.

    title: название группы.
    slug: уникальный адрес группы, часть URL.
    description: текст, описывающий сообщество.
    """

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(cls) -> str:
        return f'{cls.title}'


class Post(models.Model):
    """
    Модель для хранения статей.

    text: текс статьи.
    pud_date: дата публикации статьи.
    author: автор статьи, установлена связь с таблицей User,
    при удалении из таблицы User автора,
    также будут удалены все связанные статьи.
    group: название сообщества, к которому относится статья,
    установлена связь с моделью Group, чтобы при добавлении
    новой записи можно было сослаться на данную модель.
    """

    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts')
    group = models.ForeignKey(
        Group, blank=True, null=True,
        on_delete=models.CASCADE,
    )
