from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Andar, Quarto
from pacientes.models import Paciente

def is_enfermeiro(user):
    return user.groups.filter(name='Enfermeiros').exists()

@login_required
@user_passes_test(is_enfermeiro)
def painel_andares(request):
    andares = Andar.objects.all().order_by('numero')
    quartos_por_andar = {}
    
    for andar in andares:
        quartos = Quarto.objects.filter(andar=andar).order_by('numero')
        quartos_por_andar[andar] = quartos

    pacientes_sem_quarto = Paciente.objects.filter(quarto__isnull=True)
    
    if request.method == 'POST':
        andar_id = request.POST.get('andar')
        numero_quarto = request.POST.get('numero')
        paciente_id = request.POST.get('paciente')
        
        if all([andar_id, numero_quarto, paciente_id]):
            try:
                andar = Andar.objects.get(id=andar_id)
                paciente = Paciente.objects.get(id=paciente_id)
                
                quarto, created = Quarto.objects.get_or_create(
                    andar=andar,
                    numero=numero_quarto,
                    defaults={'paciente': paciente}
                )
                
                if not created:
                    quarto.paciente = paciente
                    quarto.save()
                
                return redirect('painel_andares')
            except (Andar.DoesNotExist, Paciente.DoesNotExist):
                pass

    context = {
        'quartos_por_andar': quartos_por_andar,
        'pacientes_sem_quarto': pacientes_sem_quarto,
        'andares': andares,
    }
    return render(request, 'Painel_enfermeiro.html', context)

@login_required
@user_passes_test(is_enfermeiro)
def liberar_quarto(request, quarto_id):
    quarto = get_object_or_404(Quarto, id=quarto_id)
    quarto.paciente = None
    quarto.save()
    return redirect('painel_andares')