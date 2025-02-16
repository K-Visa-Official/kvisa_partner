from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),

    path('user/', views.get_user_info, name='get_user_info'),  #
]