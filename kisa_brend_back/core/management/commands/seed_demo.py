"""Install demo catalogue once without rewriting merchant data."""
from pathlib import Path

from django.core.files import File
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from catalog.models import Color, Drop, Product, ProductColor, ProductImage, ProductSizeStock, Size
from core.models import SeedRun
from journal.models import Publication, PublicationProduct

ASSETS = Path(__file__).resolve().parents[2] / 'seed_assets'
SEED_KEY = 'kisa-demo-catalog-v1'
COLORS = [
    ('grey', 'Серый меланж', '#c9c9c5'), ('black', 'Чёрный', '#0c0c0c'),
    ('red', 'Красный', '#ad1936'), ('cream', 'Кремовый', '#f1eee5'),
    ('pink', 'Розовый', '#e9bacb'), ('burgundy', 'Бордовый', '#61202e'),
]
PRODUCTS = [
    ('demo-zip-hoodie', 'Зип-худи From Abusers', 'hoodie', ['grey', 'red', 'black'], '11990', '12990', 'demo-essential', 'Свободный силуэт, капюшон и застёжка на молнию.'),
    ('demo-pants-smile', 'Брюки Smile', 'pants', ['grey', 'black'], '8990', '9990', 'demo-essential', 'Брюки свободного кроя для повседневных сочетаний.'),
    ('demo-tee-from-abusers', 'Тру-фит футболка From Abusers', 'tee', ['cream', 'pink', 'burgundy', 'red'], '3990', '4490', 'demo-color', 'Базовая футболка с принтом в четырёх цветах.'),
]
ARTICLES = [
    ('demo-layering', 'Как собрать образ слоями', 'ITEM', 'hoodie', 'Сочетайте футболку, свободное худи и брюки. Меняйте верхний слой в зависимости от погоды и выбирайте комфортный для себя объём.'),
    ('demo-care', 'Уход начинается с этикетки', 'GUIDE', 'care', 'Перед стиркой проверьте рекомендации на этикетке конкретной вещи. Разделяйте одежду по цвету, учитывайте состав ткани и не превышайте указанную температуру.'),
    ('demo-capsule', 'Один гардероб — разные сочетания', 'GUIDE', 'collection', 'Начните с нейтральных оттенков и добавьте один цветовой акцент. Футболка, худи и брюки из демонстрационного каталога помогают посмотреть, как работает подборка товаров.'),
]


class Command(BaseCommand):
    help = 'Create the demo catalogue and editorial examples once; preserve all existing records.'

    def handle(self, *args, **options):
        uploaded = []
        cached = {}

        def asset(path):
            if path not in cached:
                with (ASSETS / path).open('rb') as source:
                    name = default_storage.save(f'seed/{path}', File(source))
                uploaded.append(name)
                cached[path] = name
            return cached[path]

        try:
            with transaction.atomic():
                # Unique insert also serializes concurrent command invocations.
                _, first_run = SeedRun.objects.get_or_create(key=SEED_KEY)
                if not first_run:
                    self.stdout.write('Demo catalogue already installed; skipped.')
                    return
                sizes = [Size.objects.get_or_create(name=name, defaults={'order': i})[0] for i, name in enumerate(['XS', 'S', 'M', 'L', 'XL'])]
                colors = {slug: Color.objects.get_or_create(slug=slug, defaults={'name': name, 'hex_code': code, 'order': i})[0] for i, (slug, name, code) in enumerate(COLORS)}
                drops = {}
                for i, (slug, name) in enumerate([('demo-essential', 'Essential / Demo'), ('demo-color', 'Color / Demo')]):
                    drop, created = Drop.objects.get_or_create(slug=slug, defaults={'name': name, 'order': i, 'description': 'Демонстрационная подборка KISA. Цены и наличие — пример наполнения каталога.'})
                    if created:
                        drop.image = asset('editorial/collection.png')
                        drop.save(update_fields=['image'])
                    drops[slug] = drop
                products = []
                created_products = 0
                for index, (slug, name, category, variants, rub, kgs, drop_slug, description) in enumerate(PRODUCTS):
                    product, created = Product.objects.get_or_create(slug=slug, defaults={
                        'name': name, 'drop': drops[drop_slug], 'price_rub': rub, 'price_kgs': kgs,
                        'description': description + '\n\nДемонстрационный товар: цена, состав и остатки требуют подтверждения магазином перед продажей.',
                        'composition': 'Уточните состав и рекомендации на этикетке товара. Данные для демонстрации каталога.',
                        'fit_recommendation': 'Выберите размер по таблице замеров. Перед покупкой уточните актуальные параметры вещи.',
                        'is_new': index < 2, 'is_bestseller': False, 'order': index,
                    })
                    products.append(product)
                    if not created:
                        continue
                    created_products += 1
                    for color_index, color_slug in enumerate(variants):
                        image_name = asset(f'products/{category}-{color_slug}.png')
                        image = ProductImage.objects.create(product=product, image=image_name, alt=f'{name} — {colors[color_slug].name}', order=color_index)
                        variant = ProductColor.objects.create(product=product, color=colors[color_slug], is_main=color_index == 0, order=color_index)
                        variant.images.add(image)
                        if color_index == 0:
                            product.main_image = image_name
                            product.save(update_fields=['main_image'])
                        for size_index, size in enumerate(sizes):
                            ProductSizeStock.objects.create(product=product, color=colors[color_slug], size=size, quantity=[0 if category == 'hoodie' else 2, 5, 8, 5, 2][size_index])
                for index, (slug, title, kind, photo, content) in enumerate(ARTICLES):
                    article, created = Publication.objects.get_or_create(slug=slug, defaults={
                        'title': title, 'pub_type': kind, 'published_at': timezone.now(),
                        'preview_text': content, 'content': content + '\n\nМатериал для демонстрации журнала KISA.',
                        'order': index, 'is_featured': index == 0,
                    })
                    if created:
                        article.preview_image = asset(f'editorial/{photo}.png')
                        article.hero_image = article.preview_image.name
                        article.save(update_fields=['preview_image', 'hero_image'])
                        for order, product in enumerate(products):
                            PublicationProduct.objects.create(publication=article, product=product, order=order)
        except Exception:
            for name in uploaded:
                try:
                    default_storage.delete(name)
                except Exception:
                    self.stderr.write('Could not clean up a seed upload after failure.')
            raise
        self.stdout.write(self.style.SUCCESS(f'Demo catalogue installed: {created_products} new products, 9 planned colour variants, 3 editorial examples.'))
