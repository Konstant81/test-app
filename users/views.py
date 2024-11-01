from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from users.forms import LoginUserForm, RegisterUserForm


# Create your views here.
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/registration.html'
    extra_context = {"title": "Авторизация", "button": "Войти"}


class RegistrationUser(CreateView):
    form_class = RegisterUserForm
    template_name = "users/registration.html"
    extra_context = {"title": "Регистрация", "button": "Подтвердить"}
    success_url = reverse_lazy("users:login")

