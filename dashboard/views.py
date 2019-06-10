import decimal, csv, io, pytz, json
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.safestring import mark_safe

from dashboard.forms import (ItemUpdateForm, ItemAddForm,
                             CartInfo, AddToCartCheckBox, DiscountForm, TransactionForm,
                             CustomerAddForm, CustomerUpdateForm,
                             VendorAddForm, VendorUpdateForm, VendorAddItemForm)

from dashboard.models import (Item, Cart, Order, Transaction, CartItem, Customer, Vendor,
                              TransactionStat, TransactionStatMonth, TransactionStatYear, SalesReturn, ReturnItems,
                              PurchaseReturn)
from accounts.models import Log
from datetime import date, datetime


ktm = pytz.timezone('Asia/Kathmandu')
now = ktm.localize(datetime.now())
day = now.strftime("%A")
month = now.strftime("%B")






def test(request):
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

    return render(request, 'dashboard/test.html', {'user': request.user,
                                                        'items': items, })






@login_required
def transaction_tab(request):
    transac = Transaction.objects.all()
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
            return redirect('cart-content-inv', cart.id)

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
def cart_content_inv(request, pk):
    cart = Cart.objects.get(id=pk)
    cart_item = cart.item.all()
    form = CartInfo(request.POST)
    if request.POST:
        if 'sale' in request.POST:
            print('sale checked')
            if form.is_valid():
                cart_qty = request.POST.getlist('cart_qty')
                i = 0
                for c_i in cart_item:
                    ca, created = CartItem.objects.get_or_create(item=c_i, cart_id=cart.id)
                    ca.cart_qty = int(cart_qty[i])
                    ca.return_qty = int(cart_qty[i])
                    i += 1
                    ca.save()
                return redirect('cart-confirm', cart.id)
        elif 'purchase' in request.POST:
            if form.is_valid():
                cart_qty = request.POST.getlist('cart_qty')
                i = 0
                for c_i in cart_item:
                    ca, created = CartItem.objects.get_or_create(item=c_i, cart_id=cart.id)
                    ca.cart_qty = int(cart_qty[i])
                    ca.return_qty = int(cart_qty[i])
                    i += 1
                    ca.save()
                return redirect('cart-confirm-add-item', cart.id)
    return render(request, 'dashboard/cart_content_inv.html', {'selecs': cart_item})


@login_required
def cart_content(request, pk):
    cart = Cart.objects.get(id=pk)
    cart_item = cart.item.all()
    form = CartInfo(request.POST)
    order = Order.objects.get(cart=cart)
    if request.method == 'POST':
        if form.is_valid():
            cart_qty = request.POST.getlist('cart_qty')
            i = 0
            for c_i in cart_item:
                ca, created = CartItem.objects.get_or_create(item=c_i, cart_id=cart.id)
                ca.cart_qty = int(cart_qty[i])
                ca.return_qty = int(cart_qty[i])
                i += 1
                ca.save()
            if order.vendor:
                return redirect('cart-confirm-add-item', cart.id)
            else:
                return redirect('cart-confirm', cart.id)
    return render(request, 'dashboard/cart_content.html', {'selecs': cart_item})


@login_required
def cart_confirm(request, pk):
    cart = Cart.objects.get(id=pk)
    order = Order.objects.get(cart=cart)

    cart_item = CartItem.objects.filter(cart_id=cart.id)

    # cart and order total details
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



@login_required
def cart_confirm_add_item(request, pk):
    cart = Cart.objects.get(id=pk)
    order = Order.objects.get(cart=cart)

    cart_item = CartItem.objects.filter(cart_id=cart.id)

    # cart and order total details
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
    order.grand_total = tbp
    order.save()
    cart.save()
    return render(request, 'dashboard/cart_confirm_additem.html', {'carts': cart,
                                                                   'order': order,
                                                                   'cart_items': cart_item})


@login_required
def order_transaction(request, pk):
    order = Order.objects.get(id=pk)
    cart_item = CartItem.objects.filter(cart_id=order.cart.id)
    form = TransactionForm(request.POST)
    if request.method == "POST":
        print(request.POST)
        if form.is_valid():
            received = request.POST.get('received')
            if not order.customer:
                customer_pk = request.POST.get('customer')
            # vendor_pk = request.POST.get('vendor')

            if received is '':
                form.instance.received = 0
                form.instance.due_amount = order.grand_total
            else:
                form.instance.received = decimal.Decimal(received)
                form.instance.due_amount = order.grand_total - form.instance.received

            form.instance.type = 'SALE'

            for ca in cart_item:
                up_item = Item.objects.get(item_code=ca.item.item_code)
                up_item.quantity -= ca.cart_qty
                up_item.save()
            form.instance.order = order
            if not order.customer:
                try:
                    customer = Customer.objects.get(id=int(customer_pk))

                except:
                    customer, status = Customer.objects.get_or_create(f_name='Walking', l_name='Customer',
                                                                      phone=54545454, email='others@xyz.com')
            else:
                customer = order.customer

            customer.tot_due += form.instance.due_amount
            customer.tot_recved += form.instance.received
            customer.save()
            form.instance.customer = customer
            messages.success(request, str(order.cart.quantity) + ' items sold successfully!!!')

            form.save()
            return redirect('inventory')

    return render(request, 'dashboard/add_transaction.html', {'form': form,
                                                              'cart_items': cart_item,
                                                              'order': order,
                                                              'transac': form.instance})


def order_transaction_two(request, pk):
    order = Order.objects.get(id=pk)
    cart_item = CartItem.objects.filter(cart_id=order.cart.id)
    form = TransactionForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            received = request.POST.get('received')
            # customer_pk = request.POST.get('customer')
            if not order.vendor:
                vendor_pk = request.POST.get('vendor')
                try:
                    vendor = Vendor.objects.get(id=int(vendor_pk))
                except:
                    vendor, status = Vendor.objects.get_or_create(f_name='Walking', l_name='Vendor',
                                                                      phone=54545454, email='others@xyz.com')
            else:
                vendor = order.vendor

            if received is '':
                form.instance.received = 0
                form.instance.due_amount = order.grand_total
            else:
                form.instance.received = decimal.Decimal(received)
                form.instance.due_amount = order.grand_total - form.instance.received

            for ca in cart_item:
                up_item = Item.objects.get(item_code=ca.item.item_code)
                up_item.quantity += ca.cart_qty
                up_item.save()

            form.instance.order = order
            form.instance.type = 'PURCHASE'

            vendor.tot_due += form.instance.due_amount
            vendor.tot_recved += form.instance.received
            vendor.save()

            form.instance.vendor = vendor
            messages.success(request, str(order.cart.quantity) + ' items purchased successfully!!!')

            form.save()
            return redirect('inventory')

    return render(request, 'dashboard/add_transaction_2.html', {'form': form,
                                                                'order': order,
                                                                'transac': form.instance})


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
                item_code = form.cleaned_data.get('item_code')
                item = form.cleaned_data.get('item_name')
                buying_rate = form.cleaned_data.get('buying_rate')
                sale_rate = form.cleaned_data.get('selling_rate')
                purchase_qty = form.cleaned_data.get('quantity')

                #  total amount/purchase-amount/quantity for cart and order
                amt = float(purchase_qty)*float(buying_rate)
                samt = float(purchase_qty)*float(sale_rate)

                if Item.objects.filter(item_code=item_code) or Item.objects.filter(item_name=item):
                    form.instance.quantity += int(purchase_qty)
                    messages.success(request, "Item Updated Successfully!")
                else:
                    messages.success(request,
                                     str(purchase_qty) + ' ' + str(item) + '`s ' + 'has been created successfully!!! ')

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
                return redirect('cart-confirm-add-item', cart.id)

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
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, "Transaction Deleted Successfully!!!")
        return redirect('transaction-tab')
    context = {
        'transaction': transaction
    }
    return render(request, 'dashboard/transaction_delete.html', context)


@login_required
def customer_stat(request):
    customer = Customer.objects.all().order_by('-date_created')

    prompt = {
        'order': 'Order of the CSV should be id(leave all blank), f_name, l_name, address, phone, email, tot_due, tot_recved'
    }

    if 'customerSubmit' in request.POST:
        print('i am here')
        csv_item_file = request.FILES['myFile']
        if not csv_item_file:
            messages.error(request, 'There is no CSV file!!')

        if not csv_item_file.name.endswith('.csv'):
            messages.error(request, 'This is no CSV file!!')

        data_set = csv_item_file.read().decode('UTF-8')
        to_string = io.StringIO(data_set)
        next(to_string)
        for column in csv.reader(to_string, delimiter=',', quotechar='|'):
            obj, created = Customer.objects.get_or_create(
                f_name=column[0],
                l_name=column[1],
                phone = int(column[3])
            )

            obj.address = column[2]
            obj.email = column[4]
            if column[5] == '':
                obj.tot_due = 0
            else:
                obj.tot_due = decimal.Decimal(column[5])
            if column[6] == "":
                obj.tot_recved = 0
            else:
                obj.tot_recved = decimal.Decimal(column[6])

            obj.save()
        messages.success(request, 'Customer Import Successfull!!!')

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

    if request.method == "POST":
        t_id = request.POST.get('TPK')

        return redirect('sale-return', t_id)
    return render(request, 'dashboard/customer_detail.html', {'customer': customer,
                                                              'transacs': transac,
                                                              't_item': tot_items,
                                                              'now': now,
                                                              })


def start_sale(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    items = Item.objects.all()
    form = AddToCartCheckBox(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            sel_id = request.POST.getlist('ItemPK')
            cart = Cart(quantity=0)
            cart.save()
            for selected in sel_id:
                item = Item.objects.get(id=selected)
                cart.item.add(item)

            order = Order.objects.create(cart=cart, customer=customer)
            return redirect('cart-content', cart.id)

    # paginator = Paginator(items, 10)
    # page = request.GET.get('page')
    # item_page = paginator.get_page(page)
    return render(request, 'dashboard/startsale.html', {'items': items})


def start_purchase(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    items = Item.objects.all()
    form = AddToCartCheckBox(request.POST)
    if request.method == "POST":
        if form.is_valid():
            sel_id = request.POST.getlist('ItemPK')
            cart = Cart(quantity=0)
            cart.save()
            for selected in sel_id:
                item = Item.objects.get(id=selected)
                cart.item.add(item)

            order = Order.objects.create(cart=cart, vendor=vendor)
            return redirect('cart-content', cart.id)
    context = {
        'items': items
    }
    return render(request, 'dashboard/startpurchase.html', context)



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
    prompt = {
        'order': 'Order of the CSV should be id(leave all blank), f_name, l_name, address, phone, email, tot_due, tot_recved'
    }

    if 'vendorSubmit' in request.POST:
        print('i am here')
        csv_item_file = request.FILES['myFile']
        if not csv_item_file:
            messages.error(request, 'There is no CSV file!!')

        if not csv_item_file.name.endswith('.csv'):
            messages.error(request, 'This is no CSV file!!')

        data_set = csv_item_file.read().decode('UTF-8')
        to_string = io.StringIO(data_set)
        next(to_string)
        for column in csv.reader(to_string, delimiter=',', quotechar='|'):
            obj, created = Vendor.objects.get_or_create(
                f_name=column[0],
                l_name=column[1],
                phone=int(column[3])
            )

            obj.address = column[2]
            obj.email = column[4]
            if column[5] == '':
                obj.tot_due = 0
            else:
                obj.tot_due = decimal.Decimal(column[5])
            if column[6] == "":
                obj.tot_recved = 0
            else:
                obj.tot_recved = decimal.Decimal(column[6])

            obj.save()
        messages.success(request, 'Vendor Import Successfull!!!')
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

    if request.method == "POST":
        t_id = request.POST.get('TPK')

        return redirect('purchase-return', t_id)

    return render(request, 'dashboard/vendor_detail.html', {'vendor': vendor,
                                                            'transacs': transac,
                                                            't_item': tot_items,
                                                            'now':now})


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

@login_required
def make_transaction(request):
    it = Item.objects.all()
    items = Item.objects.all().values_list('item_code', 'item_name', 'quantity', 'buying_rate', 'selling_rate')
    customers = Customer.objects.all().values_list('f_name', 'l_name', 'phone')
    vendors = Vendor.objects.all().values_list('f_name', 'l_name', 'phone')

    item_code_array = []
    item_name_array = []
    for item in items:
        item_code_array.append(item[0])
        item_name_array.append(item[1])
    customer_names = []
    for customer in customers:
        customer_names.append(str(customer[0])+' '+str(customer[1]))

    vendor_names = []
    for vendor in vendors:
        vendor_names.append(str(vendor[0]+ ' ' + str(vendor[1])))

    items_json = json.dumps(list(items), cls=DjangoJSONEncoder)
    customers_json = json.dumps(list(customers), cls=DjangoJSONEncoder)
    vendors_json = json.dumps(list(vendors), cls=DjangoJSONEncoder)

    context = {
        'item_code': mark_safe(json.dumps(list(item_code_array), cls=DjangoJSONEncoder)),
        'item_name': mark_safe(json.dumps(list(item_name_array), cls=DjangoJSONEncoder)),
        'customer_name': mark_safe(json.dumps(list(customer_names), cls=DjangoJSONEncoder)),
        'vendor_name': mark_safe(json.dumps(list(vendor_names), cls=DjangoJSONEncoder)),
        'items': it,
    }
    return render(request, 'dashboard/make_transaction.html', context)

@login_required
def populate_with_name(request):
    item_name = request.POST['item_name']
    try:
        item = get_object_or_404(Item, item_name=item_name)
        test = 1
        data = {
            'itemCode': item.item_code,
            'itemName': item.item_name,
            'itemQty': item.quantity,
            'itemBuyRate': item.buying_rate,
            'itemSaleRate': item.selling_rate,
            'message': test
        }
    except ObjectDoesNotExist:
        test = 0
        data = {
            'message': test
        }
    return JsonResponse(data)

@login_required
def populate_with_id(request):
    id = request.GET.get('item_id')
    try:
        item = Item.objects.get(item_code=id)
        test = 1
        data = {
            'itemCode': item.item_code,
            'itemName': item.item_name,
            'itemQty': item.quantity,
            'itemBuyRate': item.buying_rate,
            'itemSaleRate': item.selling_rate,
            'message': test
        }
    except ObjectDoesNotExist:
        test = 0
        data = {
            'message': test
        }
    return JsonResponse(data)

@login_required
def populate_with_qty(request):
    qty = request.GET.get('item_qty')
    id = request.GET.get('item_id')
    t_type = request.GET.get('t_type')
    item = Item.objects.get(item_code=id)
    if t_type == '1':
        total = decimal.Decimal(qty)*item.selling_rate
    elif t_type == '2':
        total = decimal.Decimal(qty) * item.buying_rate
    data = {
        'itemTotal': total
    }
    return JsonResponse(data)

@login_required
def form_collect_make_transaction(request):
    if request.method == 'POST':
        form_dict = request.POST.dict()
        tot_items = request.POST['tot_items']
        tot_rendered = request.POST['tot_rendered']
        tot_amt = request.POST['tot_amt']

        if tot_rendered == '':
            tot_rendered = 0
        if tot_amt == '':
            tot_amt = 0
        if tot_items == '':
            tot_items = 0


        keys = []
        values = []
        b = 1
        for k, v in form_dict.items():
            if k.__contains__('name'):
                keys.append(v)
            elif k.__contains__('value'):
                values.append(v)
        print(keys)
        print(values)
        if values[1] == '1' or values[1] == '2':                    #SALES
            idpos = [id_pos for id_pos, x in enumerate(keys) if x == 'id']
            qtypos = [qty_pos for qty_pos, x in enumerate(keys) if x == 'qty']
            cart = Cart(quantity=tot_items)
            cart.save()

            a = 0
            for posn in idpos:
                item = Item.objects.get(item_code=values[posn])
                cart.item.add(item)
                CartItem.objects.create(item=item, cart_id=cart.id, cart_qty=values[qtypos[a]], return_qty=values[qtypos[a]])
                if values[1] == '1':
                    item.quantity -= int(values[qtypos[a]])
                else:
                    item.quantity += int(values[qtypos[a]])
                item.save()
                a = a+1
            transaction = Transaction.objects.create()

            recievedposn = keys.index('p_amt')
            p_type_posn = keys.index('payment_type')
            if values[recievedposn] == '':
                recieved = 0
            else:
                recieved = decimal.Decimal(values[recievedposn])

            if values[p_type_posn] == '1':
                payment_type = 'CASH'
            else:
                payment_type = 'CREDIT'
                recieved = 0

            if values[1] == '1':
                order = Order.objects.create(cart=cart,
                                             tot_sale_price=decimal.Decimal(tot_amt),
                                             grand_total=decimal.Decimal(tot_rendered))
                customerposn = keys.index('customer')
                customer_name = values[customerposn]
                if customer_name == '' or not customer_name:
                    customer, status = Customer.objects.get_or_create(f_name='Not', l_name='Registered',
                                                                      email='others@xyz.com')
                else:
                    cust_name = customer_name.split()
                    customer = Customer.objects.get(f_name=cust_name[0], l_name=cust_name[1])
                transaction.customer = customer
                print(transaction.customer)
                transaction.type = 'SALE'
                due = order.grand_total - recieved
                customer.tot_due += due
                customer.tot_recved += recieved
            else:
                order = Order.objects.create(cart=cart,
                                             tot_buy_price=decimal.Decimal(tot_amt),
                                             grand_total=decimal.Decimal(tot_rendered))
                vendorposn = keys.index('vendor')
                vend_name = values[vendorposn]
                if vend_name == '' or not vend_name:
                    vendor, status = Vendor.objects.get_or_create(f_name='Not', l_name='Registered',
                                                                  email='others@xyz.com')
                else:
                    customer_name = vend_name.split()
                    vendor = Vendor.objects.get(f_name=customer_name[0], l_name=customer_name[1])
                transaction.vendor = vendor
                transaction.type = 'PURCHASE'
                due = order.grand_total - recieved
                vendor.tot_due += due
                vendor.tot_recved += recieved

            discperposn = keys.index('disc_per')
            discamtposn = keys.index('disc_amt')
            if values[discamtposn] == '' and values[discperposn] == '':
                order.disc_amt = 0
                order.disc_per = 0
            elif values[discamtposn] == '' and values[discperposn]:
                order.disc_amt = 0
                order.disc_per = decimal.Decimal(values[discperposn])
            elif values[discamtposn] and values[discperposn] == '':
                order.disc_amt = decimal.Decimal(values[discamtposn])
                order.disc_per = 0
            order.save()
            transaction.order = order
            transaction.received = recieved
            transaction.due_amount = due
            transaction.payment_type = payment_type
            transaction.save()

        elif values[1] == '3':                #PAY_DUE
            p_amt = decimal.Decimal(values[11])
            cust = values[8]
            if not cust or cust == '':
                customer = None
            else:
                customer_name = cust.split()
                customer = Customer.objects.get(f_name=customer_name[0], l_name=customer_name[1])
                if customer.tot_due > 0:
                    customer.tot_due -= p_amt
                    customer.tot_recved += p_amt
                    Transaction.objects.create(customer=customer,
                                               due_amount=customer.tot_due, type='PAYDUE',
                                               recieved=p_amt, payment_type='CASH')
                    customer.save()
            vend = values[9]
            if not vend or vend == '':
                vendor = None
            else:
                vendor_name = vend.split()
                vendor = Vendor.objects.get(f_name=vendor_name[0], l_name=vendor_name[1])
                if vendor.tot_due > 0:
                    vendor.tot_due -= p_amt
                    vendor.tot_recved += p_amt
                    vendor.save()
                    Transaction.objects.create(type="PAYDUE", payment_type="CASH", received=p_amt, due_amount=vendor.tot_due,
                                               vendor=vendor,
                                               order=None)
        print("----------------------------------------")
    data = {
        'message': 'Mission Successful'
    }
    return JsonResponse(data)

@login_required
def return_due(request):
    if request.method == 'FILES':
        customer = request.FILES['customer']
        if customer or customer != '':
            customer_name = customer.split()
            cust = Customer.objects.get(f_name=customer_name[0],
                                        l_name=customer_name[1])
            data = {
                'customerDue': cust.tot_due
            }
            return JsonResponse(data)
        else:
            data = {
                'customerDue': 'Invalid Data'
            }
            return JsonResponse


@login_required()
def import_export(request):
    prompt = {
        'order': 'Order of the CSV should be id(leave all blank), item_code, item_name, quantity, buying_rate, selling_rate, minimum_stock, location_in_store, description'
    }

    if request.method == "GET":
        return render(request, 'dashboard/import_export.html', prompt)

    if 'itemSubmit' in request.POST:
        csv_item_file = request.FILES['myFile']

        if not csv_item_file.name.endswith('.csv'):
            messages.error(request, 'This is no CSV file!!')

        data_set = csv_item_file.read().decode('UTF-8')
        to_string = io.StringIO(data_set)
        next(to_string)
        for column in csv.reader(to_string, delimiter=',', quotechar='|'):
            obj, created = Item.objects.get_or_create(
                item_code=column[0],
                item_name=column[1],
            )
            print(decimal.Decimal(column[3]))
            obj.buying_rate = decimal.Decimal(column[3])
            obj.selling_rate = decimal.Decimal(column[4])
            obj.minimum_stock = int(column[5])
            obj.location_in_store = column[6]
            obj.description = column[7]
            if created:
                obj.quantity = column[2]
            else:
                obj.quantity += int(column[2])
            obj.save()
        messages.success(request, 'File Import Successfull!!!')


    context = {}
    return render(request, 'dashboard/import_export.html', context)

@login_required
def export_items_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="item_list.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Item Code',
        'Item Name',
        'Quantity',
        'Buying Rate',
        'Selling Rate',
        'Minimum Stock',
        'Location in Store'
    ])

    items = Item.objects.all().values_list(
        'item_code',
        'item_name',
        'quantity',
        'buying_rate',
        'selling_rate',
        'minimum_stock',
        'location_in_store'
    )
    for item in items:
        writer.writerow(item)

    return response

@login_required
def export_customer(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customer_list.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'First Name',
        'Last Name',
        'Address',
        'Phone',
        'Email',
        'Total Due',
        'Total Received'
    ])

    customers = Customer.objects.all().values_list(
        'f_name',
        'l_name',
        'address',
        'phone',
        'email',
        'tot_due',
        'tot_recved'
    )
    for customer in customers:
        writer.writerow(customer)

    return response

@login_required
def export_vendor(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customer_list.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'First Name',
        'Last Name',
        'Address',
        'Phone',
        'Email',
        'Total Due',
        'Total Received'
    ])

    vendors = Vendor.objects.all().values_list(
        'f_name',
        'l_name',
        'address',
        'phone',
        'email',
        'tot_due',
        'tot_recved'
    )
    for vendor in vendors:
        writer.writerow(vendor)

    return response


@login_required
def purchase_return(request, pk):
    transaction = Transaction.objects.get(id=pk)
    cart_id = transaction.order.cart.id
    cart_items = CartItem.objects.filter(cart_id=cart_id)

    context = {
        'transaction': transaction,
        'cart_items': cart_items
    }
    return render(request, 'dashboard/purchase_return.html', context)

@login_required()
def sale_return(request, pk):
    transaction = Transaction.objects.get(id=pk)
    cart_id = transaction.order.cart.id
    cart_items = CartItem.objects.filter(cart_id=cart_id)
    print(cart_items)


    context = {
        'transaction': transaction,
        'cart_items': cart_items
    }
    return render(request, 'dashboard/sale_return.html', context)


def sale_return_ajax(request):
    if request.method == "POST":
        form_data = request.POST.dict()
        approve = request.POST['accept']
        print(approve)
        t_id = request.POST['t_id']
        transaction = Transaction.objects.get(id=t_id)
        print(transaction.customer)
        keys = []
        values = []
        for k, v in form_data.items():
            if k.__contains__('name'):
                keys.append(v)
            elif k.__contains__('value'):
                values.append(v)
        del keys[0]
        del values[0]
        c = 0
        for val in values:
            if val == '':
                c += 0
            else:
                c += int(val)
        if c != 0:
            print(keys)
            print(values)
            i = 0
            total_return = 0
            total_return_items = 0
            for i in range(0, len(keys)):
                item = Item.objects.get(item_code=keys[i])
                if values[i] == '':
                    remove_qty = 0
                else:
                    remove_qty = int(values[i])
                return_amt = remove_qty * item.selling_rate
                total_return += return_amt
                total_return_items += remove_qty
            data = {

                'totalReturn': total_return,
                'totalReturnItems': total_return_items,
                'customerName': transaction.customer.get_customer_name(),
                'cId': transaction.customer.id
            }
            if approve == "false":
                print('hello')
                data['message'] = 'unchecked'
                return JsonResponse(data)
            elif approve == 'true':
                print('wow')
                sr = SalesReturn.objects.create(customer=transaction.customer)
                print(sr.id)
                for i in range(0, len(keys)):
                    item = Item.objects.get(item_code=keys[i])
                    if values[i] == '':
                        remove_qty = 0
                    else:
                        remove_qty = int(values[i])
                        item.quantity += remove_qty
                        item.save()
                        ri = ReturnItems.objects.get_or_create(item=item, return_id=sr.id, qty=remove_qty)
                        sr.item.add(item)
                        sr.return_amount = total_return
                        transaction.customer.tot_recved -= total_return
                        transaction.customer.save()
                        cart_id = transaction.order.cart.id
                        c_item = CartItem.objects.get(cart_id=cart_id, item=item)
                        c_item.return_qty -= remove_qty
                        c_item.save()
                        sr.save()
                        messages.success(request, 'Sale return successfull!!!')
                        data['message'] = 'success'
                return JsonResponse(data)
        else:
            data = {
                'message': 'empty'
            }
            return JsonResponse(data)




def purchase_return_ajax(request):
    if request.method == "POST":
        form_data = request.POST.dict()
        approve = request.POST['accept']
        print(approve)
        t_id = request.POST['t_id']
        transaction = Transaction.objects.get(id=t_id)
        print(transaction.vendor)
        keys = []
        values = []
        for k, v in form_data.items():
            if k.__contains__('name'):
                keys.append(v)
            elif k.__contains__('value'):
                values.append(v)
        del keys[0]
        del values[0]
        c = 0
        for val in values:
            if val == '':
                c += 0
            else:
                c += int(val)
        if c != 0:
            print(keys)
            print(values)
            i = 0
            total_return = 0
            total_return_items = 0
            for i in range(0, len(keys)):
                item = Item.objects.get(item_code=keys[i])
                if values[i] == '':
                    remove_qty = 0
                else:
                    remove_qty = int(values[i])
                return_amt = remove_qty * item.selling_rate
                total_return += return_amt
                total_return_items += remove_qty
            data = {

                'totalReturn': total_return,
                'totalReturnItems': total_return_items,
                'vendorName': transaction.vendor.get_vendor_name(),
                'vId': transaction.vendor.id
            }
            if approve == "false":
                print('hello')
                data['message'] = 'unchecked'
                return JsonResponse(data)
            elif approve == 'true':
                print('wow')
                pr = PurchaseReturn.objects.create(vendor=transaction.vendor)
                print(pr.id)
                for i in range(0, len(keys)):
                    item = Item.objects.get(item_code=keys[i])
                    if values[i] == '':
                        remove_qty = 0
                    else:
                        remove_qty = int(values[i])
                        item.quantity -= remove_qty
                        item.save()
                        ri = ReturnItems.objects.get_or_create(item=item, return_id=pr.id, qty=remove_qty)
                        pr.item.add(item)
                        pr.return_amount = total_return
                        transaction.vendor.tot_recved -= total_return
                        transaction.vendor.save()
                        cart_id = transaction.order.cart.id
                        c_item = CartItem.objects.get(cart_id=cart_id, item=item)
                        c_item.return_qty -= remove_qty
                        c_item.save()
                        pr.save()
                        messages.success(request, 'Purchase return successfull!!!')
                        data['message'] = 'success'
                return JsonResponse(data)
        else:
            data = {
                'message': 'empty'
            }
            return JsonResponse(data)




@login_required()
def check_date(request):
    id = request.GET.get('transaction_id')
    print(id)
    transaction = Transaction.objects.get(id=id)
    timestamp = (transaction.timestamp - now).total_seconds()
    if timestamp/86400 < 7:
        check = 'true'
    else:
        check = 'false'
    data = {
        'check': check
    }
    return JsonResponse(data)

