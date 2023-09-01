from django.contrib import admin
from .models import Category, Product, Cart, ProductCart, Order, ProductOrder, CustomUser


class ProductCartInline(admin.TabularInline):
    model = ProductCart
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class ProductAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class CartAdmin(admin.ModelAdmin):
    inlines = [ProductCartInline]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(ProductCart)
admin.site.register(Order)
admin.site.register(ProductOrder)
admin.site.register(CustomUser)
