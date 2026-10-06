from django.db import models
from django.utils.html import format_html
from solo.models import SingletonModel
from core.models import TimeStampedModel, SingletonBase


class MainPageSettings(SingletonBase):
    slogan = models.CharField('Главный слоган', max_length=255, default='ОДЕЖДА КАК ЛИЧНОЕ ПРОСТРАНСТВО')
    manifesto = models.TextField('Текст манифеста', blank=True, help_text='Текст "KISA создаёт вещи для повседневной жизни..."')
    team_photo = models.ImageField('Фото команды/студии', upload_to='about/', blank=True, null=True)
    hero_video = models.FileField('Видео на главной (опционально)', upload_to='about/video/', blank=True, null=True)

    class Meta:
        verbose_name = 'Настройки главной страницы'
        verbose_name_plural = 'Настройки главной страницы'

    def __str__(self):
        return 'Настройки главной страницы'


class BrandPrinciple(TimeStampedModel):
    number = models.PositiveIntegerField('Порядковый номер', unique=True)
    title = models.CharField('Заголовок', max_length=100)
    description = models.TextField('Описание')
    icon = models.ImageField('Иконка/Изображение', upload_to='about/principles/', blank=True, null=True)
    is_active = models.BooleanField('Активный', default=True)

    class Meta:
        verbose_name = 'Принцип бренда'
        verbose_name_plural = 'Принципы бренда'
        ordering = ['number']

    def __str__(self):
        return f'{self.number:02d} — {self.title}'


class BrandHistory(TimeStampedModel):
    year = models.PositiveIntegerField('Год', unique=True)
    title = models.CharField('Заголовок этапа', max_length=200)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='about/history/', blank=True, null=True)
    is_active = models.BooleanField('Показывать на сайте', default=True)

    class Meta:
        verbose_name = 'История бренда (год)'
        verbose_name_plural = 'История бренда'
        ordering = ['-year']

    def __str__(self):
        return f'{self.year} — {self.title}'


class TeamBlock(SingletonBase):
    text = models.TextField('Текст блока "Команда"', blank=True, help_text='"KISA — маленькая команда с полным вниманием к каждой вещи..."')
    photo = models.ImageField('Фото команды', upload_to='about/team/', blank=True, null=True)

    class Meta:
        verbose_name = 'Блок "Команда"'
        verbose_name_plural = 'Блок "Команда"'

    def __str__(self):
        return 'Блок "Команда"'