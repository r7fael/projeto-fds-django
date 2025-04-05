from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Consulta
from django.contrib.auth.decorators import login_required
from pacientes.models import Paciente
from users.models import Medico
from datetime import datetime

def lista_consultas(request):
    consultas = Consulta.objects.all()
    return render(request, 'consultas/lista.html', {'consultas': consultas})

def detalhes_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    return render(request, 'consultas/detalhes.html', {'consulta': consulta})

@login_required
def cadastrar_consulta(request):
    if request.method == 'POST':
        paciente_id = request.POST.get('paciente')
        medico_id = request.POST.get('medico')
        data_str = request.POST.get('data')
        descricao = request.POST.get('descricao', '').strip()

        if not medico_id:
            messages.error(request, "Por favor, selecione um médico")
            pacientes = Paciente.objects.all()
            medicos = Medico.objects.all()
            return render(request, 'application/cadastrar_consulta.html', {
                'pacientes': pacientes,
                'medicos': medicos
            })

        try:
            paciente = get_object_or_404(Paciente, id=paciente_id)
            medico = get_object_or_404(Medico, id=medico_id)
            data = datetime.strptime(data_str, "%Y-%m-%d").replace(hour=12, minute=0)
            
            Consulta.objects.create(
                paciente=paciente,
                medico=medico,
                data=data,
                descricao=descricao
            )
            messages.success(request, "Consulta cadastrada com sucesso!")
            return redirect('application:painel_enfermeiro')
            
        except Exception as e:
            messages.error(request, f"Erro ao cadastrar consulta: {str(e)}")
            return redirect('application:cadastrar_consulta')
    
    pacientes = Paciente.objects.all()
    medicos = Medico.objects.all()
    return render(request, 'application/cadastrar_consulta.html', {
        'pacientes': pacientes,
        'medicos': medicos
    })