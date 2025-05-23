from django.urls import path
from . import views

app_name = 'pacientes'

urlpatterns = [
    path('', views.lista_pacientes, name='lista'),
    path('cadastrar/', views.cadastrar_paciente, name='cadastrar'),
    path('medico-pacientes/', views.medico_pacientes, name='medico_pacientes'),
    path('paciente/<int:paciente_id>/', views.visualizar_paciente, name='visualizar_paciente'),
    path('paciente/<int:paciente_id>/observacoes/adicionar/', views.adicionar_observacao, name='adicionar_observacao'),
    path('paciente/<int:paciente_id>/observacoes/', views.listar_observacoes, name='listar_observacoes'),
    path('prontuario/consultar/', views.consultar_prontuario_paciente, name='consultar_prontuario_paciente'),
    path('prontuario/visualizar/<str:cpf>/<str:data_nascimento_str>/', views.visualizar_prontuario_publico, name='visualizar_prontuario_publico'),
]