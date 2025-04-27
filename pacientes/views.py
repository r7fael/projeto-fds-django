from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import Medico, Enfermeiro
from notificacoes.models import Notificacao
from pacientes.models import Paciente
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

@login_required
def cadastrar_paciente(request):
    enfermeiro = Enfermeiro.objects.get(usuario=request.user)

    if request.method == 'POST':
        print(request.POST)
        nome_completo = request.POST.get('nome_completo')
        cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')
        medico_id = request.POST.get('medico_responsavel')
        medicamentos = request.POST.get('medicamentos', '')

        if nome_completo and cpf and data_nascimento and medico_id:
            medico = Medico.objects.get(id=medico_id)
            Paciente.objects.create(
                nome_completo=nome_completo,
                cpf=cpf,
                data_nascimento=data_nascimento,
                medico_responsavel=medico,
                medicamentos=medicamentos
            )
            messages.success(request, 'Paciente cadastrado com sucesso!')
            return redirect('application:painel_enfermeiro')
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

@login_required
def medico_pacientes(request):
    try:
        medico = Medico.objects.select_related('usuario').get(usuario=request.user)
        pacientes = Paciente.objects.filter(medico_responsavel=medico)\
                                  .select_related('medico_responsavel__usuario')
        
        if request.method == 'POST' and request.POST.get('form_type') == 'medicamentos':
            paciente_id = request.POST.get('paciente_id')
            medicamentos = request.POST.get('medicamentos', '').strip()
            
            if paciente_id:
                try:
                    paciente = Paciente.objects.get(id=paciente_id, medico_responsavel=medico)
                    if paciente.medicamentos != medicamentos:
                        paciente.medicamentos = medicamentos
                        paciente.save(update_fields=['medicamentos'])
                        messages.success(request, 'Medicamentos atualizados com sucesso!')
                    return redirect('application:medico_pacientes')
                
                except Paciente.DoesNotExist:
                    messages.error(request, 'Paciente não encontrado ou não pertence ao seu cadastro!')
                except Exception as e:
                    messages.error(request, 'Erro ao atualizar os medicamentos')
        
        return render(request, 'application/painel_medico.html', {
            'pacientes': pacientes,
            'medico': medico
        })
    
    except Medico.DoesNotExist:
        raise PermissionDenied("Acesso restrito a médicos cadastrados")