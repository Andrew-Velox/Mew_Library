from django.urls import path
from .views import UserRegistrationView,ProfileView,User_logout,UserLoginView,AccountPassChangeView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/', ProfileView, name='profile'),
    path('logout/', User_logout, name='logout'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('pass_change/', AccountPassChangeView.as_view(), name='pass_change'),
]
