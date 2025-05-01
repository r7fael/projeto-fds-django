from django.db import models
from pacientes.models import Paciente

class Andar(models.Model):
    numero = models.PositiveIntegerField(unique=True, verbose_name="Número do Andar")
    descricao = models.CharField(max_length=100, blank=True, verbose_name="Descrição")
    
    @property
    def total_quartos(self):
        return self.quartos.count()
    
    @property
    def quartos_ocupados(self):
        return self.quartos.filter(paciente__isnull=False).count()
    
    @property
    def quartos_disponiveis(self):
        return self.total_quartos - self.quartos_ocupados
    
    @property
    def taxa_ocupacao(self):
        if self.total_quartos == 0:
            return 0
        return (self.quartos_ocupados / self.total_quartos) * 100

    def __str__(self):
        return f"Andar {self.numero} - {self.descricao or 'Sem descrição'}"

    class Meta:
        verbose_name = "Andar"
        verbose_name_plural = "Andares"
        ordering = ['numero']

class Quarto(models.Model):
    andar = models.ForeignKey(Andar, on_delete=models.CASCADE, related_name='quartos')
    numero = models.PositiveIntegerField(verbose_name="Número do Quarto")
    paciente = models.OneToOneField(
        Paciente, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='quarto',
        verbose_name="Paciente Internado"
    )
    data_ocupacao = models.DateField(null=True, blank=True, verbose_name="Data de Ocupação")

    class Meta:
        unique_together = ('andar', 'numero')
        verbose_name = "Quarto"
        verbose_name_plural = "Quartos"
        ordering = ['andar__numero', 'numero']

    def __str__(self):
        status = "Ocupado" if self.paciente else "Disponível"
        return f"Andar {self.andar.numero} - Quarto {self.numero} ({status})"

    def save(self, *args, **kwargs):
        if self.paciente and not self.data_ocupacao:
            from datetime import date
            self.data_ocupacao = date.today()
        elif not self.paciente:
            self.data_ocupacao = None
        super().save(*args, **kwargs)