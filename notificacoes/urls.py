from django.urls import path
from . import views


app_name = 'notificacoes'

urlpatterns = [
    path('', views.lista_lembretes, name='lista_lembretes'),
    path('adicionar/', views.adicionar_lembrete, name='adicionar_lembrete'),
    path('concluir/<int:lembrete_id>/', views.marcar_concluido, name='marcar_concluido'),
    path('paciente/adicionar/', views.adicionar_paciente, name='adicionar_paciente'),
]