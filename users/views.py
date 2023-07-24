from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import auth, messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from saved_sales.models import Saved_sales
from sales.models import Sale
from .models import User


def register(request, *args, **kwargs):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Teie konto - {username}, on edukalt loodud!')
            return redirect('sales-home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required 
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Andmed on edukalt uuendatud!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    current_user = request.user
    user_id = current_user.id
    results = Saved_sales.objects.filter(id_user = user_id)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'results': results,
        'sales': Sale.objects.all()
    }
    return render(request, 'users/profile.html', context)


def delete_offer(request, pk):
    saved_sale = Saved_sales.objects.get(id = pk)
    saved_sale.delete()
    
    messages.success(request, f'Valitud toode oli eemaldatud!')
    return HttpResponseRedirect("/")
    
