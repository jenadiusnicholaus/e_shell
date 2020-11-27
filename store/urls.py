from django.urls import path
from . import views

urlpatterns = [
    path('', views.StoreList.as_view(), name="home"),
    path('product/', views.ShopProduct.as_view(), name="product"),
    path('product_details/<int:pk>/', views.Product_details.as_view(), name="product_details"),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name="add_to_cart"),
    path('cart/', views.CartIterms.as_view(), name="cart"),
    path('remove_from_cart/<int:pk>/', views.remove_from_cart, name="remove_from_cart"),
    path('remove_single_item_from_cart/<int:pk>/', views.remove_single_item_from_cart,
         name="remove_single_item_from_cart"),
    path('remove_from_cart/<int:pk>/', views.remove_from_cart, name="remove_from_cart"),
    path('checkout/', views.CheckOut.as_view(), name="checkout"),

]
