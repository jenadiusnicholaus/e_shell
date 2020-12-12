
from django.shortcuts import render,get_object_or_404, redirect
from store.models import Product,Category,SubCategory,SubSubCategory
from django.views.generic import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import *
from django.db.models import Q


#===========================================prduct start here=======================================#

# @login_required(login_url='/login')
# def staff_index(request):
#     return render(request, 'staff/index.html')

@login_required(login_url='/login')
def products_list(request):
    qs = request.GET.get('q')
    if qs:
        products = Product.objects.filter(
        # Q(user__username=query)|
        Q(name__icontains=qs)|
        Q(price__icontains=qs)
        )
    products = Product.objects.filter(author=request.user)
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
        form = ProductForm(request.POST , request.FILES)
        product = Product()
        if form.is_valid():
            # product.sub_category = 'ENGINE OIL DIESEL'
            product.name = form.cleaned_data['name']
            product.price = form.cleaned_data['price']
            product.image = form.cleaned_data['image']
            product.author = request.user
            product.save()
            print(request)
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

#===========================================product end here==================================#






#===========================================product-category start here==========================#
def product_category(request):
    category = Category.objects.filter(author=request.user)
    context = {
        'category': category
    }
    return render(request, 'staff/product-category.html', context)
 
def add_category(request):
    if request.method == 'POST':
        form = categoryForm(request.POST or None)
        category = Category()
        if form.is_valid():
            category.name = form.cleaned_data.get('name')
            category.author = request.user
            category.save()
            return redirect('Product_category')
    form = categoryForm()
    context ={
     'form':form
    }
    return render(request, 'staff/add-category.html', context)



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

#===========================================product-category ends here==========================#







#===========================================product-sub-category start here==========================#

def product_sub_category(request):
    sub_category = SubCategory.objects.filter(author=request.user)
    context = {
        'sub_category': sub_category
    }
    return render(request, 'staff/product-sub-category.html', context)

def add_sub_category(request):
    if request.method == 'POST':
        form = subcategoryForm(request.POST or None)
        sub = SubCategory()
        if form.is_valid():
            sub.name = form.cleaned_data.get('name')
            sub.category = form.cleaned_data.get('category')
            sub.author = request.user
            sub.save()
            return redirect('Product_sub_category')
    form = subcategoryForm()
    context ={
     'form':form
    }
    return render(request, 'staff/add-subcategory.html', context)


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
    product = get_object_or_404(SubCategory, id=id)
    product.delete()
    return redirect('Product_sub_category')


#===========================================product-sub-category ends here==========================#






#===========================================product-sub-sub-category start here==========================#

def Product_sub_sub_category(request):
    sub_sub_category = SubSubCategory.objects.filter(author=request.user)
    context = {
     'sub_sub_category':sub_sub_category
    }
    return render(request, 'staff/product-sub-sub-category.html',context)

def add_sub_sub_category(request):
    if request.method == 'POST':
        form = subsubcategoryForm(request.POST or None)
        sub_sub = SubSubCategory()
        if form.is_valid():
            sub_sub.name = form.cleaned_data.get('name')
            sub_sub.subcategory = form.cleaned_data.get('subcategory')
            sub_sub.author = request.user
            sub_sub.save()
            return redirect('Product_sub_sub_category')
    form = subsubcategoryForm()
    context ={
     'form':form
    }
    return render(request, 'staff/add-subsubcategory.html', context)

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
    product = get_object_or_404(SubSubCategory, id=id)
    product.delete()
    return redirect('Product_sub_sub_category')

#===========================================product-sub-sub-category start here==========================#
