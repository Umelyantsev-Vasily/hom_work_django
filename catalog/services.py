# catalog/services.py
from django.core.cache import cache
from django.conf import settings
from .models import Product, Category


class ProductService:

    @staticmethod
    def get_products_by_category(category_name):
        """Получить все продукты в указанной категории по имени"""
        cache_key = f'products_category_{category_name}'
        products = cache.get(cache_key)

        if products is None or not settings.CACHE_ENABLED:
            try:
                category = Category.objects.get(name=category_name)
                products = Product.objects.filter(
                    category=category,
                    publication_status='published'
                )
                if settings.CACHE_ENABLED:
                    cache.set(cache_key, products, 60 * 15)
            except Category.DoesNotExist:
                products = Product.objects.none()

        return products