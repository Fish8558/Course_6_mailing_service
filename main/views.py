from django.views.generic import TemplateView


class IndexView(TemplateView):
    extra_context = {'title': 'Главная'}
    template_name = 'main/index.html'
