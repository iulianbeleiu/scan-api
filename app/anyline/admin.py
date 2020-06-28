from django.contrib import admin

from .models import Anyline


@admin.register(Anyline)
class AnylineAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name',
                    'active', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_per_page = 10
