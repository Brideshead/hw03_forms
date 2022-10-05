from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """
    Модель для хранения данных сообществ.

    TITLE_LENGTH_RETURN: ограничение символов на вывод названия группы.

    title: название группы.
    slug: уникальный адрес группы, часть URL.
    description: текст, описывающий сообщество.
    """

    TITLE_LENGTH_RETURN: int = 30

    title = models.CharField(verbose_name='Название группы', max_length=200)
    slug = models.SlugField(verbose_name='Уникальный адрес', unique=True)
    description = models.TextField(verbose_name='Описание группы')

    def __str__(self) -> str:
        return self.title[:self.TITLE_LENGTH_RETURN]


class Post(models.Model):
    """
    Модель для хранения статей.

    TITLE_LENGTH_RETURN: ограничение символов на вывод текста статьи.


    text: текс статьи.
    pud_date: дата публикации статьи.
    author: автор статьи, установлена связь с таблицей User,
    при удалении из таблицы User автора,
    также будут удалены все связанные статьи.
    group: название сообщества, к которому относится статья,
    установлена связь с моделью Group, чтобы при добавлении
    новой записи можно было сослаться на данную модель.
    """

    TEXT_LENGTH_RETURN: int = 50

    text = models.TextField(verbose_name='Текст поста')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='posts',
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Группа',
        related_name='posts',
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.text[:self.TEXT_LENGTH_RETURN]
