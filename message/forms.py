from django import forms
from main.utils import StyleFormMixin
from message.models import Message


class MessageForm(StyleFormMixin, forms.ModelForm):
    """Форма создания и редактирования сообщения"""
    class Meta:
        model = Message
        exclude = ('owner',)
