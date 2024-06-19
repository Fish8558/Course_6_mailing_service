from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from main.utils import AccessCheckMixin
from message.forms import MessageForm
from message.models import Message


class MessageListView(LoginRequiredMixin, ListView):
    """Контроллер просмотра списка сообщений"""
    model = Message
    extra_context = {'title': 'Сообщения'}

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if not user.is_superuser:
            queryset = queryset.filter(owner=user)
        return queryset


class MessageDetailView(LoginRequiredMixin, AccessCheckMixin, DetailView):
    """Контроллер просмотра одного сообщения"""
    model = Message
    extra_context = {'title': 'Информация о сообщении'}


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания сообщения"""
    model = Message
    form_class = MessageForm
    extra_context = {'title': 'Создание сообщения'}
    success_url = reverse_lazy('messages:message_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, AccessCheckMixin, UpdateView):
    """Контроллер редактирования сообщения"""
    model = Message
    form_class = MessageForm
    extra_context = {'title': 'Редактирование сообщения'}

    def get_success_url(self):
        return reverse('messages:message_detail', args=[self.kwargs.get('pk')])


class MessageDeleteView(LoginRequiredMixin, AccessCheckMixin, DeleteView):
    """Контроллер удаления сообщения"""
    model = Message
    extra_context = {'title': 'Удаление сообщения'}
    success_url = reverse_lazy('messages:message_list')
