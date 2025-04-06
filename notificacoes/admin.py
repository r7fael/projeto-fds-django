from django.contrib import admin
from .models import Paciente, Lembrete

class LembreteAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'medico', 'tipo', 'data_lembrete', 'concluido', 'prioridade')
    list_filter = ('concluido', 'tipo', 'medico')
    search_fields = ('paciente__nome', 'descricao')

admin.site.register(Paciente)
admin.site.register(Lembrete, LembreteAdmin)