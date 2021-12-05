from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from store.models import Product
from .models import User
from store.admin import ProductAdmin
from tags.models import TageedItem
admin.site.register(User)


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TageedItem
    extra = 0
    min_num = 1
    max_num = 5


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
