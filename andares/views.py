from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Andar, Quarto
from pacientes.models import Paciente

def controle_andares(request):
    if Andar.objects.count() == 0:
        criar_andares_e_quartos()
    
    andares = Andar.objects.all().prefetch_related('quartos')
    
    total_andares = Andar.objects.count()
    total_quartos = Quarto.objects.count()
    quartos_ocupados = Quarto.objects.filter(paciente__isnull=False).count()
    quartos_disponiveis = total_quartos - quartos_ocupados
    taxa_ocupacao = (quartos_ocupados / total_quartos * 100) if total_quartos > 0 else 0
    
    pacientes_disponiveis = Paciente.objects.filter(quarto__isnull=True)
    
    context = {
        'andares': andares,
        'total_andares': total_andares,
        'total_quartos': total_quartos,
        'quartos_ocupados': quartos_ocupados,
        'quartos_disponiveis': quartos_disponiveis,
        'taxa_ocupacao': taxa_ocupacao,
        'pacientes_disponiveis': pacientes_disponiveis,
    }
    
    return render(request, 'andares.html', context)

def atribuir_quarto(request):
    if request.method == 'POST':
        quarto_id = request.POST.get('quarto_id')
        paciente_id = request.POST.get('paciente_id')
        
        try:
            quarto = Quarto.objects.get(id=quarto_id)
            paciente = Paciente.objects.get(id=paciente_id)
            
            if quarto.paciente:
                messages.warning(request, 'Este quarto já está ocupado!')
            else:
                quarto.paciente = paciente
                quarto.save()
                messages.success(request, f'Paciente {paciente.nome_completo} atribuído ao quarto com sucesso!')
                
        except (Quarto.DoesNotExist, Paciente.DoesNotExist):
            messages.error(request, 'Erro ao atribuir quarto!')
    
    return redirect('controle_andares')

def liberar_quarto(request, quarto_id):
    try:
        quarto = Quarto.objects.get(id=quarto_id)
        if quarto.paciente:
            paciente_nome = quarto.paciente.nome_completo
            quarto.paciente = None
            quarto.data_ocupacao = None
            quarto.save()
            messages.success(request, f'Quarto liberado! Paciente {paciente_nome} removido.')
        else:
            messages.warning(request, 'Este quarto já está disponível!')
    except Quarto.DoesNotExist:
        messages.error(request, 'Quarto não encontrado!')
    
    return redirect('controle_andares')

def criar_andares_e_quartos():
    for andar_num in range(1, 22):
        andar, created = Andar.objects.get_or_create(
            numero=andar_num,
            defaults={'descricao': f'Ala {((andar_num-1)//7)+1}'} 
        )

        for quarto_num in range(1, 29):
            Quarto.objects.get_or_create(
                andar=andar,
                numero=quarto_num
            )