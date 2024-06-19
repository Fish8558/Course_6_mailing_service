from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.forms import ArticleForm
from blog.models import Article


class ArticleListView(ListView):
    model = Article
    queryset = Article.objects.all()
    extra_context = {"title": "Cтатьи"}


class ArticleDetailView(DetailView):
    model = Article
    extra_context = {"title": "Статья"}

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_views += 1
        self.object.save()
        return self.object


class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'blog.add_article'
    model = Article
    form_class = ArticleForm
    extra_context = {"title": "Добавление статьи"}

    def get_success_url(self):
        return reverse('blog:article_view', args=[self.object.slug])

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'blog.change_article'
    model = Article
    form_class = ArticleForm
    extra_context = {
        "title": "Редактирование статьи"
    }

    def get_success_url(self):
        return reverse('blog:article_view', args=[self.object.slug])


class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'blog.delete_article'
    model = Article
    extra_context = {
        "title": "Удаление статьи"
    }
    success_url = reverse_lazy('blog:article_list')
