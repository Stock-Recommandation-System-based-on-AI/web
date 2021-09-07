from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Stock



# Create your views here.
def main_page(request):
    return render(request, 'stock/main_page.html')


def forecasts(request):
    if request.user.is_authenticated:
        return render(request, 'stock/forecasts.html')
    else:
        return redirect('accounts:login')


def forecast_detail(request, stock_pk):
    stock = get_object_or_404(Stock, pk=stock_pk)
    context = {
        'stock': stock,
    }
    return render(request, 'stock/forecast_detail.html', context)


def interest(request, stock_pk):
    user = request.user
    stock = get_object_or_404(Stock, pk=stock_pk)
    if stock.interest_users.filter(pk=user.pk).exists():
        stock.interest_users.remove(user)
        interested = False
    else:
        stock.interest_users.add(user)
        interested = True
    context = {
        'count': stock.like_users.count(),
        'interested': interested,
    }
    return JsonResponse(context)
