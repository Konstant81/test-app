from datetime import date
from django.shortcuts import render
from main.models import Order

# Create your views here.

def index(request):
    if d := request.GET.get('date'):
        year, week = map(int, d.split('-W'))
    else:
        year, week = date.today().year, date.today().isocalendar().week
    dates = sorted([x.order_date for x in Order.objects.all() if
             x.order_date.isocalendar().week == week and x.order_date.year == year])
    cur_week = f"{year}-W{week}"
    sum_amount = Order.objects.raw(
            '''SELECT "order"."id", "order"."order_date",
                        GROUP_CONCAT("client"."fullname", ";") AS clients,
                        SUM("order"."amount") AS "sum_amount"
                        FROM "order"
                        JOIN "client" ON "order"."client_id" = "client"."id" 
                        WHERE "order"."order_date" BETWEEN %s AND %s
                        GROUP BY "order"."order_date"''', [dates[0], dates[-1]]) if dates else False

    context = {
        "title": "Главная страница",
        "content": "Главная страница приложения",
        "week_orders": sum_amount,
        "current_week": cur_week,
    }
    return render(request, "main/index.html", context)

def edit(request):
    context = {
        "title": "Редактирование",
        "content": "Страница редактирования БД"
    }
    return render(request, "main/base.html", context)

def send(request):
    context = {
        "title": "Отправка",
        "content": "Страница отправки JSON"
    }
    return render(request, "main/base.html", context)
