import hashlib
import json
import os
import random
import string

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from authentication.models import User
from .forms import CheckoutForm, EditProductForm, GuestUserForm
from .models import *
from .utils import cookieCart, save_delivery


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def search_product(request):
    if request.method == 'GET':
        query = request.GET.get('q')

        product_submitted = request.GET.get('submit')

        if query is not None:
            lookups = Q(name__icontains=query) | Q(name__icontains=query)

            results = Product.objects.filter(lookups).distinct()
            recommend_product = OrderItem.objects.filter(ordered=False).order_by('-date_added')[:3]

            context = {'results': results,
                       'submitbutton': product_submitted,
                       'recommend': recommend_product,
                       }

            return render(request, 'store/search_result.html', context)

        else:
            return render(request, 'store/search_result.html')
    else:
        return render(request, 'store/search_result.html')


class Home(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter()
        recommend_product = OrderItem.objects.filter(ordered=False).order_by('-date_added')[:3]
        product = Product.objects.all()
        if self.request.user.is_authenticated:

            context = {

                'products': product,
                'categories': categories,
                'recomend': recommend_product,
            }
            return render(self.request, template_name='store/home.html', context=context)

        else:
            cookie_date = cookieCart(self.request)
            order = cookie_date['order']
            order_items = cookie_date['order_items']

            context = {
                'order': order,
                'products': product,
                'categories': categories,
            }
            return render(self.request, template_name='store/home.html', context=context)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Home, self).get_context_data(**kwargs)
        # Add in the publisher
        recommend_product = OrderItem.objects.filter(ordered=False).order_by('-date_added')[:3]
        category = Category.objects.all().order_by('-create_on')
        context.update(
            {
                'categories': category,
                'recommend': recommend_product,

            }
        )
        return context


class SubCategoriesDateils(DetailView):
    model = SubCategory
    template_name = 'store/sub_categories_details.html'

    def get_context_data(self, **kwargs):
        context = super(SubCategoriesDateils, self).get_context_data()
        sub_sub_categories = SubSubCategory.objects.all()
        recommend_product = OrderItem.objects.filter(ordered=False).order_by('-date_added')
        context.update(
            {
                'sub_sub_categories': sub_sub_categories,
                'recommend': recommend_product,

            }

        )
        return context


class SubSubCategoriesDateils(DetailView):
    model = SubSubCategory
    template_name = 'store/subsubcategory.html'

    def get_context_data(self, **kwargs):
        context = super(SubSubCategoriesDateils, self).get_context_data()
        recommend_product = OrderItem.objects.filter(ordered=False).order_by('-date_added')
        context.update(
            {
                'recommend': recommend_product,
            }
        )
        return context


class ShopProduct(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'store/products.html'
    paginate_by = 10


class ProductDetails(DetailView):
    model = Product
    template_name = 'store/product_details.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetails, self).get_context_data(**kwargs)
        category = Category.objects.all().order_by('-create_on')
        recommend_product = OrderItem.objects.filter(ordered=False).order_by('-date_added')
        form = EditProductForm()
        context.update(
            {'form': form,
             'categories': category,
             'recommend': recommend_product
             }
        )
        return context


# @login_required()
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.is_ajax and request.method == 'POST':
        # get the form data
        form = EditProductForm(request.POST)
        # save the data and after fetch the object in instance
        if form.is_valid():
            instance = form.cleaned_data.get('quantity')
            # get the item to edit
            # TODO
            try:
                # trying to edit a product before getting to cart
                order_item, created = OrderItem.objects.get_or_create(
                    product=product,
                    customer=request.user,
                    ordered=False
                )
                order_qs = Order.objects.get(customer=request, ordered=False)
                if order_qs.exists():
                    order = order_qs[0]
                    if order.order_items.filter(product__pk=product.pk).exists():
                        order_item.quantity += int(instance)
                        messages.success(request, 'editing is successfully ')
                        return redirect('product_details', pk=product.pk)
                    else:
                        order.order_items.add(order_item)
                        messages.success(request, 'order added to order items ')
                        return redirect('product_details', pk=product.pk)

                else:
                    order = Order.objects.create(
                        customer=request.user,
                        ordered=False,
                    )
                    order.order_items.add(order_item)
                    messages.success(request, 'cart was create successfully')
                    return redirect('cart')
            except ObjectDoesNotExist as e:

                return redirect('checkour')
            # serialize in new friend object in json
            # serialize_instance = serializers.serialize('json', [instance])
            # send to client side.
            # return JsonResponse({"messages": 'product has been edited successfully'},
            #                     status=200)
        else:
            return JsonResponse({"error": form.errors}, status=400)
    return JsonResponse({"error": " form no valid"}, status=400)


def add_to_cart(request, pk):
    if request.user.is_authenticated:
        try:
            customer = request.user
        except:
            device_id = request.COOKIES['device'],
            print(device_id)
            customer, created = User.objects.get_or_create(
                device_id=device_id
            )
        product = get_object_or_404(Product, pk=pk)
        order_item, created = OrderItem.objects.get_or_create(
            customer=customer,
            product=product,
        )
        order_qs = Order.objects.filter(customer=customer, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.order_items.filter(product__pk=product.pk).exists():
                order_item.quantity += 1
                order_item.save()
                messages.success(request, 'this item quantity was updated ')
                return redirect('home', )
            else:

                order.order_items.add(order_item)
                messages.success(request, 'This item was added to your cart ')
                return redirect('home', )

        else:

            order = Order.objects.create(customer=customer, ref_id=create_ref_code())

            order.order_items.add(order_item)
            messages.success(request, 'this item was added to your cart ')
            return redirect('home')
    else:
        product = get_object_or_404(Product, pk=pk)

        device_id = request.COOKIES['device'],
        print(device_id)
        customer, created = User.objects.get_or_create(
            device_id=device_id
        )
        order_item, created = OrderItem.objects.get_or_create(
            customer=customer,
            product=product,
        )
        # if not request.session.session_key:
        #     request.session.create()
        # session_id = request.session.session_key

        order_qs = Order.objects.filter(customer=customer, ordered=False, session_key=request.session.session_key)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.order_items.filter(product__pk=product.pk).exists():
                order_item.quantity += 1
                order_item.save()

                messages.success(request, 'this item is already added to cart ')
                return redirect('home')
            else:
                order.order_items.add(order_item)
                messages.success(request, 'This item was added to your cart ')
                return redirect('cart')
        else:

            order = Order.objects.create(
                customer=customer
            )
            order.order_items.add(order_item)
            messages.success(request, 'Your item is added successfully')
    return redirect("cart")


class CartItems(View):
    def get(self, orgs, *args, **kwargs):

        if self.request.user.is_authenticated:
            # grab the loged-in used
            customer = self.request.user
            try:
                # query the oder filtering by logged in user and ordered not
                order = Order.objects.get(customer=customer, ordered=False)
                order_items = order.order_items.all()

            except:
                messages.info(self.request, ' No item in the cart')
                return redirect('home')

            context = {
                'order': order,
                'order_items': order_items
            }


            return render(self.request, 'store/cart.html', context=context)
        else:
            cookie_date = cookieCart(self.request)
            order = cookie_date['order']
            order_items = cookie_date['order_items']

            context = {
                'order': order,
                'order_items': order_items
            }

        return render(self.request, 'store/cart.html', context=context)


class AddDeliveryInfo(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            order = Order.objects.get(customer=request.user, ordered=False)


        else:
            device_id = request.COOKIES['device'],
            print(device_id)
            customer, created = User.objects.get_or_create(
                device_id=device_id
            )
            order = Order.objects.get(customer=customer, ordered=False)

        if request.method == "POST":
            pickup_order_at_station = request.POST.get('pickup_order_at_station')
            deliver_my_order = request.POST.get("deliver_my_order")
            insure_my_order = request.POST.get('insure_my_order')
            same_day_delivery = request.POST.get('same_day_delivery')
            express_delivery = request.POST.get('express_delivery')

            delivery_info = OrderDeliveryInfo()
            if request.user.is_authenticated:
                delivery_info.user = request.user
            else:
                delivery_info.user = customer
            delivery_info.pickup_order_at_station = pickup_order_at_station
            delivery_info.deliver_my_order = deliver_my_order
            delivery_info.insure_my_order = insure_my_order
            delivery_info.same_day_delivery = same_day_delivery
            delivery_info.express_delivery = express_delivery

            delivery_info.save()

            # update the order
            order.deliveryInfo = delivery_info
            order.save()
            messages.success(self.request, 'Delivery info has been updated')
            return redirect('checkout')


def remove_from_cart(request, pk):
    # let get an item from thr item list
    product = get_object_or_404(Product, pk=pk)
    # let check if the user has the oder in that is not ordered yet
    order_qs = Order.objects.filter(customer=request.user, ordered=-False)
    # if that the user has the order in the order list
    if order_qs.exists():
        # then grab the that order
        order = order_qs[0]
        # and check the specific oder item regarding to slug item in the request
        if order.order_items.filter(product__pk=product.pk).exists():
            """
             after that now we need to grab that oder from the oder_item by filtering using
             user in request and ordered not, and the item itself
            """
            order_item = OrderItem.objects.filter(
                product=product,
                customer=request.user,
                ordered=False
            )[0]
            """
            then finally we remove that oder from cart completely
            """
            order.order_items.remove(order_item)
            messages.success(request, 'this item was removed from your cart ')
            return redirect('cart', )
        else:
            # a message to the user that there is no that kind of query set
            messages.warning(request, 'this item was was not in your cart ')
            return redirect('/', )
    else:
        messages.warning(request, "You don't have an active order")
        return redirect('/')


def remove_single_item_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        customer=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.order_items.filter(product__pk=product.pk).exists():
            order_item = OrderItem.objects.filter(
                product__pk=product.pk,
                customer=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.order_items.remove(order_item)
            messages.info(request, "This item qty was updated.")
            return redirect("cart")
        else:
            # add a message saying the user dosent have an order
            messages.info(request, "Item was not in your cart.")
            return redirect("/", )
    else:
        # add a message saying the user dosent have an order
        messages.info(request, "u don't have an active order.")
        return redirect("/", )


def get_hashed_password(password):
    """  hash password on company register"""
    password = password.encode()
    salt = os.urandom(16)
    password_hash = hashlib.pbkdf2_hmac("sha256", password, salt, 100000)

    return password_hash


class CheckOut(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                order = Order.objects.get(customer=self.request.user, ordered=False)
                order_items = order.order_items.all()
            except ObjectDoesNotExist as e:
                messages.warning(request, 'No Product to checkout')
                return redirect('home')

            form = CheckoutForm()
            context = {
                'order': order,
                'order_items': order_items,
                'form': form,
            }
            return render(self.request, 'store/checkout.html', context)
        else:
            guestUserForm = GuestUserForm()
            cookie_date = cookieCart(self.request)
            order = cookie_date['order']
            order_items = cookie_date['order_items']
            form = CheckoutForm()
            context = {
                'order': order,
                'form': form,
                'order_items': order_items,
                'guest_form': guestUserForm,
            }
            return render(self.request, template_name='store/checkout.html', context=context)

    def post(self, *args, **kwargs):

        if self.request.user.is_authenticated:
            order = Order.objects.get(customer=self.request.user, ordered=False)
            form = CheckoutForm(self.request.POST)

            if form.is_valid():
                address1 = form.cleaned_data.get('address1')
                address2 = form.cleaned_data.get('address2')
                city = form.cleaned_data.get('city')
                region = form.cleaned_data.get('region')
                tin_number = form.cleaned_data.get('tin_number')
                country = form.cleaned_data.get('country')
                pay_option = form.cleaned_data.get('pay_option')
                phone = form.cleaned_data.get('phone')
                #  added field
                if not address1:
                    messages.warning(self.request, f'{address1} not optional')
                    return redirect('checkout')
                if not city:
                    messages.warning(self.request, f'{city} not optional')
                    return redirect('checkout')
                if not region:
                    messages.warning(self.request, f'{region} not optional')
                    return redirect('checkout')
                if not tin_number:
                    messages.warning(self.request, f'{tin_number} not optional')
                    return redirect('checkout')
                if not country:
                    messages.warning(self.request, f'{country} not optional')
                    return redirect('checkout')
                description = form.cleaned_data.get('description')
                shipping_address = ShippingAddress()
                shipping_address.customer = self.request.user

                shipping_address.region = region
                shipping_address.address1 = address1
                shipping_address.address2 = address2
                shipping_address.pay_option = pay_option
                shipping_address.tin_number = tin_number
                shipping_address.country = country
                shipping_address.phone = phone
                shipping_address.city = city
                shipping_address.description = description
                shipping_address.payment_option = pay_option
                shipping_address.save()

                order.shippingAddress = shipping_address
                order.save()

                # redirect to payment option
                payment_option = self.request.POST.get('option')

                if payment_option == 'paypal':
                    print(payment_option)
                    messages.success(self.request, ' Chosen paypal')
                    return redirect('payment', payment_option=payment_option)
                elif payment_option:
                    print(payment_option)
                    messages.success(self.request, ' Chosen skrill')
                    return redirect('payment', payment_option=payment_option)
                messages.success(self.request, 'Form submitted successfully')
                return redirect('checkout')
            else:
                print(form.data)
                messages.success(self.request, 'form is not ok')
                return redirect('checkout')

        else:
            if self.request.method == 'POST' and self.request.is_ajax():
                form = GuestUserForm(self.request.POST)
                # save the data and after fetch the object in instance
                if form.is_valid():
                    username = form.cleaned_data.get('username')
                    email = form.cleaned_data.get('email')
                    password = form.cleaned_data.get('password')
                    print(username)
                    print(email)
                    print(password)
                    customer, created = User.objects.get_or_create(
                        email=email
                    )
                    customer.username = username
                    customer.password = get_hashed_password(password)
                    customer.save()

                    cartadata = cookieCart(self.request)
                    items = cartadata['order_items']

                    for item in items:
                        product = Product.objects.get(pk=item['product']['id'])

                        orderitem, created = OrderItem.objects.get_or_create(
                            product=product,
                            customer=customer
                        )
                        order_qs = Order.objects.filter(customer=customer, ordered=False)
                        if order_qs.exists():
                            order = order_qs[0]
                            if order.order_items.filter(product__id=product.pk).exists():
                                orderitem.quantity = item['quantity']
                                orderitem.save()
                                print('order updated')
                                return redirect('checkout')
                            else:
                                order.order_items.add(orderitem)
                                print('order updated')
                                return redirect('checkout')

                        else:
                            order = Order.objects.create(
                                ref_id=create_ref_code(),
                                customer=customer
                            )
                            order.order_items.add(orderitem)
                            print('order created')
                            user_auth = authenticate(email=email, password=get_hashed_password(password))
                            if user_auth:
                                # we need to check if the auth_user is activate to our system
                                if user_auth.is_active:
                                    # if not request.POST.get('remember_me', None):
                                    # make the session to end in one mouth
                                    login(self.request, user_auth)
                                    messages.info(self.request, 'welcome home ')
                                    return redirect('/')

                                else:
                                    messages.info(self.request,
                                                  'Your account was inactive.Try to activate your account now')
                                    return redirect('sign_in')
                            else:
                                print("Someone tried to login and failed.")
                                print("They used username: {} and password: {}".format(email, password))
                                messages.warning(self.request, 'Invalid login details given,')

                                return redirect('checkout')

                    # serialize in new friend object in json
                    # ser_instance = serializers.serialize('json', [form, ])
                    # send to client side.
                    return redirect('checkout')
                else:
                    # some form errors occured.
                    return JsonResponse({"error": form.errors}, status=400)
                # some error occured
            return JsonResponse({"error": ""}, status=400)


class Payment(View):
    def get(self, request, payment_option, *args, **kwargs):
        order = Order.objects.get(customer=self.request.user, ordered=False)
        context = {
            'order': order
        }
        if payment_option == 'skrill':
            return render(request, template_name='store/skrill.html', context=context)
        elif payment_option == 'paypal':
            return render(request, template_name='store/skrill.html', context=context)
