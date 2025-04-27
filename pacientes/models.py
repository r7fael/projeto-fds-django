from django.db import models
from datetime import date
from users.models import Medico

class Paciente(models.Model):
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    medico_responsavel = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True, blank=True)
    precisa_retorno = models.BooleanField(default=False)
    medicamentos = models.TextField(blank=True, null=True, help_text="Lista de medicamentos e dosagens prescritos")
    
    def __str__(self):
        return f"Paciente: {self.nome_completo}"
    
    def get_idade(self):
        hoje = date.today()
        idade = hoje.year - self.data_nascimento.year
        if (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day):
            idade -= 1
        return idade