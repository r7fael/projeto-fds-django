from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import Medico, Enfermeiro, Farmaceutico
from notificacoes.models import Notificacao
from consultas.models import Consulta
from pacientes.models import Paciente, ObservacaoSaude
from datetime import datetime
from django.utils import timezone
from notificacoes.utils import gerar_notificacoes_para_medico
from django.contrib import messages
from andares.models import Andar, Quarto

def home(request):
    return render(request, 'application/home.html')

def cadastro(request):
    return render(request, 'application/cadastro.html')

@login_required
def painel_medico(request):
    try:
        medico = Medico.objects.get(usuario=request.user)
        gerar_notificacoes_para_medico(medico)
        
        hoje = timezone.now().date()
        
        consultas = Consulta.objects.filter(
            medico=medico,
            data__gte=hoje
        ).order_by('data')

        consultas_hoje = Consulta.objects.filter(
            medico=medico,
            data=hoje
        )
        
        pacientes = Paciente.objects.filter(medico_responsavel=medico)
        notificacoes = Notificacao.objects.filter(
            medico=medico,
            lida=False
        ).order_by('-data_criacao')[:5]
        consultas_hoje = consultas.filter(data=hoje)
        pacientes_retorno = pacientes.filter(precisa_retorno=True)

        context = {
            'medico': medico,
            'consultas': consultas,
            'pacientes': pacientes,
            'notificacoes': notificacoes,
            'qtd_consultas_hoje': consultas_hoje.count(),
            'qtd_pacientes_retorno': pacientes_retorno.count(),
        }

        return render(request, 'application/painel_medico.html', context)

    except Medico.DoesNotExist:
        return render(request, 'application/nao_autorizado.html')

@login_required
def painel_enfermeiro(request):
    try:
        enfermeiro = Enfermeiro.objects.get(usuario=request.user)
    except Enfermeiro.DoesNotExist:
        return render(request, 'application/nao_autorizado.html')

    pacientes = Paciente.objects.select_related('medico_responsavel__usuario').all()
    medicos = Medico.objects.select_related('usuario').all()
    andares = Andar.objects.all().prefetch_related('quartos')
    total_andares = Andar.objects.count()
    total_quartos = Quarto.objects.count()
    quartos_ocupados = Quarto.objects.filter(paciente__isnull=False).count()
    quartos_disponiveis = total_quartos - quartos_ocupados
    taxa_ocupacao = (quartos_ocupados / total_quartos * 100) if total_quartos > 0 else 0
    pacientes_disponiveis = Paciente.objects.filter(quarto__isnull=True)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'paciente':
            nome = request.POST.get('nome_completo')
            cpf = request.POST.get('cpf')
            data_nascimento = request.POST.get('data_nascimento')
            medico_id = request.POST.get('medico_responsavel')
            medicamentos = request.POST.get('medicamentos', '')

            if nome and cpf and data_nascimento and medico_id:
                try:
                    medico = Medico.objects.get(id=medico_id)
                    Paciente.objects.create(
                        nome_completo=nome,
                        cpf=cpf,
                        data_nascimento=data_nascimento,
                        medico_responsavel=medico,
                        medicamentos=medicamentos
                    )
                    messages.success(request, 'Paciente cadastrado com sucesso!')
                    return redirect('application:painel_enfermeiro')
                except Exception as e:
                    messages.error(request, f'Erro ao cadastrar paciente: {str(e)}')
            else:
                messages.error(request, 'Por favor, preencha todos os campos do paciente.')
                
        elif form_type == 'consulta':
            paciente_id = request.POST.get('paciente')
            medico_id = request.POST.get('medico')
            data_str = request.POST.get('data')
            descricao = request.POST.get('descricao', '').strip()

            if paciente_id and medico_id and data_str and descricao:
                try:
                    paciente = Paciente.objects.get(id=paciente_id)
                    medico = Medico.objects.get(id=medico_id)
                    data_naive = datetime.strptime(data_str, "%Y-%m-%d").replace(hour=12, minute=0)
                    data = timezone.make_aware(data_naive)

                    Consulta.objects.create(
                        paciente=paciente,
                        medico=medico,
                        data=data,
                        descricao=descricao
                    )
                    messages.success(request, 'Consulta cadastrada com sucesso!')
                    return redirect('application:painel_enfermeiro')
                except Exception as e:
                    messages.error(request, f'Erro ao cadastrar consulta: {str(e)}')
            else:
                messages.error(request, 'Por favor, preencha todos os campos da consulta.')

        elif form_type == 'medicamentos':
            paciente_id = request.POST.get('paciente_id')
            medicamentos = request.POST.get('medicamentos', '').strip()
            
            if paciente_id:
                try:
                    paciente = Paciente.objects.get(id=paciente_id)
                    paciente.medicamentos = medicamentos
                    paciente.save()
                    messages.success(request, 'Medicamentos atualizados com sucesso!')
                except Exception as e:
                    messages.error(request, f'Erro ao atualizar medicamentos: {str(e)}')
        
        elif form_type == 'observacao':
            paciente_id = request.POST.get('paciente_id')
            tipo = request.POST.get('tipo')
            observacao_texto = request.POST.get('observacao', '').strip()
            
            if paciente_id and tipo and observacao_texto:
                try:
                    paciente = Paciente.objects.get(id=paciente_id)
                    ObservacaoSaude.objects.create(
                        paciente=paciente,
                        autor=enfermeiro,
                        tipo=tipo,
                        observacao=observacao_texto,
                        data_criacao=timezone.now()
                    )
                    messages.success(request, 'Observação adicionada com sucesso!')
                except Exception as e:
                    messages.error(request, f'Erro ao adicionar observação: {str(e)}')
            else:
                messages.error(request, 'Por favor, preencha todos os campos da observação.')

    context = {
        'enfermeiro': enfermeiro,
        'pacientes': pacientes,
        'medicos': medicos,
        'tipos_observacao': ObservacaoSaude.TIPO_CHOICES,
        'andares': andares,
        'total_andares': total_andares,
        'total_quartos': total_quartos,
        'quartos_ocupados': quartos_ocupados,
        'quartos_disponiveis': quartos_disponiveis,
        'taxa_ocupacao': taxa_ocupacao,
        'pacientes_disponiveis': pacientes_disponiveis,
    }

    return render(request, 'application/painel_enfermeiro.html', context)

@login_required
def painel_farmaceutico(request):
    try:
        farmaceutico = Farmaceutico.objects.get(usuario=request.user) 
        
        context = {
            'farmaceutico': farmaceutico,
        }

        return render(request, 'application/painel_farmaceutico.html', context)

    except Farmaceutico.DoesNotExist:
        return render(request, 'application/nao_autorizado.html')