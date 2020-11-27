from django.urls import path
from . import views

urlpatterns = [
    path('sign_up/', views.UserSignUp.as_view(), name='sign_up'),
    path('sign_in/', views.UserSignIn.as_view(), name='sign_in'),
    path('sign_out/', views.user_sign_out, name='sign_out')
]
