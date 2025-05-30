from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from users.models import Medico, Enfermeiro
from notificacoes.models import Notificacao
from pacientes.models import Paciente, ObservacaoSaude
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from datetime import datetime

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
                            autor_medico=medico,
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
    
    usuario_eh_medico = hasattr(request.user, 'medico') and request.user.medico is not None
    usuario_eh_enfermeiro = hasattr(request.user, 'enfermeiro') and request.user.enfermeiro is not None

    if usuario_eh_medico:
        medico_atual = request.user.medico
        if paciente.medico_responsavel != medico_atual:
            raise PermissionDenied("Você não tem permissão para adicionar observações a este paciente, pois não é o médico responsável.")
    elif not usuario_eh_enfermeiro:
        raise PermissionDenied("Acesso restrito a médicos e enfermeiros cadastrados.")

    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        observacao_texto = request.POST.get('observacao', '').strip()
        
        if tipo and observacao_texto:
            dados_para_criar_observacao = {
                'paciente': paciente,
                'tipo': tipo,
                'observacao': observacao_texto,
                'data_criacao': timezone.now()
            }
            
            if usuario_eh_medico:
                dados_para_criar_observacao['autor_medico'] = request.user.medico
            elif usuario_eh_enfermeiro:
                dados_para_criar_observacao['autor_enfermeiro'] = request.user.enfermeiro
            
            ObservacaoSaude.objects.create(**dados_para_criar_observacao)
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
    
def consultar_prontuario_paciente(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf', '').strip()
        data_nascimento_str = request.POST.get('data_nascimento', '').strip()

        if not cpf or not data_nascimento_str:
            messages.error(request, 'Por favor, preencha o CPF e a Data de Nascimento.')
            return render(request, 'application/consultar_prontuario_form.html')

        try:
            data_nascimento_obj = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Formato de Data de Nascimento inválido. Use AAAA-MM-DD.')
            return render(request, 'application/consultar_prontuario_form.html')

        try:
            paciente = Paciente.objects.get(cpf=cpf, data_nascimento=data_nascimento_obj)
            return redirect('pacientes:visualizar_prontuario_publico', cpf=paciente.cpf, data_nascimento_str=data_nascimento_str)

        except Paciente.DoesNotExist:
            messages.error(request, 'Paciente não encontrado com os dados fornecidos. Verifique as informações ou entre em contato com o hospital.')
        except Paciente.MultipleObjectsReturned:
            messages.error(request, 'Múltiplos registros encontrados para estes dados. Por favor, contate o suporte do hospital.')
        except Exception as e:
            messages.error(request, f'Ocorreu um erro: {e}')

    return render(request, 'application/consultar_prontuario_form.html')


def visualizar_prontuario_publico(request, cpf, data_nascimento_str):
    try:
        data_nascimento_obj = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()
        paciente = get_object_or_404(Paciente, cpf=cpf, data_nascimento=data_nascimento_obj)
        observacoes = paciente.observacoes.filter(tipo__in=['geral', 'evolucao']).order_by('-data_criacao')[:5]
        context = {
            'paciente': paciente,
            'observacoes': observacoes,
        }
        return render(request, 'application/visualizar_prontuario_resumo.html', context)

    except ValueError:
        messages.error(request, 'Dados inválidos para visualização.')
        return redirect('pacientes:consultar_prontuario_paciente')
    
    except Exception as e:
        messages.error(request, f'Ocorreu um erro ao carregar o prontuário: {e}')
        return redirect('pacientes:consultar_prontuario_paciente')