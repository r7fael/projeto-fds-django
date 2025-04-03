from django.shortcuts import render

def home(request):
    return render(request, 'application/home.html')

def cadastro(request):
    return render(request, 'application/cadastro.html')
