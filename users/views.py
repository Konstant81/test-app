from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login

from users.forms import LoginUserForm


# Create your views here.
def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = LoginUserForm()
    return render(request, 'users/login.html', {'form': form})
 
def registration(request):
    context = {
        "title":"Регистрация"
    }
    return render(request, 'users/registration.html', context)

def profile(request):
    context = {
        "title":"Профиль пользователя"
    }
    return render(request, 'users/profile.html', context)

def logout(request):
    context = {
        "title":"Выход"
    }
    return render(request, 'users/logout.html', context)
