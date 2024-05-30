from django.urls import path
from .views import (
 UserRegister, UserLogin,
   UserLogout, UserView, OTPVerificationView)

urlpatterns = [
     path('register/', UserRegister.as_view(), name='register' ),
     path('login/', UserLogin.as_view(), name='login'),
     path('logout/', UserLogout.as_view(), name='logout'),
     path('user/', UserView.as_view(), name='user'),
     path('verify-otp/', OTPVerificationView.as_view(), name='verify-otp') ,

]
