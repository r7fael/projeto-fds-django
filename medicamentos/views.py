from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Medicamento

@login_required
def lista_medicamentos(request):
    medicamentos = Medicamento.objects.all()
    context = {
        'medicamentos': medicamentos,
        'estoque_baixo': Medicamento.objects.filter(quantidade__lte=5).count()
    }
    return render(request, 'application/painel_farmaceutico.html', context)

@login_required
def adicionar_medicamento(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        principio_ativo = request.POST.get('principio_ativo')
        quantidade = request.POST.get('quantidade')
        
        if nome and quantidade:
            Medicamento.objects.create(
                nome=nome,
                principio_ativo=principio_ativo,
                quantidade=quantidade,
            )
            return redirect('medicamentos:lista')
    
    return render(request, 'application/painel_farmaceutico.html')

@login_required
def editar_medicamento(request, pk):
    medicamento = get_object_or_404(Medicamento, pk=pk)
    
    if request.method == 'POST':
        medicamento.nome = request.POST.get('nome')
        medicamento.principio_ativo = request.POST.get('principio_ativo')
        medicamento.quantidade = request.POST.get('quantidade')
        medicamento.save()
        return redirect('medicamentos:lista')
    
    context = {'medicamento': medicamento}
    return render(request, 'application/painel_farmaceutico.html', context)

@login_required
def excluir_medicamento(request, pk):
    medicamento = get_object_or_404(Medicamento, pk=pk)
    
    if request.method == 'POST':
        medicamento.delete()
        return redirect('medicamentos:lista')
    
    context = {'medicamento': medicamento}
    return render(request, 'application/painel_farmaceutico.html', context)