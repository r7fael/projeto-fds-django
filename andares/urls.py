from django.urls import path
from . import views

app_name = 'andares'

urlpatterns = [
    path('', views.painel_andares, name='painel_andares'),
    path('liberar-quarto/<int:quarto_id>/', views.liberar_quarto, name='liberar_quarto'),
]