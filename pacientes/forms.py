from django import forms
from .models import RegistroPacienteAndar, Paciente

class RegistroAndarForm(forms.ModelForm):
    paciente = forms.ModelChoiceField(queryset=Paciente.objects.all(), label="Paciente")

    class Meta:
        model = RegistroPacienteAndar
        fields = ['paciente', 'andar', 'numero_quarto']