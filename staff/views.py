from django.shortcuts import render,get_object_or_404, redirect
from store.models import Product
from django.views.generic import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import ProductForm 


@login_required(login_url= '/login')
def staff_index(request):
	return render(request, 'staff/index.html')

@login_required(login_url= '/login')
def products_list(request):
	products = Product.objects.all()
	context ={
	 'products':products
	}
	return render(request, 'staff/product-list.html', context)


# class ProductAdd(LoginRequiredMixin, CreateView):
#     model = Product
#     template_name = 'staff/product-add.html'
#     fields = ['name', 'price', 'image']
#     success_url = '/products'
    

#     def form_valid(self, form):
#         form.instance.user =self.request.user
#         return super().form_valid(form)


def add_product(request):
	if request.method == 'POST':
		form = ProductForm(request.POST or None, request.FILES)
		product = Product()
		if form.is_valid():
			#product.sub_category = 'ENGINE OIL DIESEL'
			product.name = request.POST.get('name')
			product.price = request.POST.get('price')
			product.image = request.FILE.get('image')
			product.product_by = request.user
			product.save()
			print(product)
			return redirect('products_list')
		else:
			messages.error(request, 'Post error')
			return redirect('add_product')
	form = ProductForm()
	context={
		'form':form
	}
	return render(request, 'staff/product-add.html', context)


class ProductUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'staff/product-edit.html'
    fields = ['name','price', 'image']
    #form_class = forms.ProductForm
    # success_url = '/'
    login_url = 'login'
    

    def form_valid(self, form):
        form.instance.user =self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        product=self.get_object()
        if self.request.user == product.product_by:
            return True
        return False


def delete_product(request, id):
	product = get_object_or_404(Product, id=id)
	product.delete()
	return redirect('products_list')


