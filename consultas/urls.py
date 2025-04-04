from django.urls import path
from .views import lista_consultas, detalhes_consulta

app_name = 'consultas'

urlpatterns = [
    path('', lista_consultas, name='lista'),
    path('<int:consulta_id>/', detalhes_consulta, name='detalhes'),
]
