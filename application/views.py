from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import Medico, Enfermeiro
from application.models import Consulta, Notificacao
from pacientes.forms import PacienteForm
from pacientes.models import Paciente

def home(request):
    return render(request, 'application/home.html')

def cadastro(request):
    return render(request, 'application/cadastro.html')

@login_required
def painel_medico(request):
    try:
        medico = Medico.objects.get(usuario=request.user)

        consultas = Consulta.objects.filter(medico=medico).order_by('data')[:5]
        pacientes = Paciente.objects.filter(medico_responsavel=medico)
        notificacoes = Notificacao.objects.filter(medico=medico, lida=False).order_by('-data_criacao')[:5]

        context = {
            'medico': medico,
            'consultas': consultas,
            'pacientes': pacientes,
            'notificacoes': notificacoes,
        }

        return render(request, 'application/painel_medico.html', context)

    except Medico.DoesNotExist:
        return render(request, 'application/nao_autorizado.html')

@login_required
def painel_enfermeiro(request):
    try:
        enfermeiro = Enfermeiro.objects.get(usuario=request.user)

        if request.method == 'POST':
            form = PacienteForm(request.POST)
            if form.is_valid():
                paciente = form.save(commit=False)
                paciente.save()
                return redirect('application:painel_enfermeiro')
        else:
            form = PacienteForm()

        context = {
            'enfermeiro': enfermeiro,
            'form': form
        }

        return render(request, 'application/painel_enfermeiro.html', context)

    except Enfermeiro.DoesNotExist:
        return render(request, 'application/nao_autorizado.html')
