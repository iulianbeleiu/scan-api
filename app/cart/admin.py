from django.contrib import admin

from .models import CartItem, Cart


class CartItemsInline(admin.TabularInline):
    model = Cart.items.through
    extra = 0
    verbose_name = "Cart Item"
    verbose_name_plural = "Cart Items"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price',
                    'quantity', 'created_at', 'created_at')
    search_fields = ('name', 'price', 'quantity',
                     'created_at', 'created_at')
    list_per_page = 10


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'total', 'completed', 'created_at', 'created_at')
    search_fields = ('total', 'completed', 'created_at', 'created_at')
    list_per_page = 10
    inlines = [CartItemsInline]
    exclude = ('items',)
