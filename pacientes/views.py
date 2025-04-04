from django.shortcuts import render
from application.models import Paciente, Medico

def lista_pacientes(request):
    medico = Medico.objects.get(usuario=request.user)
    pacientes = Paciente.objects.filter(medico_responsavel=medico)
    return render(request, 'pacientes/lista.html', {'pacientes': pacientes})