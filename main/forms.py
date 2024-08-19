from django import forms
from .models import Client, Order


class AddOrderForm(forms.ModelForm):
    client = forms.ModelChoiceField(label="Заказчик", empty_label="Выберите заказчика", queryset=Client.objects.all(), required=True)
    # order_date = forms.DateField(label="Дата заказа", widget=forms.widgets.DateInput(attrs={'type':'date'}), required=True)
    amount = forms.IntegerField(label="Сумма заказа", min_value=1, required=True)

    class Meta:
        model = Order
        fields = ['client', 'order_date', 'amount']
        widgets = {
            'order_date': forms.DateInput(attrs={'type':'date'})
        }

class EditdOrderForm(forms.ModelForm):
    # client = forms.ModelChoiceField(label="Заказчик", queryset=Order.objects.get(pk=id), empty_label="Выберите заказчика", required=True)
    # order_date = forms.DateField(label="Дата заказа", widget=forms.widgets.DateInput(attrs={'type':'date'}), required=True)
    amount = forms.IntegerField(label="Сумма заказа", min_value=1, required=True)

    class Meta:
        model = Order
        fields = ['client', 'order_date', 'amount']
        widgets = {
            'order_date': forms.DateInput(format='%Y-%m-%d', attrs={'type':'date'})
        }
