import decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404

from dashboard.forms import (ItemUpdateForm, ItemAddForm,
                             CartInfo, AddToCartCheckBox, DiscountForm, TransactionForm,
                             CustomerAddForm, CustomerUpdateForm,
                             VendorAddForm, VendorUpdateForm, TransactionMiniForm)

from dashboard.models import (Item, Cart, Order, Transaction, CartItem, Customer, Vendor,
                              TransactionStat, TransactionStatMonth, TransactionStatYear)
from accounts.models import Log
from datetime import date, datetime
import pytz


ktm = pytz.timezone('Asia/Kathmandu')
now = ktm.localize(datetime.now())
day = now.strftime("%A")
month = now.strftime("%B")


@login_required
def transaction_tab(request):
    transac = Transaction.objects.all().order_by('-timestamp')
    return render(request, 'dashboard/transaction_tab.html', {'transacs': transac})


@login_required
def index(request):

    transc = Transaction.objects.all().order_by('-timestamp')[:10]

    # creating transaction detail of every day
    tr_today = Transaction.objects.filter(timestamp__year=date.today().year, timestamp__month=date.today().month,
                                          timestamp__day=date.today().day)
    trd, status = TransactionStat.objects.get_or_create(timestamp=now.date())
    trd.tot_items_purchased = 0
    trd.tot_payed = 0
    trd.tot_pay_due = 0
    trd.tot_items_sold = 0
    trd.tot_recvd = 0
    trd.tot_recv_due = 0

    for t in tr_today:

        if t.type == 'SALE':
            trd.tot_items_sold += t.order.cart.quantity
            trd.tot_recvd += t.received
            trd.tot_recv_due += t.due_amount
            trd.save()
        if t.type == 'PURCHASE':
            trd.tot_items_purchased += t.order.cart.quantity
            trd.tot_payed += t.received
            trd.tot_pay_due += t.due_amount
            trd.save()
        if t.type == 'PAYDUE':
            if t.customer:
                trd.tot_recvd += t.received
                trd.tot_recv_due -= t.received
            if t.vendor:
                trd.tot_payed += t.received
                trd.tot_pay_due -= t.received

    trm = Transaction.objects.filter(timestamp__year=date.today().year, timestamp__month=date.today().month)

    #  creating transactin stat for every month
    try:
        tr_month = TransactionStatMonth.objects.get(date=str(date.today().year)+'-'+str(date.today().month))
    except ObjectDoesNotExist:
        tr_month = TransactionStatMonth.objects.create(date=str(date.today().year)+'-'+str(date.today().month),
                                                       month_name=month)

    for tr in trm:
        if tr.type == 'SALE':
            tr_month.tot_recvd += tr.received
            tr_month.tot_recv_due += tr.due_amount
            tr_month.tot_items_sold += tr.order.cart.quantity
        if tr.type == 'PURCHASE':
            tr_month.tot_payed += tr.received
            tr_month.tot_pay_due += tr.due_amount
            tr_month.tot_items_purchased += tr.order.cart.quantity
        if tr.type == 'PAYDUE':
            if tr.customer:
                tr_month.tot_recvd += tr.received
                tr_month.tot_recv_due -= tr.received
            if tr.vendor:
                tr_month.tot_payed += tr.received
                tr_month.tot_pay_due -= tr.received

    # collecting yearly transaction data
    tr_y = Transaction.objects.filter(timestamp__year=date.today().year)

    try:
        tr_year = TransactionStatYear.objects.get(year=str(date.today().year))
    except ObjectDoesNotExist:
        tr_year = TransactionStatYear.objects.create(year=str(date.today().year))

    for tr in tr_y:
        if tr.type == 'SALE':
            tr_year.tot_recvd += tr.received
            tr_year.tot_recv_due += tr.due_amount
            tr_year.tot_items_sold += tr.order.cart.quantity
        if tr.type == 'PURCHASE':
            tr_year.tot_payed += tr.received
            tr_year.tot_pay_due += tr.due_amount
            tr_year.tot_items_purchased += tr.order.cart.quantity
        if tr.type == 'PAYDUE':
            if tr.customer:
                tr_year.tot_recvd += tr.received
                tr_year.tot_recv_due -= tr.received
            if tr.vendor:
                tr_year.tot_payed += tr.received
                tr_year.tot_pay_due -= tr.received

    return render(request, 'dashboard/dboard.html', {'user': request.user, 'transacs': transc,
                                                     'now': now, 'day': day, 'month': month,
                                                     'stat_day': trd, 'stat_month':tr_month, 'stat_year': tr_year})


@login_required
def transaction_detail(request, pk):
    transac = Transaction.objects.get(id=pk)
    if not transac.type == 'PAYDUE':
        item = CartItem.objects.filter(cart_id=transac.order.cart.id)
    else:
        item = None
    return render(request, 'dashboard/transaction_detail.html', {'transac': transac,
                                                                 'cart_item': item})


@login_required
def inventory(request):
    items = Item.objects.all().order_by('-id')
    form = AddToCartCheckBox(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            sel_id = request.POST.getlist('ItemPK')
            cart = Cart(quantity=0)
            cart.save()
            for selected in sel_id:
                item = Item.objects.get(id=selected)
                cart.item.add(item)

            order = Order.objects.create(cart=cart)
            return redirect('cart-content', cart.id)

    return render(request, 'dashboard/inventory.html', {'user': request.user,
                                                        'items': items,})


@login_required()
def sale(request, pk):
    item = Item.objects.get(pk=pk)
    cart = Cart(quantity=0)
    cart.save()
    cart.item.add(item)
    order = Order.objects.create(cart=cart)
    return redirect('cart-content', cart.id)


@login_required
def cart_content(request, pk):
    cart = Cart.objects.get(id=pk)
    cart_item = cart.item.all()
    form = CartInfo(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            cart_qty = request.POST.getlist('cart_qty')
            i = 0
            for c_i in cart_item:
                ca = CartItem(item=c_i, cart_id=cart.id)
                if cart_qty[i] is '' or int(cart_qty[i]) < 0:
                    ca.cart_qty += 0
                # elif int(cart_qty[i]) > c_i.quantity:
                #     messages.warning(request, str(c_i.item_name)+' : ITEM QUANTITY EXCEED!!\nAVAILABLE QUANTITY : '+str(c_i.quantity))
                #     return redirect('cart-content', pk)
                else:
                    ca.cart_qty = int(cart_qty[i])
                i += 1
                ca.save()
            return redirect('cart-confirm', cart.id)
    return render(request, 'dashboard/cart_content.html', {'selecs': cart_item})


@login_required
def cart_confirm(request, pk):
    cart = Cart.objects.get(id=pk)
    order = Order.objects.get(cart=cart)

    cart_item = CartItem.objects.filter(cart_id=cart.id)

    # cart and order total details
    if not order.grand_total:
        tqty = 0
        tbp = 0
        tsp = 0
        for c_i in cart_item:
            tqty += c_i.cart_qty
            tbp += c_i.get_cart_buy_price()
            tsp += c_i.get_cart_sale_price()

        cart.quantity = tqty
        order.tot_buy_price = tbp
        order.tot_sale_price = tsp
        order.grand_total = tsp
        order.save()
        cart.save()

    form = DiscountForm(request.POST)

    if request.method == "POST":
        if form.is_valid():
            disc_per = form.cleaned_data.get('disc_per')
            disc_amt = form.cleaned_data.get('disc_amt')
            if disc_per and disc_amt:
                messages.warning(request, "[Error]Both Discount Field Configured!!")
                return redirect('cart-confirm', cart.id)
            if disc_per:
                amt = disc_per/100*order.tot_sale_price
                order.disc_amt = amt
                order.grand_total = order.get_gt_amt()
                order.save()
            if disc_amt:
                order.disc_amt = disc_amt
                order.grand_total = order.get_gt_amt()
                order.save()
            return render(request, 'dashboard/cart_confirm.html', {'carts': cart,
                                                                   'form': form,
                                                                   'order': order,
                                                                   'cart_items': cart_item})

    return render(request, 'dashboard/cart_confirm.html', {'carts': cart,
                                                           'form': form,
                                                           'order': order,
                                                           'cart_items': cart_item})


def cart_confirm_add_item(request, pk):  # TODO
    cart = Cart.objects.get(id=pk)
    order = Order.objects.get(cart=cart)

    cart_item = CartItem.objects.filter(cart_id=cart.id)

    # cart and order total details
    if not order.grand_total:
        tqty = 0
        tbp = 0
        tsp = 0
        for c_i in cart_item:
            tqty += c_i.cart_qty
            tbp += c_i.get_cart_buy_price()
            tsp += c_i.get_cart_sale_price()

        cart.quantity = tqty
        order.tot_buy_price = tbp
        order.tot_sale_price = tsp
        order.grand_total = tsp
        order.save()
        cart.save()

    form = DiscountForm(request.POST)

    if request.method == "POST":
        if form.is_valid():
            disc_per = form.cleaned_data.get('disc_per')
            disc_amt = form.cleaned_data.get('disc_amt')
            if disc_per and disc_amt:
                messages.warning(request, "[Error]Both Discount Field Configured!!")
                return redirect('cart-confirm-add-item', cart.id)  # TODO
            if disc_per:
                amt = disc_per/100*order.tot_buy_price
                order.disc_amt = amt
                order.grand_total -= order.disc_amt
                order.save()
            if disc_amt:
                order.disc_amt = disc_amt
                order.grand_total -= disc_amt
                order.save()
            return render(request, 'dashboard/cart_confirm.html', {'carts': cart,
                                                                   'form': form,
                                                                   'order': order,
                                                                   'cart_items': cart_item})

    return render(request, 'dashboard/cart_confirm.html', {'carts': cart,
                                                           'form': form,
                                                           'order': order,
                                                           'cart_items': cart_item})


@login_required
def order_transaction(request, pk):
    order = Order.objects.get(id=pk)
    cart_item = CartItem.objects.filter(cart_id=order.cart.id)
    form = TransactionMiniForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            print(form.instance.type)
            if form.instance.type == 'SALE':
                for ca in cart_item:
                    up_item = Item.objects.get(item_code=ca.item.item_code)
                    up_item.quantity -= ca.cart_qty
                    up_item.save()

            if form.instance.type == 'PURCHASE':
                pass
            form.instance.order = order
            form.save()
            return redirect('order-transaction-2', form.instance.id)

    return render(request, 'dashboard/add_transaction.html', {'form': form,
                                                              'order': order})


@login_required
def order_transaction_two(request, pk):
    transaction = Transaction.objects.get(id=pk)

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)

        if form.is_valid():
            received = request.POST.get('received')
            customer_pk = request.POST.get('customer')
            vendor_pk = request.POST.get('vendor')

            if received is '':
                form.instance.received = 0
                form.instance.due_amount = transaction.order.grand_total
            else:
                form.instance.received = decimal.Decimal(received)
                form.instance.due_amount = transaction.order.grand_total-form.instance.received

            if form.instance.type == 'SALE':
                try:
                    customer = Customer.objects.get(id=int(customer_pk))

                except:
                    customer, status = Customer.objects.get_or_create(f_name='Not', l_name='Registered',
                                                                      email='others@xyz.com')

                customer.tot_due += form.instance.due_amount
                customer.tot_recved += form.instance.received
                customer.save()

                form.instance.customer = customer
                messages.success(request, str(transaction.order.cart.quantity) + ' items sold successfully!!!')

            if form.instance.type == "PURCHASE":
                try:
                    vendor = Vendor.objects.get(id=int(vendor_pk))

                except:
                    vendor, status = Vendor.objects.get_or_create(f_name='Not', l_name='Registered',
                                                                  email='others@xyz.com')

                vendor.tot_due += form.instance.due_amount                            
                vendor.tot_recved += form.instance.received
                vendor.save()

                form.instance.vendor = vendor
                messages.success(request, str(transaction.order.cart.quantity) + ' items purchased successfully!!!')

            form.save()
            return redirect('inventory')
    else:
        form = TransactionForm(instance=transaction)

    return render(request, 'dashboard/add_transaction_2.html', {'form': form,
                                                                'transac': transaction})


@login_required
def item_detail(request, pk):
    item = Item.objects.get(pk=pk)
    try:
        cart_item = CartItem.objects.filter(item=item).last()
        transaction = Transaction.objects.get(order__cart__id=cart_item.cart_id, type='PURCHASE')

        context = {
            'item': item,
            'purchase': transaction
        }
    except:
        context = {
            'item': item
        }
    return render(request, 'dashboard/item_detail.html', context)


@login_required
def add_item(request):
    if request.method == "POST":
        user = request.user
        if user.is_admin:
            form = ItemAddForm(request.POST,
                               request.FILES)
            if form.is_valid():

                item = form.cleaned_data.get('item_name')
                buying_rate = form.cleaned_data.get('buying_rate')
                sale_rate = form.cleaned_data.get('selling_rate')
                purchase_qty = form.cleaned_data.get('quantity')

                #  total amount/purchase-amount/quantity for cart and order
                amt = float(purchase_qty)*float(buying_rate)
                samt = float(purchase_qty)*float(sale_rate)

                form.save()  # item added to db
                item = Item.objects.get(item_name=item)

                cart = Cart(quantity=purchase_qty)  # cart created for form instance
                cart.save()
                cart.item.add(item)

                cart_item = CartItem.objects.create(cart_id=cart.id, item=item,
                                                    cart_qty=purchase_qty, cart_amt=amt)
                order = Order.objects.create(cart=cart,
                                             tot_buy_price=amt,
                                             tot_sale_price=samt,
                                             grand_total=amt)
                messages.success(request,
                                 str(purchase_qty)+' ' + str(item) + '`s ' + 'has been created successfully!!! ')
                Log.objects.create(user=request.user,
                                   subject="Add Item",
                                   detail='Item Name:' + str(item) + ' Quantity :' + str(purchase_qty) + '\n'
                                          + 'Buying Rate: ' + str(buying_rate) + ' Selling Rate: ' + str(sale_rate))
                return redirect('cart-confirm-add-item', cart.id)

        else:
            messages.warning(request, 'Permission Denied!!')
            return redirect('inventory')
    else:
        form = ItemAddForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/add_item.html', context)


@login_required
def item_update(request, pk):
    item = Item.objects.get(pk=pk)
    if request.method == 'POST':
        form = ItemUpdateForm(request.POST, instance=item)
        if form.is_valid():

            qty = request.POST.get('QTY')
            br = form.cleaned_data.get('buying_rate')
            sr = form.cleaned_data.get('selling_rate')

            if qty:
                amt = float(qty) * float(br)
                s_amt = float(qty) * float(sr)
                form.instance.quantity += int(qty)  # updating item quantity

                cart = Cart(quantity=qty)
                cart.save()
                cart.item.add(item)

                cart_item = CartItem.objects.create(cart_id=cart.id, item=item,
                                                    cart_qty=qty, cart_amt=amt)
                order = Order.objects.create(cart=cart, tot_buy_price=amt,
                                             grand_total=amt, tot_sale_price=s_amt)
                form.save()
                return redirect('cart-confirm', cart.id)

            form.save()

            messages.success(request, 'Item has been updated!')
            Log.objects.create(user=request.user,
                               subject="Update Item",
                               detail='Item Name:' + str(item) + ' Quantity :' + str(qty) + '\n'
                                      + 'Buying Rate: ' + str(br) + ' Selling Rate: ' + str(sr))
            return redirect('inventory')

    else:
        form = ItemUpdateForm(instance=item)

    context = {
        'form': form,
    }
    return render(request, 'dashboard/item_update.html', context)


@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Item Deleted Successfully!!!")
        return redirect('inventory')
    context = {
        'item': item
    }
    return render(request, 'dashboard/item_delete.html', context)


@login_required
def customer_stat(request):
    customer = Customer.objects.all().order_by('-date_created')
    return render(request, 'dashboard/customer_admin.html', {'customers': customer})


@login_required
def add_customer(request):
    user = request.user
    form = CustomerAddForm(request.POST)
    if user.is_admin:
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, str(form.instance.f_name) + ' is added to store successfully')
                Log.objects.create(user=request.user, subject='ADD CUSTOMER',
                                   detail='Name: ' + str(form.instance.f_name) + ' ' +
                                          str(form.instance.l_name) + '; Created Successfully')
                return redirect('customer')
    else:
        messages.warning(request, "Permission Denied")
        redirect('customer')
    return render(request, 'dashboard/add_customer.html', {'form': form})


@login_required
def customer_update(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == "POST":
        user = request.user
        if user.is_admin:
            form = CustomerUpdateForm(request.POST, instance=customer)
            if form.is_valid():
                form.save()
                messages.success(request, customer.get_customer_name() + str(' updated successfully!!'))
                Log.objects.create(user=request.user, subject='UPDATE VENDOR',
                                   detail='Name: ' + str(form.instance.f_name) + ' ' +
                                          str(form.instance.l_name) + '; UPDATED Successfully')
                return redirect('customer-detail', customer.id)
        else:
            messages.warning(request, 'Permission Denied!!')
            return redirect('customer-detail', customer.id)
    else:
        form = CustomerUpdateForm(instance=customer)
    context = {
        'form': form,
        'customer': customer
    }
    return render(request, 'dashboard/customer_update.html', context)


@login_required
def customer_detail(request, pk):
    customer = Customer.objects.get(id=pk)
    transac = Transaction.objects.filter(customer=customer)

    tot_due = 0
    tot_received = 0
    tot_items = 0
    for tr in transac:
        if not tr.type == 'PAYDUE':
            tot_due += tr.due_amount
            tot_items += tr.order.cart.quantity
            tot_received += tr.received

    return render(request, 'dashboard/customer_detail.html', {'customer': customer,
                                                              'transacs': transac,
                                                              't_item': tot_items})


@login_required()
def pay_due_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        amount = request.POST.get('PAYDUE')
        amt = decimal.Decimal(amount)
        if customer.tot_due > 0:
            customer.tot_due -= amt
            customer.tot_recved += amt
            customer.save()
            messages.success(request, 'Rs '+str(amt)+' submitted!! Due has been updated successfully!!!')
            Transaction.objects.create(customer=customer, due_amount=customer.tot_due, received=amt,
                                       payment_type='CASH', order=None, type='PAYDUE')
            Log.objects.create(user=request.user,
                               subject='DUE PAYMENT',
                               detail='DATE: '+str(now)+'\nCustomer Name:' + customer.get_customer_name() + '\t PAID AMOUNT: '+str(amt))
        else:
            messages.warning(request, 'Zero Due amount for selected customer!!')
            return redirect('customer-detail', customer.id)
        return redirect('customer-detail', customer.id)

    return render(request, 'dashboard/pay_due.html', {'customer': customer})


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, "Customer Deleted Successfully!!!")
        Log.objects.create(user=request.user, subject='CUSTOMER DELETE',
                           detail=str(customer.get_customer_name())+' deleted from database!!')
        return redirect('customer')
    context = {
        'customer': customer
    }
    return render(request, 'dashboard/customer_delete.html', context)


@login_required
def vendor_stat(request):
    vendor = Vendor.objects.all().order_by('-date_created')
    return render(request, 'dashboard/vendor_admin.html', {'vendors': vendor})


@login_required
def add_vendor(request):
    user = request.user
    form = VendorAddForm(request.POST)
    if user.is_admin:
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, str(form.instance.f_name) + ' is added to store successfully')
                Log.objects.create(user=request.user, subject='ADD VENDOR', detail='Name: '+str(form.instance.f_name)+' '+
                                   str(form.instance.l_name)+'; Created Successfully')
                return redirect('vendor')
    else:
        messages.warning(request, "Permission Denied")
        redirect('vendor')
    return render(request, 'dashboard/add_vendor.html', {'form': form})


@login_required
def vendor_update(request, pk):
    vendor = Vendor.objects.get(id=pk)
    if request.method == "POST":
        user = request.user
        if user.is_admin:
            form = VendorUpdateForm(request.POST, instance=vendor)
            if form.is_valid():
                form.save()
                messages.success(request, vendor.get_vendor_name()+str(' updated successfully!!'))
                Log.objects.create(user=request.user, subject='UPDATE VENDOR',
                                   detail='Name: ' + str(form.instance.f_name) + ' ' +
                                          str(form.instance.l_name) + '; UPDATED Successfully')
                return redirect('vendor-detail', vendor.id)
        else:
            messages.warning(request, 'Permission Denied!!')
            return redirect('vendor-detail', vendor.id)
    else:
        form = VendorUpdateForm(instance=vendor)
    context = {
        'form': form,
        'vendor': vendor
    }
    return render(request, 'dashboard/vendor_update.html', context)


@login_required
def vendor_detail(request, pk):
    vendor = Vendor.objects.get(id=pk)
    transac = Transaction.objects.filter(vendor=vendor)

    tot_due = 0
    tot_received = 0
    tot_items = 0
    for tr in transac:
        if not tr.type == 'PAYDUE':
            tot_due += tr.due_amount
            tot_items += tr.order.cart.quantity
            tot_received += tr.received

    return render(request, 'dashboard/vendor_detail.html', {'vendor': vendor,
                                                            'transacs': transac,
                                                            't_item': tot_items})


@login_required()
def pay_due_vendor(request, pk):
    vendor = Vendor.objects.get(id=pk)
    if request.method == 'POST':
        amount = request.POST.get('PAYDUE')
        amt = decimal.Decimal(amount)
        if vendor.tot_due > 0:
            vendor.tot_due -= amt
            vendor.tot_recved += amt
            vendor.save()
            messages.success(request, 'Rs ' + str(amt) + ' submitted!! Due has been updated successfully!!!')
            Transaction.objects.create(type="PAYDUE", payment_type="CASH", received=amt, due_amount=amt, vendor=vendor,
                                       order=None)
            Log.objects.create(user=request.user,
                               subject='DUE PAYMENT',
                               detail='DATE: '+str(now)+'\nVendor Name:' + vendor.get_vendor_name() + '\t PAID AMOUNT: '+str(amt))
        else:
            messages.warning(request, 'Zero Due amount for selected customer!!')
            return redirect('vendor-detail', vendor.id)
        return redirect('vendor-detail', vendor.id)

    return render(request, 'dashboard/pay_due_vendor.html', {'vendor': vendor})


@login_required
def vendor_delete(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == 'POST':
        vendor.delete()
        messages.success(request, "Vendor Deleted Successfully!!!")
        Log.objects.create(user=request.user, subject='VENDOR DELETE',
                           detail=str(vendor.get_vendor_name()) + ' deleted from database!!')
        return redirect('vendor')
    context = {
        'vendor': vendor
    }
    return render(request, 'dashboard/vendor_delete.html', context)

