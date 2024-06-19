from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """Модель клиент сервиса, получает рассылки"""
    firstname = models.CharField(max_length=50, verbose_name='Имя')
    lastname = models.CharField(max_length=50, verbose_name='Фамилия')
    surname = models.CharField(max_length=50, verbose_name='Отчество')
    email = models.EmailField(max_length=256, verbose_name='Почта')
    comment = models.TextField(max_length=450, **NULLABLE, verbose_name='Комментарий')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='Создатель')

    def __str__(self):
        return f'{self.firstname} {self.lastname} {self.surname}'.title()

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        unique_together = ['email', 'owner']
