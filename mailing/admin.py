from django.contrib import admin
from mailing.models import Mailing, Logs


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'data_mailing', 'data_mailing_finish', 'periodicity', 'status',)
    list_filter = ('status', 'owner',)
    search_fields = ('name',)


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing', 'datatime', 'status',)
    list_filter = ('mailing', 'status',)
    search_fields = ('mailing',)
