from django.db import models
from solo.models import SingletonModel


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        abstract = True
        ordering = ['-created_at']


class SingletonBase(SingletonModel, TimeStampedModel):
    class Meta:
        abstract = True


class SEOModel(models.Model):
    meta_title = models.CharField('Meta Title', max_length=255, blank=True)
    meta_description = models.TextField('Meta Description', blank=True)
    meta_keywords = models.CharField('Meta Keywords', max_length=255, blank=True)

    class Meta:
        abstract = True

class Subscriber(TimeStampedModel):
    email = models.EmailField('Email', unique=True)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

    def __str__(self):
        return self.email


class SeedRun(models.Model):
    key = models.CharField(max_length=100, unique=True)
    completed_at = models.DateTimeField(auto_now_add=True)
