from django.contrib import admin
from . import models

admin.site.register(models.Collection)
admin.site.register(models.Address)
admin.site.register(models.Cart)
admin.site.register(models.CartItem)
admin.site.register(models.Customer)
admin.site.register(models.OrderItem)
admin.site.register(models.Product)
admin.site.register(models.Promotion)
