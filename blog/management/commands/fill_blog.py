from django.core.management.base import BaseCommand
from blog.models import BlogPost
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Fill blog with test data'

    def handle(self, *args, **options):
        titles = [
            "Как я научился программировать за 30 дней",
            "10 лучших фреймворков 2025 года",
            "Django vs Flask: подробное сравнение",
            "История успеха Python",
            "Секреты оптимизации SQL-запросов"
        ]

        for i, title in enumerate(titles):
            BlogPost.objects.create(
                title=title,
                content=f"Это тестовое содержимое статьи {i+1}. " * 50,
                is_published=random.choice([True, False]),
                views_count=random.randint(0, 1000)
            )
        self.stdout.write(self.style.SUCCESS('Successfully filled blog with test data'))