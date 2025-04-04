from django.shortcuts import render, get_object_or_404
from .models import Consulta

def lista_consultas(request):
    consultas = Consulta.objects.all()
    return render(request, 'consultas/lista.html', {'consultas': consultas})

def detalhes_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    return render(request, 'consultas/detalhes.html', {'consulta': consulta})
