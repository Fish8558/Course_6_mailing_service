from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView, \
    LogListView

app_name = MailingConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('<int:pk>', MailingDetailView.as_view(), name='mailing_detail'),
    path('create/', MailingCreateView.as_view(), name='mailing_create'),
    path('update/<int:pk>', MailingUpdateView.as_view(), name='mailing_update'),
    path('delete/<int:pk>', MailingDeleteView.as_view(), name='mailing_delete'),
    path('<int:mailing_pk>/logs/', LogListView.as_view(), name='log_list'),
]
