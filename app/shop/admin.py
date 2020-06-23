from django.contrib import admin

from .models import Shop, Product, Address


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'quantity',
                    'price', 'barcode', 'image', 'is_active')
    search_fields = ('name', 'description', 'quantity',
                     'price', 'barcode', 'image', 'is_active')
    list_per_page = 10


class ShopProductsInline(admin.TabularInline):
    model = Shop.products.through
    extra = 0
    verbose_name = "Product"
    verbose_name_plural = "Products"


class ShopAddressInline(admin.TabularInline):
    model = Shop.address.through
    extra = 0
    max_num = 1
    min_num = 1
    verbose_name = "Address"
    verbose_name_plural = "Address"


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'user')
    search_fields = ('name', 'is_active', 'user')
    list_per_page = 10
    inlines = [ShopProductsInline, ShopAddressInline]
    exclude = ('products', 'address')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'postcode',
                    'region', 'city', 'street', 'number')
    search_fields = ('country', 'postcode',
                     'region', 'city', 'street', 'number')
    list_per_page = 10
