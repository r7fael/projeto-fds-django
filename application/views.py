from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import Medico, Enfermeiro
from application.models import Notificacao
from consultas.models import Consulta
from pacientes.models import Paciente
from datetime import datetime

def home(request):
    return render(request, 'application/home.html')

def cadastro(request):
    return render(request, 'application/cadastro.html')

@login_required
def painel_medico(request):
    try:
        medico = Medico.objects.get(usuario=request.user)
        
        consultas = Consulta.objects.filter(
            medico=medico,
            data__gte=datetime.now().date()  
        ).order_by('data')
        
        pacientes = Paciente.objects.filter(medico_responsavel=medico)
        
        notificacoes = Notificacao.objects.filter(
            medico=medico, 
            lida=False
        ).order_by('-data_criacao')[:5]

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
        pacientes = Paciente.objects.all()
        medicos = Medico.objects.all()

        if request.method == 'POST':
            if 'nome_completo' in request.POST:
                nome = request.POST.get('nome_completo')
                cpf = request.POST.get('cpf')
                data_nascimento = request.POST.get('data_nascimento')
                medico_id = request.POST.get('medico_responsavel')
                medico = Medico.objects.get(id=medico_id)

                Paciente.objects.create(
                    nome_completo=nome,
                    cpf=cpf,
                    data_nascimento=data_nascimento,
                    medico_responsavel=medico
                )
                return redirect('application:painel_enfermeiro')

            elif 'descricao' in request.POST:
                paciente_id = request.POST.get('paciente')
                data_str = request.POST.get('data')
                descricao = request.POST.get('descricao')
                medico_id = request.POST.get('medico')

                paciente = Paciente.objects.get(id=paciente_id)
                medico = Medico.objects.get(id=medico_id)
                data = datetime.strptime(data_str, "%Y-%m-%d").replace(hour=12, minute=0)

                Consulta.objects.create(
                    paciente=paciente,
                    medico=medico,
                    data=data,
                    descricao=descricao
                )
                return redirect('application:painel_enfermeiro')

        context = {
            'enfermeiro': enfermeiro,
            'pacientes': pacientes,
            'medicos': medicos,
        }

        return render(request, 'application/painel_enfermeiro.html', context)

    except Enfermeiro.DoesNotExist:
        return render(request, 'application/nao_autorizado.html')