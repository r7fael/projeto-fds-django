from django.shortcuts import render

def lista_notificacoes(request):
    return render(request, 'notificacoes/lista.html')