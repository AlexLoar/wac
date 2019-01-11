from django.urls import path

from . import views

app_name = 'users_v1'

urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('users', views.CustomUserList.as_view(), name='list'),
    path('users/<int:pk>', views.CustomUserDetail.as_view(), name='detail')
]
