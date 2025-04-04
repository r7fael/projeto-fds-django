from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Medico, Enfermeiro, Farmaceutico
from pacientes.models import Paciente

TIPO_USUARIOS = [
    ('medico', 'Médico'),
    ('enfermeiro', 'Enfermeiro'),
    ('farmaceutico', 'Farmacêutico'),
]

class CadastroUsuario(UserCreationForm):
    tipo_usuario = forms.ChoiceField(choices=TIPO_USUARIOS)
    registro_profissional = forms.CharField(max_length=20, required=False, label="Registro Profissional")
    
    class Meta:
        model = Usuario
        fields = ['email', 'nome_completo', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        if commit:
            user.save()
            
            tipo = self.cleaned_data['tipo_usuario']
            
            if tipo == 'medico':
                Medico.objects.create (
                    usuario = user,
                    crm = self.cleaned_data['registro_profissional']
                )
            
            elif tipo == 'enfermeiro':
                Enfermeiro.objects.create(
                    usuario=user,
                    coren=self.cleaned_data['registro_profissional']
                )
                
            elif tipo == 'farmaceutico':
                Farmaceutico.objects.create(
                    usuario=user,
                    crf=self.cleaned_data['registro_profissional']
                )
                
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)