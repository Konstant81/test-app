from datetime import date
import base64
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DeleteView, UpdateView
from main.forms import AddOrderForm, EditdOrderForm
from main.models import Client, Order

# Create your views here.


def index(request):
    if d := request.GET.get("date"):
        year, week = map(int, d.split("-W"))
    else:
        year, week = date.today().year, date.today().isocalendar().week
    dates = sorted(
        [
            x.order_date
            for x in Order.objects.all()
            if x.order_date.isocalendar().week == week and x.order_date.year == year
        ]
    )
    cur_week = f"{year}-W{week}"
    sum_amount = (
        Order.objects.raw(
            '''SELECT "order"."id", "order"."order_date",
                        REPLACE(GROUP_CONCAT(DISTINCT "client"."fullname"), ',', '; ') AS clients,
                        SUM("order"."amount") AS "sum_amount"
                        FROM "order"
                        JOIN "client" ON "order"."client_id" = "client"."id" 
                        WHERE "order"."order_date" BETWEEN %s AND %s
                        GROUP BY "order"."order_date"''',
            [dates[0], dates[-1]],) if dates else False
    )
    week_total = (
        Order.objects.raw(
            '''SELECT "order"."id", "order"."order_date",
                        REPLACE(GROUP_CONCAT(DISTINCT "client"."fullname"), ',', '; ') AS clients,
                        SUM("order"."amount") AS sum_amount
                        FROM "order"
                        JOIN "client" ON "order"."client_id" = "client"."id" 
                        WHERE "order"."order_date" BETWEEN %s AND %s''',
            [dates[0], dates[-1]],) if dates else False
    )
    amount_total, client_week = week_total[0].sum_amount if week_total else None, week_total[0].clients if week_total else None

    context = {
        "title": "Главная страница",
        "content": "Главная страница приложения",
        "week_orders": sum_amount,
        "amount_total": amount_total,
        "client_week": client_week,
        "current_week": cur_week,
    }
    return render(request, "main/index.html", context)

@login_required
def order(request, client_pk=""):
    print(request.path == f'/orders/{client_pk}')
    if client_pk:
        orders = Order.objects.select_related("client").filter(client__id=client_pk)
    else:
        orders = Order.objects.select_related("client").all()
    clients = Client.objects.all()
    context = {
        "clients": clients,
        "orders": orders,
    }
    return render(request, "main/orders.html", context)


def get_json(request):
    auth_user = "user1:1234"
    auth_bytes = auth_user.encode("ascii")
    b64_bytes = base64.b64encode(auth_bytes)
    user_b64 = b64_bytes.decode("ascii")
    auth_template = f'Basic {user_b64}'
    if request.headers["Authorization"] == auth_template:
        data = serializers.serialize("json", Order.objects.all())
        return JsonResponse(data, safe=False)
    return HttpResponse('Unauthorized', status=401)


class AddOrder(CreateView):
    form_class = AddOrderForm
    template_name = "main/add_order.html"
    success_url = reverse_lazy("main:orders")
    extra_context = {
        "title": "Добавить",
        "content": "Добавить заказ",
        "button": "Добавить"
    }


class UpdateOrder(UpdateView):
    form_class = EditdOrderForm
    template_name = "main/add_order.html"
    success_url = reverse_lazy("main:orders")
    extra_context = {
        "title": "Редактировать",
        "content": "Редактировать заказ",
        "button": "Сохранить"
    }

    def get_queryset(self):
        return Order.objects.all()
    

class DeleteOrder(DeleteView):
    model = Order
    template_name = "main/delete.html"
    success_url = reverse_lazy("main:orders")
