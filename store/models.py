from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.datetime_safe import datetime

from e_shell import settings


class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    create_on = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Product Category'

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    create_on = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name_plural = 'Product Sub Category'

    def __str__(self):
        return self.name


class Product(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    discount= models.CharField(max_length=200, null= True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    available = models.CharField(max_length=30, null=True, blank=True)
    label = models.CharField(max_length=30, null=True)
    description = models.TextField(max_length=20, null=True)

    def __str__(self):
        return self.name

    @property  # When an image isn't uploaded for a product, return empty string to avoid errors (called in home.html)
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={
            'pk': self.pk
        })

    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs={
            'pk': self.pk
        })

    def get_remove_single_item_from_cart(self):
        return reverse('remove_single_item_from_cart', kwargs={'pk': self.pk})


class OrderItem(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    ordered = models.BooleanField(default=False, null=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Ordered products'

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return f'{self.product.name} Quantity of {self.quantity}'


class Order(models.Model):
    ref_id = models.CharField(max_length=40, null=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    order_items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False, null=True)
    deliveryInfo = models.ForeignKey('OrderDeliveryInfo', on_delete=models.CASCADE, null=True)
    shippingAddress = models.ForeignKey('ShippingAddress', on_delete=models.CASCADE, null=True)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.customer)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.order_items.all()
        for i in orderitems:
            if not i.product.digital:
                shipping = True
        return shipping

    # Getting the total value of the cart
    @property
    def get_cart_total(self):
        orderitems = self.order_items.all()
        total = sum([item.get_total for item in orderitems])
        return total

    # Getting the total value of the item
    @property
    def get_cart_items_total(self):
        total_items = 0
        orderitems = self.order_items.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderDeliveryInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    pickup_order_at_station = models.CharField(max_length=200, null=True)
    deliver_my_order = models.CharField(max_length=200, null=True)
    insure_my_order = models.CharField(max_length=200, null=True)
    same_day_delivery = models.CharField(max_length=200, null=True)
    express_delivery = models.CharField(max_length=200, null=True)

    def __str__(self):
        return 'Delivery info'


class ShippingAddress(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    # order must have shipping address and not viscera
    # order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    # added field
    description = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.address
