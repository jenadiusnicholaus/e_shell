from django.urls import path
from .views import *
from authentication.views import staff_login, staff_logout

urlpatterns =[
	path('staff/', products_list, name='staff_index'),

	path('products/', products_list, name='products_list'),
	path('add_product/', add_product, name='add_product'),
	path('edit_product/<int:pk>/', ProductUpdateView.as_view(), name='edit_product'),
	path('delete_product/<int:id>', delete_product, name='delete_product'),

	path('products-category/', Product_category, name='Product_category'),
	path('edit_category/<int:pk>/', CategoryUpdateView.as_view(), name='edit_category'),
	path('delete_category/<int:id>', delete_category, name='delete_category'),

	path('products-sub-category/', Product_sub_category, name='Product_sub_category'),
	path('edit_sub_category/<int:pk>/', SubCategoryUpdateView.as_view(), name='edit_sub_category'),
	path('delete_sub_category/<int:id>', delete_sub_category, name='delete_sub_category'),


	path('products-sub-sub-category/', Product_sub_sub_category, name='Product_sub_sub_category'),
	path('edit_sub_sub_category/<int:pk>/', SubSubCategoryUpdateView.as_view(), name='edit_sub_sub_category'),
	path('delete_sub_sub_category/<int:id>', delete_sub_sub_category, name='delete_sub_sub_category'),


	path('login/', staff_login, name='login'),
	path('logout/', staff_logout, name='logout')
]