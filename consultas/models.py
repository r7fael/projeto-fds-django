from django.db import models
from users.models import Medico
from pacientes.models import Paciente

class Consulta(models.Model):
    medico = models.ForeignKey(
        Medico,
        on_delete=models.CASCADE,
        related_name='consultas'
    )
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='consultas'
    )
    data = models.DateTimeField()
    descricao = models.TextField()

    def __str__(self):
        return f"Consulta de {self.paciente.usuario.nome_completo} com {self.medico.usuario.nome_completo} em {self.data.strftime('%d/%m/%Y %H:%M')}"
