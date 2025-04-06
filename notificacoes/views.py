from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Lembrete, Paciente
from .forms import LembreteForm, PacienteForm
from django.utils import timezone

@login_required
def lista_lembretes(request):
    lembretes = Lembrete.objects.filter(
        medico=request.user,
        concluido=False
    ).order_by('data_lembrete')
    
    # Filtrar lembretes atrasados
    lembretes_atrasados = lembretes.filter(data_lembrete__lt=timezone.now())
    
    # Filtrar próximos lembretes
    lembretes_proximos = lembretes.filter(data_lembrete__gte=timezone.now())
    
    context = {
        'lembretes_atrasados': lembretes_atrasados,
        'lembretes_proximos': lembretes_proximos,
    }
    return render(request, 'lembretes/lista_lembretes.html', context)

@login_required
def adicionar_lembrete(request):
    if request.method == 'POST':
        form = LembreteForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lembrete adicionado com sucesso!')
            return redirect('lista_lembretes')
    else:
        form = LembreteForm(user=request.user)
    
    return render(request, 'lembretes/adicionar_lembrete.html', {'form': form})

@login_required
def marcar_concluido(request, lembrete_id):
    lembrete = get_object_or_404(Lembrete, id=lembrete_id, medico=request.user)
    lembrete.concluido = True
    lembrete.save()
    messages.success(request, 'Lembrete marcado como concluído!')
    return redirect('lista_lembretes')

@login_required
def adicionar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente adicionado com sucesso!')
            return redirect('lista_lembretes')
    else:
        form = PacienteForm()
    
    return render(request, 'lembretes/adicionar_paciente.html', {'form': form})