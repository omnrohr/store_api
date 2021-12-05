from django.db.models.aggregates import Count
from django.contrib import admin
from django.db.models.query import QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'low')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection']

    def collection_title(self, product: models.Product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product: models.Product):
        if product.inventory < 10:
            return 'low'
        return 'ok'


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'payment_status']
    list_per_page = 10
    list_select_related = ['customer']
    search_fields = ['payment_status',
                     'customer__first_name__istartswith', 'customer__last_name__istartswith']

    # def customer_name(self, order: models.Order):
    #     return order.customer.first_name + " " + order.customer.last_name


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'customer_orders']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='customer_orders')
    def customer_orders(self, customer: models.Customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer__id': customer.id
            })
        )
        return format_html('<a href="{}">{} Orders</a>', url, customer.customer_orders)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            customer_orders=Count('orders')
        )


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection: models.Collection):
        # admin:app_model_page
        url = (
            reverse('admin:store_product_changelist')
            + '?' + urlencode({
                'collection__id': str(collection.id)
            }))
        return format_html('<a href="{}">{} Products</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )


# admin.site.register(models.Collection)
admin.site.register(models.Address)
admin.site.register(models.Cart)
admin.site.register(models.CartItem)
# admin.site.register(models.Customer)
admin.site.register(models.OrderItem)
# I register the modle in the @admin
# admin.site.register(models.Product)
admin.site.register(models.Promotion)
