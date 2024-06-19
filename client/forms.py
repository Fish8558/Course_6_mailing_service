from django import forms
from django.core.exceptions import ValidationError
from client.models import Client
from main.utils import StyleFormMixin


class ClientForm(StyleFormMixin, forms.ModelForm):
    """Форма создания и редактирования клиента"""

    class Meta:
        model = Client
        exclude = ('owner',)

    def __init__(self, *args, owner, pk=None, **kwargs):
        self.owner = owner
        self.pk = pk
        super().__init__(*args, **kwargs)

    def clean_email(self):
        """Clean метод проверяющий уникальность email клиента
        среди клиентов пользователя"""
        email = self.cleaned_data.get('email')
        if self.pk and Client.objects.filter(email=email, owner=self.owner, pk=self.pk).exists():
            return email
        if Client.objects.filter(email=email, owner=self.owner).exists():
            raise ValidationError('Повторяющийся email!')
        return email
