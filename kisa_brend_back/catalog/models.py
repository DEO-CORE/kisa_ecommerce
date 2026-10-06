from django.db import models
from django.urls import reverse
from colorfield.fields import ColorField
from core.models import TimeStampedModel, SEOModel


class Drop(TimeStampedModel, SEOModel):
    name = models.CharField('Название дропа', max_length=100)
    slug = models.SlugField('Slug', max_length=120, unique=True)
    is_active = models.BooleanField('Активный', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Изображение дропа', upload_to='drops/', blank=True, null=True)

    class Meta:
        verbose_name = 'Дроп/Коллекция'
        verbose_name_plural = 'Дропы/Коллекции'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:drop_detail', kwargs={'slug': self.slug})


class Color(TimeStampedModel):
    name = models.CharField('Название цвета', max_length=50)
    slug = models.SlugField('Slug', max_length=60, unique=True)
    hex_code = ColorField('HEX код', default='#000000')
    is_active = models.BooleanField('Активный', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Size(TimeStampedModel):
    SIZE_CHOICES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
    ]
    
    name = models.CharField('Размер', max_length=10, choices=SIZE_CHOICES, unique=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активный', default=True)

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'
        ordering = ['order']

    def __str__(self):
        return self.name


class Product(TimeStampedModel, SEOModel):
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('Slug', max_length=220, unique=True)
    drop = models.ForeignKey(
        Drop,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name='Дроп'
    )
    colors = models.ManyToManyField(
        Color,
        through='ProductColor',
        related_name='products',
        verbose_name='Цвета'
    )
    price_rub = models.DecimalField('Цена (₽)', max_digits=10, decimal_places=2, default=0)
    price_kgs = models.DecimalField('Цена (сом)', max_digits=10, decimal_places=2, default=0)
    description = models.TextField('Описание', blank=True)
    composition = models.TextField('Состав и уход', blank=True)
    fit_recommendation = models.TextField('Рекомендации по посадке', blank=True)
    main_image = models.ImageField('Главное фото', upload_to='products/')
    is_active = models.BooleanField('Активный', default=True)
    is_new = models.BooleanField('Новинка', default=False)
    is_bestseller = models.BooleanField('Бестселлер', default=False)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'slug': self.slug})

    def get_available_sizes(self, color=None):
        stocks = self.stocks.filter(quantity__gt=0)
        if color:
            stocks = stocks.filter(color=color)
        return stocks.select_related('size').order_by('size__order')

    def get_total_stock(self):
        return self.stocks.aggregate(total=models.Sum('quantity'))['total'] or 0


class ProductColor(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_colors')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='product_colors')
    images = models.ManyToManyField('ProductImage', blank=True, related_name='product_colors')
    is_main = models.BooleanField('Основной цвет', default=False)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Цвет товара'
        verbose_name_plural = 'Цвета товаров'
        ordering = ['order']
        unique_together = ['product', 'color']

    def __str__(self):
        return f'{self.product.name} — {self.color.name}'


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Изображение', upload_to='products/gallery/')
    alt = models.CharField('Alt текст', max_length=255, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фото товаров'
        ordering = ['order']

    def __str__(self):
        return f'{self.product.name} — фото {self.order}'


class ProductSizeStock(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stocks')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='stocks')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='stocks')
    quantity = models.PositiveIntegerField('Остаток', default=0)
    reserved = models.PositiveIntegerField('Резерв', default=0)

    class Meta:
        verbose_name = 'Остаток по размеру'
        verbose_name_plural = 'Остатки по размерам'
        unique_together = ['product', 'color', 'size']
        ordering = ['size__order']

    def __str__(self):
        return f'{self.product.name} / {self.color.name} / {self.size.name}: {self.quantity} шт.'

    @property
    def available(self):
        return self.quantity - self.reserved

    @property
    def is_low_stock(self):
        return 0 < self.available <= 5

    @property
    def is_out_of_stock(self):
        return self.available <= 0