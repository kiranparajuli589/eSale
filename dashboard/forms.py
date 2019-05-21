from django import forms
from django.forms import ModelChoiceField

from .models import Item, Cart, Order, Transaction, Customer, Vendor


class ItemAddForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_code', 'item_name', 'quantity', 'buying_rate', 'selling_rate', 'location_in_store',
                  'minimum_stock', 'description', 'item_image']


class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_code', 'item_name', 'buying_rate', 'selling_rate', 'location_in_store',
                  'minimum_stock', 'description']


class VendorAddItemForm(forms.Form):
    id = forms.CharField(max_length=5, required=False)
    item_name = forms.CharField(max_length=50, required=False)
    quantity = forms.IntegerField(min_value=0, required=False)
    buy_price = forms.DecimalField(decimal_places=2, max_digits=8, min_value=0, required=False)
    sale_price = forms.DecimalField(decimal_places=2, max_digits=8, min_value=0, required=False)


class AddToCartCheckBox(forms.Form):
    add = forms.CheckboxInput()


class CartInfo(forms.Form):
    cart_qty = forms.IntegerField(required=False)


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['disc_per', 'disc_amt']


class TransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['customer'] = ModelChoiceField(queryset=Customer.objects.all().order_by('id'),
                                                   empty_label="Others",
                                                   required=False)
        self.fields['vendor'] = ModelChoiceField(queryset=Vendor.objects.all().order_by('id'),
                                                   empty_label="Others",
                                                   required=False)
    class Meta:
        model = Transaction
        fields = ['payment_type', 'received']


class CustomerAddForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['f_name', 'l_name', 'address', 'phone','email', 'image']


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['date_created']


class VendorAddForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['f_name', 'l_name', 'address', 'phone', 'email', 'image']


class VendorUpdateForm(forms.ModelForm):
    class Meta:
        model = Vendor
        exclude = ['date_created']


class EntryForm(forms.Form):
    item_code = forms.CharField(max_length=10, required=False)
    item_name = forms.CharField(max_length=50, required=False)
    item_qty = forms.IntegerField(required=True, min_value=0)