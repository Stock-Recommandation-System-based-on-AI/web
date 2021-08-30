from django.shortcuts import render

# Create your views here.
def main_page(request):
    return render(request, 'stock/main_page.html')


def forecasts(request):
    return render(request, 'stock/forecasts.html')