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
]

urlpatterns = [
    path('registrar-andar/', views.registrar_andar, name='registrar_andar'),
    path('visualizar-registros/', views.visualizar_registros, name='visualizar_registros'),
]