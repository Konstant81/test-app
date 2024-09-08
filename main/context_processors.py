from main.forms import AddOrderForm

def edit_form_context(request):
    add_order_form = AddOrderForm()
    return {'add_order_form': add_order_form,}
