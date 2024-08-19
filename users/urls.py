from django.urls import path
from . import views
 

app_name = "users"

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
]
