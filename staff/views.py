
from django.shortcuts import render,get_object_or_404, redirect
from store.models import Product,Category,SubCategory,SubSubCategory
from django.views.generic import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import ProductForm


@login_required(login_url='/login')
def staff_index(request):
    return render(request, 'staff/index.html')


@login_required(login_url='/login')
def products_list(request):
    products = Product.objects.all()
    context = {
        'products': products
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
            # product.sub_category = 'ENGINE OIL DIESEL'
            product.name = request.POST.get('name')
            product.price = request.POST.get('price')
            product.image = request.FILE.get('image')
            product.author = request.user
            product.save()
            print(product)
            return redirect('products_list')
        else:
            messages.error(request, 'Post error')
            return redirect('add_product')
    form = ProductForm()
    context = {
        'form': form
    }
    return render(request, 'staff/product-add.html', context)


class ProductUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'staff/product-edit.html'
    fields = ['name', 'price', 'image']
    # form_class = forms.ProductForm
    # success_url = '/'
    login_url = 'login'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.author:
            return True
        return False


def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('products_list')


def product_category(request):
    category = Category.objects.all()
    context = {
        'category': category
    }
    return render(request, 'staff/product-category.html', context)


class CategoryUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Category
    template_name = 'staff/category-edit.html'
    fields = ['name']
    # form_class = forms.ProductForm
    # success_url = '/'
    login_url = 'login'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        category = self.get_object()
        if self.request.user == category.author:
            return True
        return False


def delete_category(request, id):
    product = get_object_or_404(Category, id=id)
    product.delete()
    return redirect('Product_category')


def product_sub_category(request):
    sub_category = SubCategory.objects.all()
    context = {
        'sub_category': sub_category
    }
    return render(request, 'staff/product-sub-category.html', context)


class SubCategoryUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = SubCategory
    template_name = 'staff/sub-category-edit.html'
    fields = ['name']
    # form_class = forms.ProductForm
    # success_url = '/'
    login_url = 'login'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        sub_category = self.get_object()
        if self.request.user == sub_category.author:
            return True
        return False


def delete_sub_category(request, id):
	product = get_object_or_404(Category, id=id)
	product.delete()
	return redirect('Product_sub_category')




def Product_sub_sub_category(request):
	sub_sub_category = SubSubCategory.objects.all()
	context = {
	 'sub_sub_category':sub_sub_category
	}
	return render(request, 'staff/product-sub-sub-category.html',context)


class SubSubCategoryUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = SubSubCategory
    template_name = 'staff/sub-sub-category-edit.html'
    fields = ['name']
    #form_class = forms.ProductForm
    # success_url = '/'
    login_url = 'login'
    

    def form_valid(self, form):
        form.instance.user =self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        sub_sub_category=self.get_object()
        if self.request.user == sub_sub_category.author:
            return True
        return False


def delete_sub_sub_category(request, id):
	product = get_object_or_404(Category, id=id)
	product.delete()
	return redirect('Product_sub_sub_category')
