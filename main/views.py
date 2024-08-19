from datetime import date
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from main.forms import AddOrderForm, EditdOrderForm
from main.models import Order

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

    context = {
        "title": "Главная страница",
        "content": "Главная страница приложения",
        "week_orders": sum_amount,
        "current_week": cur_week,
    }
    return render(request, "main/index.html", context)


def order(request):
    orders = Order.objects.select_related("client").all()
    context = {
        "title": "Редактирование",
        "content": "Страница редактирования БД",
        "orders": orders,
    }
    return render(request, "main/orders.html", context)


def send(request):
    context = {
        "title": "Отправка",
        "content": "Страница отправки JSON",
    }
    data = serializers.serialize("json", Order.objects.all())
    return JsonResponse(data, safe=False)
    # return render(request, "main/send.html", context)


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


# def add_order(request):
#     if request.method == 'POST':
#         form = AddOrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('main:orders')
#     else:
#         form = AddOrderForm()
#     context = {
#         "title": "Добавить",
#         "content": "Добавить заказ",
#         "form": form
#     }
#     return render(request, "main/add_order.html", context)

# def edit_order(request, order_id):
#     order = Order.objects.get(pk=order_id)
#     if request.method == 'POST':
#         form = AddOrderForm(request.POST)
#         if form.is_valid():
#             try:
#                 return redirect('main:orders')
#             except:
#                 form.add_error(None, "Ошибка добавления заказа")
#     else:
#         form = AddOrderForm(order)
#     context = {
#         "title": "Редактировать",
#         "content": "Редактировать заказ",
#         "form": form
#     }
#     return render(request, "main/edit_order.html", context)
