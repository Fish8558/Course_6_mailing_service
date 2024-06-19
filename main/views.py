from django.views.generic import TemplateView
from blog.models import Article
from client.models import Client
from mailing.models import Mailing
from main.utils import get_random_articles_from_cache


class IndexView(TemplateView):
    extra_context = {'title': 'Главная'}
    template_name = 'main/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        mailing = Mailing.objects.all()
        clients = Client.objects.all()
        context['count_mailing'] = mailing.count()
        context['count_mailing_active'] = mailing.filter(status=Mailing.StatusOfMailing.LAUNCHED).count()
        context['articles_random'] = Article.objects.all()
        context['count_client'] = clients.count()
        context['count_client_unique'] = clients.values('email').distinct().count()
        context['object_list'] = get_random_articles_from_cache(3)
        return context
