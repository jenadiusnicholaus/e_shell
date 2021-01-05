import json
from django.shortcuts import get_object_or_404

from .models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
        # print(cart)
    except:
        cart = {}
    # assign all the item in a list
    order_items = []
    # calculate all number
    order = {
        'get_cart_total': 0,
        'get_cart_items': 0,
        'cart_items_count': 0,
        'get_total_product_vat': 0,
    }

    for product_id in cart:
        try:
            # get the product with an id from the cookie

            product = get_object_or_404(Product, pk=product_id)
            # find total for each product in cart as
            total = (product.price * cart[product_id]['quantity'])
            order['get_cart_items'] += cart[product_id]["quantity"]

            # update cort item count in cart
            order['cart_items_count'] += 1
            # update cart total in cart
            order['get_cart_total'] += total
            order['get_total_product_vat'] = (order['get_cart_total']*18)/100
            #   let now create our order item
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'image': product.image,
                    'price': product.price,
                },
                'quantity': cart[product_id]['quantity'],
                'get_total': total,
            }
            order_items.append(item)
        except:
            pass
    return {
        'order': order,
        'order_items': order_items
    }


def cartData(request):
    return {}


def save_delivery(request):
    pass
