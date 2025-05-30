from django.db import models
from datetime import date
from users.models import Medico, Enfermeiro
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    registro_profissional = models.CharField(max_length=20, blank=True)

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
    
    autor_enfermeiro = models.ForeignKey(Enfermeiro, on_delete=models.SET_NULL, null=True, blank=True, related_name='observacoes_feitas')
    autor_medico = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True, blank=True, related_name='observacoes_feitas')
    
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

    def get_autor_display(self):
        if self.autor_medico:
            return f"Dr(a). {self.autor_medico.usuario.nome_completo} (Médico)"
        elif self.autor_enfermeiro:
            return f"Enf. {self.autor_enfermeiro.usuario.nome_completo} (Enfermeiro)"
        return "Profissional de Saúde"