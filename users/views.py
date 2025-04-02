from django.shortcuts import render, redirect
from .forms import CadastroUsuario

def cadastrar_usuario(request):
    if request.method == 'POST':
        form = CadastroUsuario(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('pagina_de_sucesso')
    
    else:
        form = CadastroUsuario()
    
    return render(request, 'users/cadastro.html', {'form' : form})
