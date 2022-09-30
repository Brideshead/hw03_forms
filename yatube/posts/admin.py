from django.contrib import admin
from .models import Post, Group


class PostAdmin(admin.ModelAdmin):
    """
    Настройки отображения модели в интерфейсе админки.

    list_display: перечисляем поля, которые должны отображаться.
    list_editable: опция для измнения поля group в любом посте.
    search_fields: интерфейс для поиска по тексту постов.
    list_filter: фильтрация по дате.
    empty_value_display: вывод в поле текста '-пусто',
    если информация отсутствует.
    """

    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)
admin.site.register(Group)
