from django.urls import path
from .views import staff_index, products_list, ProductUpdateView, delete_product, add_product
from authentication.views import staff_login, staff_logout

urlpatterns =[
	path('staff/', staff_index, name='staff_index'),
	path('products/', products_list, name='products_list'),
	path('add_product/', add_product, name='add_product'),
	path('edit_product/<int:pk>/', ProductUpdateView.as_view(), name='edit_product'),
	path('delete_product/<int:id>', delete_product, name='delete_product'),
	path('login/', staff_login, name='login'),
	path('logout/', staff_logout, name='logout')
]