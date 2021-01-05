from django.urls import path
from . import views

urlpatterns = [
    path('update_item/', views.updateItem, name="update_item"),
    path('', views.Home.as_view(), name="home"),
    path('product/', views.ShopProduct.as_view(), name="product"),
    path('product_details/<int:pk>/', views.ProductDetails.as_view(), name="product_details"),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name="add_to_cart"),
    path('cart/', views.CartItems.as_view(), name="cart"),
    path('remove_from_cart/<int:pk>/', views.remove_from_cart, name="remove_from_cart"),
    path('remove_single_item_from_cart/<int:pk>/', views.remove_single_item_from_cart,
         name="remove_single_item_from_cart"),
    path('remove_from_cart/<int:pk>/', views.remove_from_cart, name="remove_from_cart"),
    path('checkout/', views.CheckOut.as_view(), name="checkout"),
    # Delivery
    path('add_delivery_info/', views.AddDeliveryInfo.as_view(), name="add_delivery_info"),
    path('sub_categories/<int:pk>/', views.SubCategoriesDateils.as_view(), name="sub_categories"),
    path('sub_sub_categories/<int:pk>/', views.SubSubCategoriesDateils.as_view(), name="sub_sub_categories"),
    path('search/', views.search_product, name="search"),
    path('edit_product/<int:pk>', views.edit_product, name="edit_product"),

]
