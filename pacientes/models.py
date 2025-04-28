from django.db import models
from datetime import date
from users.models import Medico, Enfermeiro

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

class ObservacaoSaude(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='observacoes')
    autor = models.ForeignKey(Enfermeiro, on_delete=models.SET_NULL, null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    observacao = models.TextField()

    TIPO_CHOICES = [
    ('geral', 'Geral'),
    ('medicacao', 'Medicação'),
    ('sintoma', 'Sintoma'),
    ('evolucao', 'Evolução'),
    ('outro', 'Outro')
    ]

    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    
    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'Observação de Saúde'
        verbose_name_plural = 'Observações de Saúde'
    
    def __str__(self):
        return f"Observação para {self.paciente.nome_completo} em {self.data_criacao}"

from django.db import models
from django.contrib.auth.models import User    

class Paciente(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class RegistroPacienteAndar(models.Model):
    ANDAR_CHOICES = [
        ('1', '1º Andar'),
        ('2', '2º Andar'),
        ('3', '3º Andar'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    andar = models.CharField(max_length=1, choices=ANDAR_CHOICES)
    numero_quarto = models.CharField(max_length=10)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.paciente.nome} - Andar {self.andar}, Quarto {self.numero_quarto}"