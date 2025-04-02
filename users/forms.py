from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Medico, Enfermeiro, Farmaceutico, Paciente

TIPO_USUARIOS = [
    ('medico', 'Médico'),
    ('enfermeiro', 'Enfermeiro'),
    ('farmaceutico', 'Farmacêutico'),
    ('paciente', 'Paciente')
]

class CadastroUsuario(UserCreationForm):
    tipo_usuario = forms.ChoiceField(choices=TIPO_USUARIOS)
    registro_profissional = forms.CharField(max_length=20, required=False, label="Registro Profissional")
    cpf = forms.CharField(max_length=14, required=False, label="É paciente? Digite seu CPF")
    data_nascimento = forms.DateField(required=False, label = "É paciente? Digite sua data de nascimento")
    
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
                
            elif tipo == 'paciente':
                Paciente.objects.create(
                    usuario=user,
                    cpf=self.cleaned_data['cpf'],
                    data_nascimento=self.cleaned_data['data_nascimento']
                )
                
        return user