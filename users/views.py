from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm, CadastroUsuario
from users.models import Medico, Enfermeiro, Farmaceutico

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
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)

                if Medico.objects.filter(usuario=user).exists():
                    return redirect('application:painel_medico')
                elif Enfermeiro.objects.filter(usuario=user).exists():
                    return redirect('application:painel_enfermeiro')
                elif Farmaceutico.objects.filter(usuario=user).exists():
                    return redirect('application:painel_farmaceutico')

                messages.warning(request, "Usuário sem perfil associado.")
                return redirect('application:login_usuario')

            else:
                messages.error(request, "Email ou senha inválidos")
    else:
        form = LoginForm()

    return render(request, 'application/login.html', {'form': form})
