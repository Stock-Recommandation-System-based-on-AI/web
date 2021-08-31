from django.shortcuts import render, redirect

# Create your views here.
def main_page(request):
    return render(request, 'stock/main_page.html')


def forecasts(request):
    if request.user.is_authenticated:
        return render(request, 'stock/forecasts.html')
    else:
        return redirect('accounts:login')