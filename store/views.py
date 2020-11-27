import random
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .forms import CheckoutForm
from .models import *


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


class StoreList(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'store/home.html'
    paginate_by = 10


class ShopProduct(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'store/products.html'
    paginate_by = 10


class Product_details(DetailView):
    model = Product
    template_name = 'store/product_details.html'


#
def cart(request):
    # checking if the user is authenticated
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, ordered=False).order_by('-date_ordered')
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items.order_by('-date_ordered')
    else:
        items = []  # when a user isn't authenticated
        order = {'get_cart-total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}

    return render(request, 'store/cart.html', context)


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        user=request.user,
        product=product
    )
    order_qs = Order.objects.filter(customer=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(product__pk=product.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'this item quantity was updated ')
            return redirect('cart', )
        else:
            messages.info(request, 'this item was added to your cart ')

            order.order_items.add(order_item)
            return redirect('cart', )
    else:

        order = Order.objects.create(customer=request.user, ref_id=create_ref_code())

        order.order_items.add(order_item)
        messages.info(request, 'this item was added to your cart ')
        return redirect('cart')


class CartIterms(LoginRequiredMixin, View):
    def get(self, orgs, *args, **kwargs):

        try:
            order = Order.objects.get(customer=self.request.user, ordered=False)
            context = {
                'cart_items': order
            }
            return render(self.request, 'store/cart.html', context=context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have thr active order')
            return redirect('/')


@login_required
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
                user=request.user,
                ordered=False
            )[0]
            """
            then finally we remove that oder from cart completely
            """
            order.order_items.remove(order_item)
            messages.info(request, 'this item was removed from your cart ')
            return redirect('cart', )
        else:
            # a message to the user that there is no that kind of query set
            messages.info(request, 'this item was was not in your cart ')
            return redirect('/', )
    else:
        messages.info(request, "You don't have an active order")
        return redirect('/')


@login_required
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
                user=request.user,
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


class CheckOut(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(customer=self.request.user, ordered=False)
        form = CheckoutForm()
        context = {
            'order': order,
            'form': form
        }
        return render(self.request, 'store/checkout.html', context)

    def post(self, *args, **kwargs):
        order = Order.objects.get(customer=self.request.user, ordered=False)
        form = CheckoutForm(self.request.POST)
        if form.is_valid():
            address = form.cleaned_data.get('address')
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')
            zipcode = form.cleaned_data.get('zipcode')
            #  added field
            description = form.cleaned_data.get('description')
            shipping_address = ShippingAddress()
            shipping_address.customer = self.request.user
            shipping_address.state = state
            shipping_address.address = address
            shipping_address.city = city
            shipping_address.zipcode = zipcode
            shipping_address.description = description
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
        else:
            messages.success(self.request, 'form is not ok')
            return redirect('checkout')


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
