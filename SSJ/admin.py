from django.contrib import admin
from .models import Product,Category, Cart, CartItem, Favourite, Order, GoldRate


# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Favourite)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(GoldRate)
