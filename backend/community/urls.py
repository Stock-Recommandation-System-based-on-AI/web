from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.post_list, name="post_list"),
    path('post_create/', views.post_create, name='post_create'),
    path('<int:post_pk>/', views.post_detail, name='post_detail'),
    path('<int:post_pk>/post_update/', views.post_update, name='post_update'),
    path('<int:post_pk>/post_delete/', views.post_delete, name='post_delete'),
]