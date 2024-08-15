from django.contrib import admin
from .models import Client, Order


admin.site.register(Client)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ['client', 'order_date', 'amount']
    list_display = ['id', 'client', 'order_date', 'amount']
    