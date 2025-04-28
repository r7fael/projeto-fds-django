from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from users.models import Medico, Enfermeiro
from notificacoes.models import Notificacao
from pacientes.models import Paciente, ObservacaoSaude
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils import timezone

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
        
        if request.method == 'POST':
            if request.POST.get('form_type') == 'medicamentos':
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
            
            elif request.POST.get('form_type') == 'observacao':
                paciente_id = request.POST.get('paciente_id')
                tipo = request.POST.get('tipo')
                observacao_texto = request.POST.get('observacao', '').strip()
                
                if paciente_id and tipo and observacao_texto:
                    try:
                        paciente = Paciente.objects.get(id=paciente_id, medico_responsavel=medico)
                        ObservacaoSaude.objects.create(
                            paciente=paciente,
                            autor=medico,
                            tipo=tipo,
                            observacao=observacao_texto,
                            data_criacao=timezone.now()
                        )
                        messages.success(request, 'Observação adicionada com sucesso!')
                        return redirect('application:medico_pacientes')
                    
                    except Paciente.DoesNotExist:
                        messages.error(request, 'Paciente não encontrado ou não pertence ao seu cadastro!')
                    except Exception as e:
                        messages.error(request, 'Erro ao adicionar observação')
        
        return render(request, 'application/painel_medico.html', {
            'pacientes': pacientes,
            'medico': medico,
            'tipos_observacao': ObservacaoSaude.TIPO_CHOICES
        })
    
    except Medico.DoesNotExist:
        raise PermissionDenied("Acesso restrito a médicos cadastrados")

@login_required
def adicionar_observacao(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if hasattr(request.user, 'medico'):
        if paciente.medico_responsavel != request.user.medico:
            raise PermissionDenied("Você não tem permissão para adicionar observações a este paciente")
    elif not hasattr(request.user, 'enfermeiro'):
        raise PermissionDenied("Acesso restrito a profissionais de saúde")
    
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        observacao_texto = request.POST.get('observacao', '').strip()
        
        if tipo and observacao_texto:
            autor = None
            if hasattr(request.user, 'medico'):
                autor = request.user.medico
            
            ObservacaoSaude.objects.create(
                paciente=paciente,
                autor=autor,
                tipo=tipo,
                observacao=observacao_texto,
                data_criacao=timezone.now()
            )
            messages.success(request, 'Observação adicionada com sucesso!')
            return redirect('application:visualizar_paciente', paciente_id=paciente.id)
        else:
            messages.error(request, 'Por favor, preencha todos os campos corretamente.')
    
    return render(request, 'application/adicionar_observacao.html', {
        'paciente': paciente,
        'tipos_observacao': ObservacaoSaude.TIPO_CHOICES
    })

@login_required
def listar_observacoes(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if hasattr(request.user, 'medico'):
        if paciente.medico_responsavel != request.user.medico:
            raise PermissionDenied("Você não tem permissão para ver observações deste paciente")
    elif not hasattr(request.user, 'enfermeiro'):
        raise PermissionDenied("Acesso restrito a profissionais de saúde")
    
    observacoes = ObservacaoSaude.objects.filter(paciente=paciente).order_by('-data_criacao')
    
    return render(request, 'application/listar_observacoes.html', {
        'paciente': paciente,
        'observacoes': observacoes
    })

@login_required
def visualizar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if hasattr(request.user, 'medico'):
        if paciente.medico_responsavel != request.user.medico:
            raise PermissionDenied("Você não tem permissão para ver este paciente")
    elif not hasattr(request.user, 'enfermeiro'):
        raise PermissionDenied("Acesso restrito a profissionais de saúde")
    
    observacoes = paciente.observacoes.all().order_by('-data_criacao')[:5]
    
    return render(request, 'application/visualizar_paciente.html', {
        'paciente': paciente,
        'observacoes': observacoes,
        'tipos_observacao': ObservacaoSaude.TIPO_CHOICES
    })

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import RegistroAndarForm
from .models import RegistroPacienteAndar

@login_required
def registrar_andar(request):
    if not request.user.groups.filter(name='Enfermeiros').exists():
        return HttpResponseForbidden("Acesso restrito aos enfermeiros.")

    if request.method == 'POST':
        form = RegistroAndarForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.registrado_por = request.user
            registro.save()
            return redirect('visualizar_registros')
    else:
        form = RegistroAndarForm()

    return render(request, 'registro_andar.html', {'form': form})


@login_required
def visualizar_registros(request):
    if not request.user.groups.filter(name='Medicos').exists():
        return HttpResponseForbidden("Acesso restrito aos médicos.")

    registros = RegistroPacienteAndar.objects.all()
    return render(request, 'visualizar_registros.html', {'registros': registros})
