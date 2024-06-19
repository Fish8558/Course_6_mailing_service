from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Message(models.Model):
    """Модель сообщение в рассылке"""
    letter_subject = models.CharField(max_length=150, verbose_name='Тема письма')
    letter_body = models.TextField(verbose_name='Тело письма')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='Создатель')

    def __str__(self):
        return f'{self.letter_subject}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
