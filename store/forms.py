from django import forms


class CheckoutForm(forms.Form):
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'address(Town)'
    }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'city'

    }))
    state = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'state'
    }))
    zipcode = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'zipCode'

    }))
    # added field
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'cols': 23,
        'rows': 2,
        'placeholder': 'Description'
    }))


class EditProductForm(forms.Form):
    quantity = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'value':'3',
    }))
