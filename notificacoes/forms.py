from django import forms
from .models import Lembrete, Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'historico': forms.Textarea(attrs={'rows': 4}),
        }

class LembreteForm(forms.ModelForm):
    class Meta:
        model = Lembrete
        fields = ['paciente', 'tipo', 'descricao', 'data_lembrete', 'prioridade']
        widgets = {
            'data_lembrete': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(LembreteForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['paciente'].queryset = Paciente.objects.all()  # Você pode filtrar por pacientes do médico
            self.instance.medico = user