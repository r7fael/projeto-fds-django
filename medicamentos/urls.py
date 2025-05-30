from django.urls import path
from . import views

app_name = 'medicamentos'

urlpatterns = [
    path('', views.lista_medicamentos, name='lista'),
    path('adicionar/', views.adicionar_medicamento, name='adicionar'),
    path('editar/<int:pk>/', views.editar_medicamento, name='editar'),
    path('excluir/<int:pk>/', views.excluir_medicamento, name='excluir'),
]