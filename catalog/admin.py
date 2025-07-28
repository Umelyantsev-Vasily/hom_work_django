from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Отображаемые поля в списке
    list_display_links = ('id', 'name')  # Поля-ссылки для редактирования


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')  # Отображаемые поля
    list_filter = ('category',)  # Фильтрация по категории
    search_fields = ('name', 'description')  # Поля для поиска
    list_editable = ('price',)  # Разрешить редактирование цени прямо в списке