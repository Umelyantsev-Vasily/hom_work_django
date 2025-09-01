# catalog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from .models import Product, Category
from .forms import ProductForm
from .services import ProductService
from django.core.cache import cache
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


# Главная страница - доступна всем
class HomeView(TemplateView):
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.filter(
            publication_status='published'
        )[:3]
        return context


# Список товаров - доступен всем (только опубликованные)
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        cache_key = 'all_published_products'
        products = cache.get(cache_key)

        if products is None or not settings.CACHE_ENABLED:
            products = Product.objects.filter(publication_status='published')
            if settings.CACHE_ENABLED:
                cache.set(cache_key, products, 60 * 15)  # 15 минут

        return products


# Детали товара - доступны всем (только опубликованные)
@method_decorator(cache_page(60 * 15), name='dispatch')  # Кеширование на 15 минут
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'

    def get_queryset(self):
        return Product.objects.filter(publication_status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


# Контакты - доступны всем
class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"Новое сообщение от {name} ({phone}): {message}")
        return self.get(request, *args, **kwargs)


# Создание товара - только для авторизованных
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')
    login_url = 'users:login'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


# Редактирование товара - только для владельца
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')
    login_url = 'users:login'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        product = self.get_object()
        return product.owner == self.request.user

    def handle_no_permission(self):
        return HttpResponseForbidden("У вас нет прав для редактирования этого товара")


# Удаление товара - только для владельца или модератора
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
    login_url = 'users:login'

    def test_func(self):
        product = self.get_object()
        return (product.owner == self.request.user or
                self.request.user.has_perm('catalog.can_delete_any_product'))

    def handle_no_permission(self):
        return HttpResponseForbidden("У вас нет прав для удаления этого товара")


# Функция для отмены публикации
def unpublish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Проверка прав: модератор или владелец
    if not (request.user.has_perm('catalog.can_unpublish_product') or
            product.owner == request.user):
        return HttpResponseForbidden("У вас нет прав для отмены публикации")

    product.publication_status = 'draft'
    product.save()

    return redirect('catalog:product_detail', pk=product.pk)


def category_products_view(request, category_name):
    """Представление для отображения продуктов по категории"""
    products = ProductService.get_products_by_category(category_name)

    context = {
        'products': products,
        'category_name': category_name,
    }

    return render(request, 'catalog/category_products.html', context)