from django.urls import path
from . import views

app_name = 'andares'

urlpatterns = [
    path('', views.controle_andares, name='controle_andares'),
    path('atribuir/', views.atribuir_quarto, name='atribuir_quarto'),
    path('liberar/<int:quarto_id>/', views.liberar_quarto, name='liberar_quarto'),
    path('adicionar-andares/', views.pagina_adicionar_andares, name='pagina_adicionar_andares'),
    path('add-andares/', views.pagina_adicionar_andares, name='add_andares'),
    path('criar-andar/', views.criar_andar, name='criar_andar'),
    path('criar-quartos/', views.criar_quartos, name='criar_quartos'),
    path('criar-automaticamente/', views.criar_automaticamente, name='criar_automaticamente'),
]