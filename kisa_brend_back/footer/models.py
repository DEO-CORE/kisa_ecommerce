from django.db import models
from solo.models import SingletonModel
from core.models import SingletonBase, TimeStampedModel
from colorfield.fields import ColorField


class SiteSettings(SingletonBase):
    primary_color = ColorField('Основной цвет сайта', default='#000000', help_text='Цвет для текста, кнопок, ссылок и акцентов')
    secondary_color = ColorField('Вторичный цвет', default='#ffffff', help_text='Фон, второстепенные элементы')
    accent_color = ColorField('Акцентный цвет', default='#000000', help_text='Ховеры, активные состояния')

    class Meta:
        verbose_name = 'Настройки цветов сайта'
        verbose_name_plural = 'Настройки цветов сайта'

    def __str__(self):
        return 'Настройки цветов сайта'


class Contacts(SingletonBase):
    seller_name = models.CharField('Наименование продавца / ФИО ИП', max_length=255, blank=True)
    country = models.CharField('Страна регистрации', max_length=100, blank=True)
    registration_number = models.CharField('Регистрационный номер', max_length=100, blank=True)
    tax_id = models.CharField('ИНН / налоговый номер', max_length=100, blank=True)
    legal_address = models.TextField('Юридический адрес', blank=True)
    email = models.EmailField('Email для обращений и персональных данных', blank=True)
    telegram_url = models.URLField('Telegram (ссылка/юзернейм)', max_length=255, blank=True, help_text='Например: https://t.me/kisa_shop или @kisa_shop')
    phone = models.CharField('Телефон', max_length=50, blank=True)
    address = models.TextField('Адрес', blank=True)
    work_hours = models.CharField('Режим работы', max_length=100, blank=True)

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return 'Контакты'


class Partnership(SingletonBase):
    email = models.EmailField('Email для сотрудничества', default='work@kisa')
    description = models.TextField('Описание', blank=True, help_text='Текст для страницы/блока сотрудничества')

    class Meta:
        verbose_name = 'Сотрудничество'
        verbose_name_plural = 'Сотрудничество'

    def __str__(self):
        return 'Сотрудничество'


class Support(SingletonBase):
    telegram_url = models.URLField('Telegram поддержки', max_length=255, blank=True, help_text='Например: https://t.me/kisa_support или @kisa_support')
    email = models.EmailField('Email поддержки', default='support@kisa')
    description = models.TextField('Описание', blank=True, help_text='Текст для страницы/блока поддержки')

    class Meta:
        verbose_name = 'Поддержка'
        verbose_name_plural = 'Поддержка'

    def __str__(self):
        return 'Поддержка'


class InfoPage(TimeStampedModel):
    PAGE_TYPES = [
        ('cookies', 'Политика cookie'),
        ('delivery', 'Доставка'),
        ('payment', 'Оплата'),
        ('returns', 'Возврат и обмен'),
        ('contacts', 'Контакты и реквизиты'),
        ('payment_return', 'Оплата и возврат'),
        ('documents', 'Документы'),
        ('privacy', 'Политика конфиденциальности'),
        ('terms', 'Условия покупки и использования'),
    ]
    
    page_type = models.CharField('Тип страницы', max_length=20, choices=PAGE_TYPES, unique=True)
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Контент', blank=True, help_text='Обычный текст; заголовки разделов начинайте с ##. HTML не исполняется.')
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        verbose_name = 'Информационная страница'
        verbose_name_plural = 'Информационные страницы'

    def __str__(self):
        return self.get_page_type_display()
