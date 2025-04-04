from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm
from .forms import CadastroUsuario
from users.models import Medico

def cadastrar_usuario(request):
    if request.method == 'POST':
        form = CadastroUsuario(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('pagina_de_sucesso')
    
    else:
        form = CadastroUsuario()
    
    return render(request, 'application/cadastro.html', {'form' : form})

def login_usuario(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username = email, password = password)

            if user is not None:
                login(request, user)
                
                if Medico.objects.filter(usuario = user).exists():
                    return redirect('painel_medico')
                
                return redirect('pagina_inicial')
            
            else:
                messages.error(request, "Email ou senha inválidos")
    
    else:
        form = LoginForm()
    
    return render(request, 'application/login.html', {'form' : form})