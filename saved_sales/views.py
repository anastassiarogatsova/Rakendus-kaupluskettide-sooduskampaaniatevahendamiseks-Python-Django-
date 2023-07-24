from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import Saved_sales
from users.models import User
from sales.models import Sale
from django.contrib import auth, messages
from django.contrib.messages import get_messages

@csrf_exempt
def SendSaved(request):
    current_user = request.user
    if (current_user.id == None):
        user_id = 0
    else:
        user_id = current_user.id

    pk = request.POST.get('pk')
    print(pk, user_id)

    sale_object = Sale.objects.get(id = pk)
    num_results = Saved_sales.objects.filter(headline = sale_object.headline).count()
    if (num_results >= 1):
        messages.warning(request, f'Toode on juba lisatud')
        return redirect('http://127.0.0.1:8000/sale/'+pk+'/')
        
    else:
        sale_object = Sale.objects.get(id = pk)
        saved_sale = Saved_sales(
            id_sale = pk,
            store = sale_object.store,
            headline = sale_object.headline,
            id_user = user_id
        )

        saved_sale.save()
        messages.success(request, f'Toode on lisatud')
    
    return redirect('http://127.0.0.1:8000/sale/'+pk+'/')



def about(request):

    context = {
        'saved_sales' : Saved_sales.objects.all()
    }

    return render(request, 'saved_sales/sales.html', context)