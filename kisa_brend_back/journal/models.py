from django.db import models
from django.urls import reverse
from core.models import TimeStampedModel, SEOModel
from catalog.models import Product


class PublicationType(models.TextChoices):
    ITEM = 'ITEM', 'ВЕЩЬ'
    PEOPLE = 'PEOPLE', 'ЛЮДИ'
    GUIDE = 'GUIDE', 'ГИД'
    EVENT = 'EVENT', 'СОБЫТИЕ'


class Publication(TimeStampedModel, SEOModel):
    title = models.CharField('Заголовок', max_length=255)
    slug = models.SlugField('Slug', max_length=280, unique=True)
    pub_type = models.CharField('Тип публикации', max_length=10, choices=PublicationType.choices, default=PublicationType.ITEM)
    published_at = models.DateTimeField('Дата публикации')
    preview_image = models.ImageField('Превью (карточка)', upload_to='journal/previews/')
    hero_image = models.ImageField('Главное фото статьи', upload_to='journal/heroes/', blank=True, null=True)
    preview_text = models.TextField('Краткий текст/анонс', blank=True)
    content = models.TextField('Полный текст/контент', blank=True)
    products = models.ManyToManyField(
        Product,
        through='PublicationProduct',
        related_name='publications',
        verbose_name='Связанные товары',
        blank=True
    )
    is_published = models.BooleanField('Опубликовано', default=True)
    is_featured = models.BooleanField('Рекомендуемая', default=False)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации (Журнал)'
        ordering = ['-published_at', 'order']

    def __str__(self):
        return f'[{self.get_pub_type_display()}] {self.title}'

    def get_absolute_url(self):
        return reverse('journal:publication_detail', kwargs={'slug': self.slug})

    def get_type_badge_class(self):
        badges = {
            PublicationType.ITEM: 'badge-item',
            PublicationType.PEOPLE: 'badge-people',
            PublicationType.GUIDE: 'badge-guide',
            PublicationType.EVENT: 'badge-event',
        }
        return badges.get(self.pub_type, '')


class PublicationProduct(TimeStampedModel):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='publication_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='publication_products')
    order = models.PositiveIntegerField('Порядок', default=0)
    note = models.CharField('Примечание', max_length=255, blank=True, help_text='Например: "С этим носят"')

    class Meta:
        verbose_name = 'Товар в публикации'
        verbose_name_plural = 'Товары в публикациях'
        ordering = ['order']
        unique_together = ['publication', 'product']

    def __str__(self):
        return f'{self.publication.title} — {self.product.name}'