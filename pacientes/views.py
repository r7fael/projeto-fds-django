from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import Medico, Enfermeiro
from application.models import Notificacao
from pacientes.models import Paciente
from django.contrib.auth.decorators import login_required

@login_required
def cadastrar_paciente(request):
    enfermeiro = Enfermeiro.objects.get(usuario=request.user)

    if request.method == 'POST':
        nome_completo = request.POST.get('nome_completo')
        cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')
        medico_id = request.POST.get('medico_responsavel')

        if nome_completo and cpf and data_nascimento and medico_id:
            medico = Medico.objects.get(id=medico_id)
            Paciente.objects.create(
                nome_completo=nome_completo,
                cpf=cpf,
                data_nascimento=data_nascimento,
                medico_responsavel=medico
            )
            messages.success(request, 'Paciente cadastrado com sucesso!')
            return redirect('pacientes:cadastrar')
        else:
            messages.error(request, 'Por favor, preencha todos os campos corretamente.')

    medicos = Medico.objects.all()

    return render(request, 'application/cadastrar_paciente.html', {
        'enfermeiro': enfermeiro,
        'medicos': medicos,
        'notificacoes': Notificacao.objects.filter(lida=False).order_by('-data_criacao')[:5],
    })

@login_required
def lista_pacientes(request):
    medico = Medico.objects.get(usuario=request.user)
    pacientes = Paciente.objects.filter(medico_responsavel=medico)
    return render(request, 'pacientes/lista.html', {'pacientes': pacientes})

def medico_pacientes(request):
    medico = Medico.objects.get(usuario=request.user)
    pacientes = Paciente.objects.filter(medico_responsavel=medico)
    return render(request, 'application/medico_pacientes.html', {'pacientes': pacientes})