from django import forms
from mailing.models import Mailing
from main.utils import StyleFormMixin


class MailingForm(StyleFormMixin, forms.ModelForm):
    """Форма создания и редактирования рассылки"""
    class Meta:
        model = Mailing
        exclude = ('data_mailing', 'owner',)


class ManagerMailingForm(StyleFormMixin, forms.ModelForm):
    """Форма редактирования рассылки для менеджера"""
    class Meta:
        model = Mailing
        fields = ('status',)
