from django.shortcuts import render

def lista_pacientes(request):
    return render(request, 'pacientes/lista.html')

