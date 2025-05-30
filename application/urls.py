from django.urls import path
from . import views
from pacientes.views import cadastrar_paciente, medico_pacientes

app_name = 'application'

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('painel-medico/', views.painel_medico, name='painel_medico'),
    path('painel-enfermeiro/', views.painel_enfermeiro, name='painel_enfermeiro'),
    path('painel-farmaceutico/', views.painel_farmaceutico, name='painel_farmaceutico'),
    path('cadastrar-paciente/', cadastrar_paciente, name='cadastrar_paciente'),
    path('medico-pacientes/', medico_pacientes, name='medico_pacientes'),
]