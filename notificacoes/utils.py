from pacientes.models import Paciente
from consultas.models import Consulta
from .models import Notificacao
from datetime import date

def gerar_notificacoes_para_medico(medico):
    notificacoes_geradas = []

    consultas_hoje = Consulta.objects.filter(medico=medico, data=date.today())
    if consultas_hoje.exists():
        mensagem = f"Você tem {consultas_hoje.count()} consulta(s) agendada(s) para hoje."
        Notificacao.objects.get_or_create(medico=medico, mensagem=mensagem, lida=False)
        notificacoes_geradas.append(mensagem)

    pacientes_retorno = Paciente.objects.filter(medico_responsavel=medico, precisa_retorno=True)
    if pacientes_retorno.exists():
        mensagem = f"{pacientes_retorno.count()} paciente(s) precisam de retorno."
        Notificacao.objects.get_or_create(medico=medico, mensagem=mensagem, lida=False)
        notificacoes_geradas.append(mensagem)

    return notificacoes_geradas
