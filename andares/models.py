from django.db import models
from pacientes.models import Paciente

class Andar(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    descricao = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Andar {self.numero} - {self.descricao}"

class Quarto(models.Model):
    andar = models.ForeignKey(Andar, on_delete=models.CASCADE)
    numero = models.PositiveIntegerField()
    paciente = models.OneToOneField(
        Paciente, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='quarto'
    )

    class Meta:
        unique_together = ('andar', 'numero')

    def __str__(self):
        return f"Andar {self.andar.numero} - Quarto {self.numero}"
