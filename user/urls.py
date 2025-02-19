from django.urls import path
from . import views

urlpatterns = [
    #################### 회원 ####################
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('user/', views.get_user_info, name='get_user_info'), 
    path('user/edit', views.get_user_edit, name='get_user_edit'),


    #################### 어드민 ####################
    path('user/all', views.get_all_users, name='get_all_users'),
    path('user/<int:pk>/', views.get_user_pk, name='get_user_pk'), 
]