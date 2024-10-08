from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = "users"

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('registration/', views.RegistrationUser.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
