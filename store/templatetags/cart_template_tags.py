from django import template
from store.models import Order

register = template.Library()


@register.filter
def cart_item_count(user, session_id=None):
    if user.is_authenticated:
        qs = Order.objects.filter(customer=user, ordered=False)
        if qs.exists():
            return qs[0].order_items.count()
    else:
        qs = Order.objects.filter(customer=None, ordered=False)
        if qs.exists():
            return qs[0].order_items.count()
    return 0

