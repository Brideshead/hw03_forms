from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """
    Создание объекта, который передается в качестве
    переменной form в контекст шаблона templates/create_post.html
    """
    class Meta:
        model = Post
        fields = ('text', 'group')
