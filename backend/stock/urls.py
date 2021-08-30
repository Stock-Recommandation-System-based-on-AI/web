from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [
    path('', views.main_page, name="main_page"),
    path('forecasts/', views.forecasts, name="forecasts"),
]
