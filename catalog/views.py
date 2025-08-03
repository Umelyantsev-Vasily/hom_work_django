# catalog/views.py
from django.shortcuts import render, get_object_or_404
from .models import Product

def home(request):
    products = Product.objects.all()[:12]  # Берем первые 12 товаров
    return render(request, 'catalog/home.html', {'products': products})

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f"Новое сообщение от {name} ({email}): {message}")
    return render(request, 'catalog/contacts.html')

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})