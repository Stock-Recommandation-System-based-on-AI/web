from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.community_list, name="community_list"),
    path('review_create/', views.post_create, name='review_create'),
    path('<int:review_pk>/', views.post_detail, name='review_detail'),
    path('<int:review_pk>/review_update/', views.post_update, name='review_update'),
    path('<int:review_pk>/review_delete/', views.post_delete, name='review_delete'),
]