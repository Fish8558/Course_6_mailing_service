from django.conf import settings
from django.db import models
from pytils.translit import slugify

NULLABLE = {'blank': True, 'null': True}


class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, verbose_name='slug', **NULLABLE)
    content = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='blog/', default='blog/article_example.jpg', **NULLABLE,
                              verbose_name='Изображение')
    count_views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    is_published = models.BooleanField(default=True, verbose_name='Признак публикации')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              **NULLABLE, verbose_name='Автор')

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(args, kwargs)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
