from django.contrib import admin

from .models import Shop, Product, Address


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'quantity',
                    'price', 'barcode', 'image', 'is_active')
    list_editable = ('barcode',)
    search_fields = ('name', 'description', 'quantity',
                     'price', 'barcode', 'image', 'is_active')
    list_per_page = 10


class ShopProductsInline(admin.TabularInline):
    model = Shop.products.through
    extra = 0
    verbose_name = "Product"
    verbose_name_plural = "Products"


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'user', 'address')
    search_fields = ('name', 'is_active', 'user')
    list_per_page = 10
    inlines = [ShopProductsInline]
    exclude = ('products',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'postcode',
                    'region', 'city', 'street', 'number')
    search_fields = ('country', 'postcode',
                     'region', 'city', 'street', 'number')
    list_per_page = 10
