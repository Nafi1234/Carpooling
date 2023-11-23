from django.urls import path 

from .views import UserRegistrationView,OTPVerificationView,UserLoginView,UserDetailsView,Forgotpassword,Forgototpverification,Confirmpassword,UpdateUserDetailsView,CustomTokenRefreshView
urlpatterns = [
    path('register',  UserRegistrationView.as_view()),
    path('verify-otp',OTPVerificationView.as_view()),
    path('login',UserLoginView.as_view()),
    path('details',UserDetailsView.as_view()),
    path('forgotpassword',Forgotpassword.as_view()),
    path('forgototpverification',Forgototpverification.as_view()),
    path('confirmpassword',Confirmpassword.as_view()),
    path('update',UpdateUserDetailsView.as_view()),
    path('newtoken',CustomTokenRefreshView.as_view())
]
