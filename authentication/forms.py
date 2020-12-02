from django import forms
from django.contrib.auth.forms import AuthenticationForm

class UserSignUpForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    mobile = forms.IntegerField()
    password = forms.CharField(widget=forms.PasswordInput())


class SinInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())




class loginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}), label='Email')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label='Password')

