from ninja import Router, Query
from typing import List
from django.shortcuts import get_object_or_404

from .models import Product, Category, Cart
from .schema import ProductIn, ProductOut, Error, CategoryOut, ProductFilters, CartOut
from applications.order.models import Order
from applications.order.schema import OrderOut

app = Router()


@app.get("/categories", response=List[CategoryOut])
def get_list_categories(request):
    categories = Category.objects.all()
    return categories


@app.get("/products", response=List[ProductOut])
def get_list_products(request, filters: ProductFilters = Query(...)):
    products = Product.objects.all()
    if filters.categories:
        categories = Category.objects.filter(name__in=filters.categories)
        for category in categories:
            subcategories = Category.objects.filter(tree_id=category.tree_id, lft__gte=category.lft,
                                                    rgt__lte=category.rgt)
            products = products.filter(category__in=subcategories.all())
    return products


@app.get("/products/{product_id}", response=ProductOut)
def get_product(request, product_id: int):
    product = get_object_or_404(Product, id=product_id)
    return product


@app.get("/cart", response=List[CartOut])
def get_cart(request):
    cart = Cart.objects.get(user=request.user)
    return cart


@app.post("/products/{product_id}/add_to_cart", response=CartOut)
def add_to_cart(request, product_id: int, quantity: int = 1):
    product = get_object_or_404(Product, id=product_id)
    is_exist = Cart.objects.filter(user=request.user, product=product).exists()
    if is_exist:
        cart = Cart.objects.get(user=request.user, product=product)
        cart.quantity += quantity
        cart.save()
    else:
        cart = Cart.objects.create(user=request.user, product=product, quantity=quantity)
    return cart


@app.patch("/products/{product_id}/update_quantity", response=ProductOut)
def update_quantity(request, product_id: int, quantity: int):
    cart = Cart.objects.get(user=request.user, product=product_id)
    cart.quantity = quantity
    cart.save()
    return cart.product


@app.delete("/products/{product_id}/remove_from_cart", response=ProductOut)
def remove_from_cart(request, product_id: int):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(user=request.user, product=product)
    cart.delete()
    return product


@app.post("/checkout", response=OrderOut)
def checkout(request):
    items = Cart.objects.filter(user=request.user, order=None)
    total_price = sum([item.total_price for item in items])
    order = Order.objects.create(user=request.user, total_price=total_price)
    for item in items:
        item.order = order
        item.save()
    return order
