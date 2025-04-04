from django.db import models
from users.models import Medico, Paciente

class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    data = models.DateTimeField()

class Notificacao(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    mensagem = models. TextField()
    lida = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
