from django.urls import path
from . import views
from pacientes.views import cadastrar_paciente

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('painel-medico/', views.painel_medico, name='painel_medico'),
    path('painel-enfermeiro/', views.painel_enfermeiro, name='painel_enfermeiro'),
    path('cadastrar-paciente/', cadastrar_paciente, name='cadastrar_paciente'),
]