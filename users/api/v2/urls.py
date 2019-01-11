from django.urls import path

from . import views

app_name = 'users_v2'

urlpatterns = [
    path('example', views.Example.as_view(), name='api_v2_example'),
]
