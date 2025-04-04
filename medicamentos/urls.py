from django.urls import path
from . import views

app_name = 'medicamentos'

urlpatterns = [
    path('', views.lista_medicamentos, name='lista'),
]