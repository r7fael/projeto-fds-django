from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from users.models import Usuario, Medico, Enfermeiro, Farmaceutico

def cadastrar_usuario(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        nome_completo = request.POST.get('nome_completo')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        tipo_usuario = request.POST.get('tipo_usuario')
        registro_profissional = request.POST.get('registro_profissional')

        if senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem.')
            return redirect('users:cadastrar_usuario')

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Esse email já está em uso.')
            return redirect('users:cadastrar_usuario')

        usuario = Usuario.objects.create(
            email=email,
            nome_completo=nome_completo,
            password=make_password(senha)
        )

        if tipo_usuario == 'medico':
            Medico.objects.create(usuario=usuario, crm=registro_profissional)
        elif tipo_usuario == 'enfermeiro':
            Enfermeiro.objects.create(usuario=usuario, coren=registro_profissional)
        elif tipo_usuario == 'farmaceutico':
            Farmaceutico.objects.create(usuario=usuario, crf=registro_profissional)

        return redirect('users:login_usuario')

    return render(request, 'application/cadastro.html')


def login_usuario(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
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
            return redirect('users:login_usuario')

        messages.error(request, "Email ou senha inválidos")
        return redirect('users:login_usuario')

    return render(request, 'application/login.html')
