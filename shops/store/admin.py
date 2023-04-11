from django.contrib import admin

from store.models import Order, Transaction, CartItem, Cart, Product, Category

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Transaction)
admin.site.register(Order)
