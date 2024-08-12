from django.shortcuts import render

# Create your views here.

def index(request):
    context = {
        "title": "Главная страница",
        "content": "Главная страница приложения"
    }
    return render(request, "main/index.html", context)

def edit(request):
    context = {
        "title": "Редактирование",
        "content": "Страница редактирования БД"
    }
    return render(request, "main/index.html", context)

def send(request):
    context = {
        "title": "Отправка",
        "content": "Страница отправки JSON"
    }
    return render(request, "main/index.html", context)
