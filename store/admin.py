from django.contrib import admin
from .models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = ('ref_id', 'customer', 'deliveryInfo', 'date_ordered', )
    # list_filter = ("title",)
    # search_fields = ['title', 'category']
    # prepopulated_fields = {'slug': ('title',)}
    list_display_links = ['deliveryInfo', 'customer']


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(SubSubCategory)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(OrderDeliveryInfo)
