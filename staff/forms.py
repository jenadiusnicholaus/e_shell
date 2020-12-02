from django import forms
from store.models import Product

class ProductForm(forms.Form):
	name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	price = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control'}))
	image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}))

	class Meta:
		model = Product
		fields =['name', 'price', 'image']

