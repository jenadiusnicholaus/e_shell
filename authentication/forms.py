from django import forms


class UserSignUpForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    mobile = forms.IntegerField()
    password = forms.CharField(widget=forms.PasswordInput())


class SinInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
