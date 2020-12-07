from django import forms


class UserSignUpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter your username'
        }
    ))
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                'placeholder':'Enter your Email'
            }
        )
    )
    mobile = forms.CharField(widget=forms.NumberInput(
        attrs={
            'placeholder': 'Enter your phone number'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': ' Enter password'
    }))
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Confirm password'
        }
    ))


class SinInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class loginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Email')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password')
