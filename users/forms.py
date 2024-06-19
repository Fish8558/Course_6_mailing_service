from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordResetForm
from main.utils import StyleFormMixin
from users.models import User


class LoginForm(StyleFormMixin, AuthenticationForm):
    """Форма входа пользователя"""
    pass


class RegisterForm(StyleFormMixin, UserCreationForm):
    """Форма регистрации пользователя"""
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class UserForm(StyleFormMixin, UserChangeForm):
    """Форма редактирования пользователя"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'country', 'avatar',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class RecoveryForm(StyleFormMixin, PasswordResetForm):
    """Форма восстановления пользователя"""
    pass
