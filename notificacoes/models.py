from django.db import models
from users.models import Medico

class Notificacao(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificação para {self.medico.usuario.nome_completo}: {self.mensagem}"
