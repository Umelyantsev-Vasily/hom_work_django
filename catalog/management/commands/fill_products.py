from django.core.management.base import BaseCommand
from catalog.models import Category, Product
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Очищает базу и добавляет тестовые продукты и категории'

    def handle(self, *args, **options):
        self.stdout.write("Удаление старых данных...")

        # Удаляем все существующие данные
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write("Создание тестовых категорий...")

        # Создаем категории
        categories = [
            {'name': 'Электроника', 'description': 'Гаджеты и устройства'},
            {'name': 'Книги', 'description': 'Художественная литература'},
            {'name': 'Одежда', 'description': 'Мужская и женская одежда'},
        ]

        created_categories = []
        for cat_data in categories:
            category = Category.objects.create(**cat_data)
            created_categories.append(category)
            self.stdout.write(f"Создана категория: {category.name}")

        self.stdout.write("Создание тестовых продуктов...")

        # Создаем продукты
        products = [
            {'name': 'Смартфон', 'price': 999.99, 'category': 'Электроника'},
            {'name': 'Ноутбук', 'price': 1499.99, 'category': 'Электроника'},
            {'name': 'Наушники', 'price': 199.99, 'category': 'Электроника'},
            {'name': 'Роман', 'price': 19.99, 'category': 'Книги'},
            {'name': 'Детектив', 'price': 14.99, 'category': 'Книги'},
            {'name': 'Футболка', 'price': 29.99, 'category': 'Одежда'},
            {'name': 'Джинсы', 'price': 59.99, 'category': 'Одежда'},
        ]

        for prod_data in products:
            category = next(c for c in created_categories if c.name == prod_data['category'])
            Product.objects.create(
                name=prod_data['name'],
                price=prod_data['price'],
                category=category,
                description=f"Описание для {prod_data['name']}",
                created_at=datetime.now() - timedelta(days=random.randint(1, 30))
            )

        self.stdout.write(
            self.style.SUCCESS(f"Успешно создано {len(created_categories)} категорий и {len(products)} продуктов"))