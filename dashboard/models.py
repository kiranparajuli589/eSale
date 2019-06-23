from django.db import models
from PIL import Image
import pytz
from datetime import datetime
from accounts.models import User

ktm = pytz.timezone('Asia/Kathmandu')
now = ktm.localize(datetime.now())

payment_type = (
    ('CASH', 'Cash'),
    ('CREDIT', 'Credit')
)
trans_type = (
    ('PURCHASE', 'PURCHASE'),
    ('SALE', 'SALE'),
    ('PAYDUE', 'PAYDUE'),
    # ('SALE-RETURN', 'SALE-RETURN'),
    # ('PURCHASE-RETURN', 'PURCHASE-RETURN')
)


class Item(models.Model):
    item_code = models.CharField(max_length=10, unique=True)
    item_name = models.CharField(max_length=255, unique=True)
    quantity = models.IntegerField(default=0)
    buying_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    selling_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    minimum_stock = models.IntegerField(null=True, blank=True)

    location_in_store = models.TextField(null=True, blank=True)  # location in inventory
    buying_rate_prev = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    selling_rate_prev = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    item_image = models.ImageField(default='default_item.jpeg', upload_to='item_images')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.item_name

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.item_image.path)

        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.item_image.path)


class Inventory(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Actor(models.Model):
    f_name = models.CharField(max_length=50, verbose_name='First Name')
    l_name = models.CharField(max_length=50, verbose_name='Last Name')

    address = models.CharField(max_length=50, null=True, blank=True)
    phone = models.IntegerField(verbose_name='Phone Number', unique=True)
    email = models.EmailField(unique=True, max_length=50, verbose_name='Email Address', blank=True, null=True)
    date_created = models.DateTimeField(default=now, verbose_name='Registered Date')

    tot_due = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    tot_recved = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    class Meta:
        abstract = True
        ordering = ['f_name']

    def __str__(self):
        return "%s %s" % (self.f_name, self.l_name)


class Vendor(Actor):
    image = models.ImageField(default='default.jpg', upload_to='vendor', verbose_name='Image(Vendor)')

    class Meta:
        verbose_name_plural = "Vendors"

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_vendor_name(self):
        return ("%s %s" % (self.f_name, self.l_name)).upper()

    get_vendor_name.short_description = 'Name'


class Customer(Actor):
    image = models.ImageField(default='default.jpg', upload_to='customer', verbose_name='Image(Customer)')

    class Meta:
        verbose_name_plural = "Customers"

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_customer_name(self):
        return ("%s %s" % (self.f_name, self.l_name)).upper()

    get_customer_name.short_description = 'Name'


class CartItem(models.Model):
    cart_id = models.IntegerField(default=0)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, default=0)
    cart_qty = models.IntegerField(default=0)
    return_qty = models.IntegerField(default=0)
    cart_amt = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    def get_cart_buy_price(self):
        return self.cart_qty*self.item.buying_rate

    def get_cart_sale_price(self):
        return self.cart_qty*self.item.selling_rate


class ReturnItems(models.Model):
    item = models.ForeignKey(Item, null=True, default=0, on_delete=models.CASCADE)
    return_id = models.CharField(max_length=20)
    qty = models.IntegerField()


class Cart(models.Model):
    item = models.ManyToManyField(Item, null=True, default=0)
    quantity = models.IntegerField(null=True, blank=True)  # total quantity of items in cart
    # amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True) # total

    def __str__(self):
        return 'Cart'+str(self.id)


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)
    # total_qty = models.IntegerField(default=0)
    tot_buy_price = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    tot_sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=8)

    disc_per = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    disc_amt = models.DecimalField(default=0, max_digits=8, decimal_places=2, null=True, blank=True)

    grand_total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def get_gt_amt(self):
        if self.tot_sale_price:
            return self.tot_sale_price-self.disc_amt
        elif self.tot_buy_price:
            return self.tot_buy_price-self.disc_amt

    def __str__(self):
        return "%s %s" % ('order', str(self.id))


class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, unique=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True, unique=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(default=now)
    received = models.DecimalField(max_digits=8, decimal_places=2, default=0, blank=True)  # received from customer or payed to vendor
    due_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    payment_type = models.CharField(max_length=6, choices=payment_type, default='CASH')
    type = models.CharField(max_length=10, choices=trans_type, default='SALE')

    def __str__(self):
        if self.customer:
            return self.customer.get_customer_name()
        elif not self.customer:
            return 'Other '+str(self.id)

    class Meta:
        ordering = ['-timestamp']


return_type = (
    ('SALE-RETURN', 'SALE-RETURN'),
    ('PURCHASE-RETURN', 'PURCHASE-RETURN')
)





class TransactionStat(models.Model):
    tot_recvd = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    tot_payed = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    tot_recv_due = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    tot_pay_due = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    tot_items_sold = models.IntegerField(default=0)
    tot_items_purchased = models.IntegerField(default=0)
    timestamp = models.DateField(default=now.date())


class TransactionStatMonth(models.Model):
    tot_recvd = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    tot_payed = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    tot_recv_due = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    tot_pay_due = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    tot_items_sold = models.IntegerField(default=0)
    tot_items_purchased = models.IntegerField(default=0)
    date = models.CharField(max_length=10)
    month_name = models.CharField(max_length=10)


class TransactionStatYear(models.Model):
    tot_recvd = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    tot_payed = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    tot_recv_due = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    tot_pay_due = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    tot_items_sold = models.IntegerField(default=0)
    tot_items_purchased = models.IntegerField(default=0)
    year = models.CharField(max_length=10)


class PurchaseReturn(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    item = models.ManyToManyField(Item, null=True, default=0)
    return_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    timestamp = models.DateTimeField(default=now)


class SalesReturn(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    item = models.ManyToManyField(Item, null=True, default=0)
    return_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True)
    timestamp = models.DateTimeField(default=now)


class ReturnTransaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(default=now)
    return_amt = models.DecimalField(max_digits=8, decimal_places=2, default=0, blank=True)
    type = models.CharField(max_length=10, choices=return_type, default='SALE-RETURN')
    sale_return = models.ForeignKey(SalesReturn, on_delete=models.CASCADE, null=True, blank=True)
    purchase_return = models.ForeignKey(PurchaseReturn, on_delete=models.CASCADE, null=True, blank=True)




