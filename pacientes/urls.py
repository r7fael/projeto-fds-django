from django.urls import path
from . import views

app_name = 'pacientes'

urlpatterns = [
    path('', views.lista_pacientes, name='lista'),
    path('cadastrar/', views.cadastrar_paciente, name='cadastrar'),
    path('medico-pacientes/', views.medico_pacientes, name='medico_pacientes'),
]