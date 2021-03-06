from django.urls import path, include
from rest_framework import routers

from .views import (index, inventory,
                    item_detail, item_update, item_delete, add_item,
                    cart_confirm, cart_content, order_transaction, transaction_detail,
                    customer_detail, add_customer, customer_update, customer_delete, customer_stat,
                    vendor_stat, vendor_detail, add_vendor, vendor_update, vendor_delete, transaction_tab,
                    order_transaction_two, pay_due_customer, pay_due_vendor, cart_confirm_add_item, sale, start_sale,
                    start_purchase, make_transaction, populate_with_id, populate_with_qty,
                    form_collect_make_transaction, return_due, populate_with_name, transaction_delete,
                    import_export, export_items_csv, cart_content_inv, export_customer, export_vendor,
                    sale_return, check_date, sale_return_ajax, purchase_return, purchase_return_ajax, ItemViewSet,
                    ajax_discount_form)


router = routers.DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('db/stat/', index, name='dashboard'),
    path('', inventory, name='inventory'),
    path('item/add/', add_item, name='add-item'),
    path('item/detail/<int:pk>/', item_detail, name='item-detail'),
    path('item/update/<int:pk>/', item_update, name='item-update'),
    path('item/delete/<int:pk>/', item_delete, name='item-delete'),
    path('item/sale/<int:pk>/', sale, name='sale-item'),
    path('cart/content/<int:pk>/', cart_content, name='cart-content'),
    path('cart/content/inv/<int:pk>/', cart_content_inv, name='cart-content-inv'),
    path('cart/confirm/<int:pk>/', cart_confirm, name='cart-confirm'),
    path('cart/confirm/item/add/<int:pk>/', cart_confirm_add_item, name='cart-confirm-add-item'),
    path('transaction/<int:pk>/', order_transaction, name='order-transaction'),
    path('transaction/purchase/<int:pk>', order_transaction_two, name='order-transaction-purchase'),
    path('transaction/detail/<int:pk>/', transaction_detail, name='transaction_detail'),
    path('customer/', customer_stat, name='customer'),
    path('customer/detail/<int:pk>/', customer_detail, name='customer-detail'),
    path('customer/add', add_customer, name='add-customer'),
    path('customer/update/<int:pk>/', customer_update, name='customer-update'),
    path('customer/delete/<int:pk>/', customer_delete, name='customer-delete'),
    path('transaction/delete/<int:pk>/', transaction_delete, name='transaction-delete'),

    path('vendor/', vendor_stat, name='vendor'),
    path('vendor/detail/<int:pk>/', vendor_detail, name='vendor-detail'),
    path('vendor/add', add_vendor, name='add-vendor'),
    path('vendor/update/<int:pk>/', vendor_update, name='vendor-update'),
    path('vendor/delete/<int:pk>/', vendor_delete, name='vendor-delete'),
    path('transaction/', transaction_tab, name='transaction-tab'),
    path('pay/due/customer/<int:pk>/', pay_due_customer, name='pay-due-customer'),
    path('pay/due/vendor/<int:pk>/', pay_due_vendor, name='pay-due-vendor'),
    path('start/sale/<int:pk>/', start_sale, name='start-sale'),
    path('start/purchase/<int:pk>/', start_purchase, name='start-purchase'),
    path('make/transaction/', make_transaction, name='entry'),
    path('import/export/', import_export, name='import-export'),
    path('export/csv/', export_items_csv, name='export_items_csv'),
    path('export/customer/', export_customer, name='export-customer'),
    path('export/vendor/', export_vendor, name='export-vendor'),
    path('sale/return/<int:pk>/', sale_return, name='sale-return'),
    path('purchase/return/<int:pk>/', purchase_return, name='purchase-return'),

    path('ajax/id/', populate_with_id, name='ajax-id'),
    path('ajax/name/', populate_with_name, name='ajax-name'),
    path('ajax/qty/', populate_with_qty, name='ajax-qty'),
    path('ajax/make/transaction/', form_collect_make_transaction, name='form-collect'),
    path('ajax/due/', return_due, name='ajax-due'),
    path('ajax/sale/tid/', sale_return_ajax, name='ajax-form-item'),
    path('ajax/purchase/tid/', purchase_return_ajax, name='ajax-purchase-return'),
    path('ajax/check/', check_date, name='ajax-check'),
    path('ajax/discount/form', ajax_discount_form, name='ajax-discount-form'),
    path('ajax/check/other-customer', check_date, name='ajax-check-customer'),
]
