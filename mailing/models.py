from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from client.models import Client
from message.models import Message

NULLABLE = {'blank': True, 'null': True}


class Mailing(models.Model):
    """Модель рассылки"""

    class PeriodicityOfMailing(models.TextChoices):
        ONCE_TIME = "Один раз", _("Один раз")
        ONCE_DAY = "Ежедневно", _("Ежедневно")
        ONCE_WEEK = "Еженедельно", _("Еженедельно")
        ONCE_MONTH = "Ежемесячно", _("Ежемесячно")

    class StatusOfMailing(models.TextChoices):
        CREATED = "Создана", _("Создана")
        LAUNCHED = "Запущена", _("Запущена")
        FINISHED = "Завершена", _("Завершена")

    name = models.CharField(max_length=50, verbose_name='Название')
    data_mailing = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    sent_time = models.DateTimeField(default=timezone.now, verbose_name='Дата отправки')
    data_mailing_finish = models.DateTimeField(default=timezone.now() + timedelta(days=180),
                                               verbose_name='Дата завершения')
    periodicity = models.CharField(default=PeriodicityOfMailing.ONCE_TIME, choices=PeriodicityOfMailing,
                                   verbose_name='Периодичность')
    client_mailing = models.ManyToManyField(Client, verbose_name='Получатели')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='Создатель')
    status = models.CharField(default=StatusOfMailing.CREATED, choices=StatusOfMailing, verbose_name='Статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        permissions = [
            ('set_deactivate', 'Can deactivate mailing'),
            ('view_all_mailing', 'Can view all mailing'),
        ]


class Logs(models.Model):
    """Модель логов рассылки"""

    class StatusOfLogs(models.TextChoices):
        SUCCESS = "Успешно", _("Успешно")
        FAILED = "Безуспешно", _("Безуспешно")

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')
    datatime = models.DateTimeField(verbose_name='Дата и время попытки')
    status = models.CharField(choices=StatusOfLogs, verbose_name='Статус')
    answer_server = models.TextField(verbose_name='Ответ почтового сервера')

    def __str__(self):
        return f"{self.datatime} | {self.mailing} | {self.status} | {self.answer_server}"

    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'
