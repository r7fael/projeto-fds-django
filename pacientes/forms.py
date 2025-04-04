from django import forms
from pacientes.models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome_completo', 'cpf', 'data_nascimento', 'medico_responsavel']
