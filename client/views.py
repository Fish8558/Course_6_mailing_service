from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from client.forms import ClientForm
from client.models import Client
from main.utils import AccessCheckMixin


class ClientListView(LoginRequiredMixin, ListView):
    """Контроллер просмотра списка клиентов"""
    model = Client
    extra_context = {'title': 'Клиенты сервиса'}

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if not user.is_superuser:
            queryset = queryset.filter(owner=user)
        return queryset


class ClientDetailView(LoginRequiredMixin, AccessCheckMixin,  DetailView):
    """Контроллер просмотра одного клиента"""
    model = Client
    extra_context = {'title': 'Информация о клиенте'}


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания клиента"""
    model = Client
    form_class = ClientForm
    extra_context = {'title': 'Добавление клиента'}
    success_url = reverse_lazy('clients:client_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        data = super().get_form_kwargs()
        data['owner'] = self.request.user
        return data


class ClientUpdateView(LoginRequiredMixin, AccessCheckMixin, UpdateView):
    """Контроллер редактирования клиента"""
    model = Client
    form_class = ClientForm
    extra_context = {'title': 'Редактирование клиента'}

    def get_success_url(self):
        return reverse('clients:client_detail', args=[self.kwargs.get('pk')])

    def get_form_kwargs(self):
        data = super().get_form_kwargs()
        data['owner'] = self.request.user
        data['pk'] = self.kwargs.get('pk')
        return data


class ClientDeleteView(LoginRequiredMixin, AccessCheckMixin, DeleteView):
    """Контроллер удаления клиента"""
    model = Client
    extra_context = {'title': 'Удаление клиента'}
    success_url = reverse_lazy('clients:client_list')
