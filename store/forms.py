from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class CheckoutForm(forms.Form):
    address1 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'address(Town)'
    }))
    address2 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'address2'
    }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'city'
    }))
    region = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Region'
    }))
    zipcode = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'zipCode'

    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'phone number'

    }))
    tin_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'TIN number'
    }))
    # added field
    description = forms.CharField(widget=forms.Textarea(attrs={

        'cols': 23,
        'rows': 1,
        'placeholder': 'Description'
    }))
    country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    pay_option = forms.CharField()


class EditProductForm(forms.Form):
    quantity = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'value': '3',
    }))
