from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView

from users.forms import LoginUserForm, RegisterUserForm


# Create your views here.
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {"title": "Авторизация", "button": "Войти"}

    # def get_success_url(self):
    #     return reverse_lazy('main:index')

# def login_user(request):
#     if request.method == 'POST':
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user and user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('main:index'))
#     else:
#         form = LoginUserForm()
#     return render(request, 'users/login.html', {'form': form})

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

# def logout_user(request):
#     context = {
#         "title":"Выход"
#     }
#     logout(request)
#     return HttpResponseRedirect(reverse('users:login'))
