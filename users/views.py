from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from users.forms import LoginUserForm, RegisterUserForm


# Create your views here.
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {"title": "Авторизация", "button": "Войти"}


class RegistrationUser(CreateView):
    form_class = RegisterUserForm
    template_name = "users/registration.html"
    extra_context = {"title": "Регистрация", "button": "Подтвердить"}
    success_url = reverse_lazy("users:login")


def registration(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return render(request, "users/registration_done.html")
    else:
        form = RegisterUserForm()
    context = {
        "title":"Регистрация",
        "button": "Подтвердить",
        "form": form,
    }
    return render(request, 'users/registration.html', context)

def profile(request):
    context = {
        "title":"Профиль пользователя"
    }
    return render(request, 'users/profile.html', context)
