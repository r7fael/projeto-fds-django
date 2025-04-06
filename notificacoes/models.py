from django.conf import settings
from django.db import models
from django.utils import timezone

class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    historico = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nome

class Lembrete(models.Model):
    TIPO_CHOICES = [
        ('CONSULTA', 'Consulta de Retorno'),
        ('EXAME', 'Exame de Acompanhamento'),
        ('MEDICAMENTO', 'Controle de Medicação'),
        ('OUTRO', 'Outro'),
    ]
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    descricao = models.TextField()
    data_lembrete = models.DateTimeField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    concluido = models.BooleanField(default=False)
    prioridade = models.PositiveSmallIntegerField(default=1, choices=[(1, 'Baixa'), (2, 'Média'), (3, 'Alta')])
    
    class Meta:
        ordering = ['-prioridade', 'data_lembrete']
    
    def __str__(self):
        return f"Lembrete para {self.paciente} - {self.get_tipo_display()}"
    
    def esta_atrasado(self):
        return not self.concluido and self.data_lembrete < timezone.now()