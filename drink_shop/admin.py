from django.contrib import admin

# Register your models here.

from .models import Category, Product, Order, OrderProduct, ShippingAddress


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'cover', 'featured', 'active')
    readonly_fields = ('slug',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'featured', 'active', 'category')
    readonly_fields = ('slug',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(ShippingAddress)