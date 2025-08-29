# catalog/urls.py
from django.urls import path
from .views import (
    HomeView, ProductListView, ProductDetailView, ContactsView,
    ProductCreateView, ProductUpdateView, ProductDeleteView, unpublish_product
)

app_name = 'catalog'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:pk>/unpublish/', unpublish_product, name='unpublish_product'),  # добавляем новый путь
]