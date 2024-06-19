from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from mailing.forms import MailingForm, ManagerMailingForm
from mailing.models import Mailing, Logs
from client.models import Client
from message.models import Message


class MailingListView(ListView):
    """Контроллер просмотра списка рассылок"""
    model = Mailing
    extra_context = {'title': 'Рассылки'}

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='moderator').exists():
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MailingDetailView(DetailView):
    """Контроллер просмотра одной рассылки"""
    model = Mailing
    extra_context = {'title': 'Информация о рассылке'}

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='moderator').exists() and user != self.object.owner:
            raise PermissionDenied
        return self.object


class MailingCreateView(CreateView):
    """Контроллер создания рассылки"""
    model = Mailing
    form_class = MailingForm
    extra_context = {'title': 'Создание рассылки'}
    success_url = reverse_lazy('mailings:mailing_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        form.fields['client_mailing'].queryset = Client.objects.filter(owner=user)
        form.fields['message'].queryset = Message.objects.filter(owner=user)
        return form

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    """Контроллер редактирования рассылки"""
    model = Mailing
    form_class = MailingForm
    extra_context = {'title': 'Редактирование рассылки'}

    def get_success_url(self):
        return reverse('mailings:mailing_detail', args=[self.kwargs.get('pk')])

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            form.fields['client_mailing'].queryset = Client.objects.filter(owner=user)
            form.fields['message'].queryset = Message.objects.filter(owner=user)
        return form

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return MailingForm
        elif user.groups.filter(name='moderator').exists():
            return ManagerMailingForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if (not user.is_superuser and user != self.object.owner and
                not user.groups.filter(name='moderator').exists()):
            raise PermissionDenied
        return self.object


class MailingDeleteView(DeleteView):
    """Контроллер удаления рассылки"""
    model = Mailing
    extra_context = {'title': 'Удаление рассылки'}
    success_url = reverse_lazy('mailings:mailing_list')


class LogListView(ListView):
    """Контроллер просмотра логов рассылки"""
    model = Logs
    extra_context = {'title': 'Лог рассылок'}

    def get_queryset(self, *args, **kwargs):
        mailing_pk = self.kwargs.get('mailing_pk')
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(mailing__pk=mailing_pk)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['mailing_pk'] = self.kwargs.get('mailing_pk')
        return context

    def dispatch(self, request, *args, **kwargs):
        mailing_pk = self.kwargs.get('mailing_pk')
        user = self.request.user
        if not user.is_superuser and not Mailing.objects.filter(pk=mailing_pk, owner=user).exists():
            raise PermissionDenied
        return super().dispatch(request, args, **kwargs)
