from django.db import models
from django.contrib.auth.models import User

class Medicamento(models.Model):
    nome = models.CharField(max_length=100)
    principio_ativo = models.CharField(max_length=100)
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return self.nome