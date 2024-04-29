from ninja import Query
from ninja_extra import (
    api_controller, route, NinjaExtraAPI
)
from typing import List
from django.shortcuts import get_object_or_404

from .models import Product, Category, Cart
from .schema import ProductIn, ProductOut, Error, CategoryOut, ProductFilters, CartOut
from applications.order.models import Order
from applications.order.schema import OrderOut


@api_controller('/products', tags=['Products'])
class ProductController:
    @route.get("", response=List[ProductOut])
    def get_list_products(self, filters: ProductFilters = Query(...)):
        products = Product.objects.all()
        if filters.categories:
            categories = Category.objects.filter(name__in=filters.categories)
            for category in categories:
                subcategories = Category.objects.filter(tree_id=category.tree_id, lft__gte=category.lft,
                                                        rgt__lte=category.rgt)
                products = products.filter(category__in=subcategories.all())
        return products

    @route.get("/{product_id}", response=ProductOut)
    def get_product(self, product_id: int):
        product = get_object_or_404(Product, id=product_id)
        return product

    @route.post("/{product_id}/add_to_cart", response=CartOut)
    def add_to_cart(self, product_id: int, quantity: int = 1):
        product = get_object_or_404(Product, id=product_id)
        is_exist = Cart.objects.filter(user=self.request.user, product=product).exists()
        if is_exist:
            cart = Cart.objects.get(user=self.request.user, product=product)
            cart.quantity += quantity
            cart.save()
        else:
            cart = Cart.objects.create(user=self.request.user, product=product, quantity=quantity)
        return cart

    @route.patch("/{product_id}/update_quantity", response=ProductOut)
    def update_quantity(self, product_id: int, quantity: int):
        cart = Cart.objects.get(user=self.request.user, product=product_id)
        cart.quantity = quantity
        cart.save()
        return cart.product

    @route.delete("/{product_id}/remove_from_cart", response=ProductOut)
    def remove_from_cart(request, product_id: int):
        product = get_object_or_404(Product, id=product_id)
        cart = Cart.objects.get(user=request.user, product=product)
        cart.delete()
        return product


# @app.get("/categories", response=List[CategoryOut])
# def get_list_categories(request):
#    categories = Category.objects.all()
#    return categories


# @app.get("/cart", response=List[CartOut])
# def get_cart(request):
#     cart = Cart.objects.get(user=request.user)
#     return cart


# @app.post("/checkout", response=OrderOut)
# def checkout(request):
#     items = Cart.objects.filter(user=request.user, order=None)
#     total_price = sum([item.total_price for item in items])
#     order = Order.objects.create(user=request.user, total_price=total_price)
#     for item in items:
#         item.order = order
#         item.save()
#     return order



