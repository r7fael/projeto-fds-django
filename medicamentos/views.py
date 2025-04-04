from django.shortcuts import render

def lista_medicamentos(request):
    return render(request, 'medicamentos/lista.html')