from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CreationForm(UserCreationForm):
    """
    Класс для формы регистрации.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        help_texts = {
            'first_name': 'имя пользователя',
            'last_name' : 'фамилия пользователя',
            'username': 'имя пользователя',
            'email': 'почта пользователя',
        } 
