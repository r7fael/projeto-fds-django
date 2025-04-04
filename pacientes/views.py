from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import Medico, Enfermeiro
from application.models import Notificacao
from pacientes.models import Paciente
from .forms import PacienteForm
from django.contrib.auth.decorators import login_required

def lista_pacientes(request):
    medico = Medico.objects.get(usuario=request.user)
    pacientes = Paciente.objects.filter(medico_responsavel=medico)
    return render(request, 'pacientes/lista.html', {'pacientes': pacientes})

@login_required
def cadastrar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente cadastrado com sucesso!')
            return redirect('pacientes:cadastrar')
    else:
        form = PacienteForm()

    enfermeiro = Enfermeiro.objects.get(usuario=request.user)

    return render(request, 'application/cadastrar_paciente.html', {
        'form': form,
        'enfermeiro': enfermeiro,
        'notificacoes': Notificacao.objects.filter(lida=False).order_by('-data_criacao')[:5],
    })

def medico_pacientes(request):
    return render(request, 'application/medico_pacientes.html')