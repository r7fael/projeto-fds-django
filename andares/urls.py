from django.urls import path
from . import views

app_name = 'andares'

urlpatterns = [
    path('', views.controle_andares, name='controle_andares'),
    path('atribuir/', views.atribuir_quarto, name='atribuir_quarto'),
    path('liberar/<int:quarto_id>/', views.liberar_quarto, name='liberar_quarto'),
]