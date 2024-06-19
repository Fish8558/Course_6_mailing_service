import random
import secrets
import string
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.forms import BooleanField
from blog.models import Article


class StyleFormMixin:
    """Класс миксин стилизации формы"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fields_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = "form-check-input"
            else:
                field.widget.attrs['class'] = "form-control"


def make_random_password():
    character = string.ascii_letters + string.digits
    password = "".join(secrets.choice(character) for i in range(15))
    return password


class AccessCheckMixin:
    """Класс миксин проверки на суперюзера и создателя объекта"""

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and user != self.object.owner:
            raise PermissionDenied
        return self.object


def get_article_list_from_cache():
    if settings.CACHE_ENABLED:
        key = 'article_list'
        article_list = cache.get(key)
        if article_list is None:
            article_list = Article.objects.filter(is_published=True)
            cache.set(key, article_list)
    else:
        article_list = Article.objects.filter(is_published=True)

    return article_list


def get_random_articles(count: int) -> list:
    queryset_count = Article.objects.aggregate(count=Count('id'))['count']

    if queryset_count == 0:
        random_articles = []
    elif count >= queryset_count:
        random_articles = list(Article.objects.all())
    else:
        random_indexes = random.sample(range(queryset_count), count)
        random_articles = [Article.objects.all()[index] for index in random_indexes]
    return random_articles


def get_random_articles_from_cache(count: int) -> list:
    if settings.CACHE_ENABLED:
        key = 'article_random_list'
        article_list = cache.get(key)
        if article_list is None:
            article_list = get_random_articles(count)
            cache.set(key, article_list)
    else:
        article_list = get_random_articles(count)

    return article_list
