from django import forms
from store.models import Product, Category,SubCategory
from django.forms import ModelChoiceField

class ProductForm(forms.Form):
	name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'product name'}))
	price = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'price'}))
	image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control','placeholder':'image'}))

	class Meta:
		model = Product
		fields =['name', 'price', 'image']




class categoryForm(forms.Form):
	name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'category name'}))
	
	class Meta:
		model = Category
		fields =['name']


class subcategoryForm(forms.Form):
	name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'sub category name'}))
	category = forms.ModelChoiceField(
		queryset=Category.objects.all()
		,widget=forms.Select(attrs={'class':'form-control',}),empty_label="Select Category" )
	
	class Meta:
		model = SubCategory
		fields =['name', 'category']




class subsubcategoryForm(forms.Form):
	name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'sub sub category name'}))
	subcategory = forms.ModelChoiceField(
		queryset=SubCategory.objects.all()
		,widget=forms.Select(attrs={'class':'form-control',}),empty_label="Select sub category" )
	
	class Meta:
		model = SubCategory
		fields =['name', 'subcategory']

