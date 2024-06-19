from django.contrib import admin
from client.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'surname', 'email',)
    list_filter = ('owner',)
    search_fields = ('email',)
