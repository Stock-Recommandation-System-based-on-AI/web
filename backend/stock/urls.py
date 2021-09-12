from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [
    path('', views.main_page, name="main_page"),
    path('forecasts/', views.forecasts, name="forecasts"),
    path('forecasts/<str:stock_pk>/', views.forecast_detail, name="forecast_detail"),
    path('<str:stock_pk>/interest/', views.interest, name='interest'),
]
