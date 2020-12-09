from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView

from authentication.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from authentication.forms import UserSignUpForm, SinInForm, loginForm
# Create your views here.
from django.views.generic.base import View


class UserSignUp(View):
    def get(self, *args, **kwargs):

        context = {}
        form = UserSignUpForm(self.request.POST or None)
        context['form'] = form
        return render(self.request, 'authentication/sign_up.html', context)

    def post(self, request, *args, **kwargs):
        form = UserSignUpForm(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            password2 = form.cleaned_data.get('password2')
            mobile = form.cleaned_data.get('mobile')

            # cheking for passwords matching
            if password != password2:
                messages.warning(self.request, "password doesn't match")
                return redirect('sign_up')

            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):

                User.objects.create_user(email, password, mobile=mobile, username=username, is_active=True)
                # it going to be used later in the email sending
                user = User.objects.get(username=username, email=email)
                # TODO send email address to activate a user if you want it to
                messages.warning(self.request, f'Login now')
                return redirect('sign_in')
            else:
                messages.warning(self.request, 'Looks like a username with that email or password already exists')
                return redirect("sign_up")
        else:
            print('from not valid')
            messages.warning(self.request, 'Form not valid')
        return redirect('sign_up')


class UserSignIn(View):
    def get(self, request, *args, **kwargs):
        form = SinInForm()
        context = {
            'form': form
        }
        return render(request, template_name='authentication/sign_in.html', context=context)

    def post(self, request, *args, **kwargs):
        if self.request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')
            remember_me = request.POST.get('remember_me')

            user_auth = authenticate(email=email, password=password)
    
            if user_auth:
                # we need to check if the auth_user is activate to our system
                if user_auth.is_active:
                    # if not request.POST.get('remember_me', None):
                    # make the session to end in one mouth
                    login(request, user_auth)
                    messages.info(self.request, 'welcome home ')
                    return redirect('/')

                else:
                    messages.info(self.request, 'Your account was inactive.Try to activate your account now')
                    return redirect('sign_in')
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(email, password))
                messages.warning(self.request, 'Invalid login details given,')
                return redirect("sign_in")


def user_sign_out(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    messages.warning(request, 'Your signed Out, Login again')
    return redirect('sign_in')


def staff_login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                messages.success(request, 'succesfull Logged in')
                return redirect('/products')
            else:
                messages.error(request, "Ivalid Username/Password Or You're not Staff")
                return redirect('login')
    form = loginForm()
    context = {
        'form': form
    }
    return render(request, 'staff/login.html', context)


def staff_logout(request, ):
    logout(request)
    messages.info(request, 'Your signed Out, Login again')
    return redirect('login')

# ========================================== for reference purpose===========================================#

# def login(request):
#     next = request.POST.get('next', request.GET.get('next', ''))
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = auth.authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 if next:
#                     return HttpResponseRedirect(next)
#                 return HttpResponseRedirect('/home')
#             else:
#                 return HttpResponse('Inactive user')
#         else:
#             return HttpResponseRedirect(settings.LOGIN_URL)
#     return render(request, "login.html")

# ===========================================dont delete these codes are important================================#
