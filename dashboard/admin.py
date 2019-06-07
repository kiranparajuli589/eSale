from django.contrib import admin

from dashboard.models import (Item, Vendor, Customer, Cart, Order, Transaction, CartItem,
                              Inventory, TransactionStat, TransactionStatMonth, TransactionStatYear)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_code', 'item_name', 'quantity', 'buying_rate', 'selling_rate')
    list_filter = ('location_in_store',)
    search_fields = ('item_code', 'item_name', 'description')
    ordering = ('item_code', 'item_name', 'buying_rate', 'selling_rate')

class VendorAdmin(admin.ModelAdmin):
    list_display = ('get_vendor_name', 'email', 'phone', 'address', 'tot_recved', 'tot_due')
    list_filter = ('f_name', 'address', 'date_created')
    date_hierarchy = 'date_created'
    search_fields = ('email', 'f_name', 'l_name', 'address')
    ordering = ('-date_created', 'email', 'tot_recved', 'tot_due')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('get_customer_name', 'email', 'phone', 'address', 'tot_recved', 'tot_due')
    list_filter = ('f_name', 'address', 'date_created')
    date_hierarchy = 'date_created'
    search_fields = ('email', 'f_name', 'l_name', 'address')
    ordering = ('-date_created', 'email', 'tot_recved', 'tot_due')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'customer', 'vendor', 'type', 'payment_type', 'received', 'due_amount')
    list_filter = ('customer', 'vendor', 'type', 'timestamp')
    search_fields = ('customer__f_name', 'vendor__f_name')
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)


class TransactionStatAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'tot_recvd', 'tot_recv_due', 'tot_items_sold',
                    'tot_payed', 'tot_pay_due', 'tot_items_purchased')
    list_filter = ('timestamp',)
    date_hierarchy = 'timestamp'
    search_fields = ('timestamp',)


class TransactionStatMonthAdmin(admin.ModelAdmin):
    list_display = ('date', 'month_name', 'tot_recvd', 'tot_recv_due', 'tot_items_sold',
                    'tot_payed', 'tot_pay_due', 'tot_items_purchased')
    list_filter = ('date', 'month_name')
    search_fields = ('date',)


admin.site.register(Item, ItemAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Cart)
# admin.site.register(Order)
admin.site.register(Transaction, TransactionAdmin)
# admin.site.register(CartItem)
admin.site.register(TransactionStat, TransactionStatAdmin)
admin.site.register(TransactionStatMonth, TransactionStatMonthAdmin)
admin.site.register(TransactionStatYear)


