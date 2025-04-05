from django.urls import path
from . import views
from .views import lista_consultas, detalhes_consulta

app_name = 'consultas'

urlpatterns = [
    path('', lista_consultas, name='lista'),
    path('<int:consulta_id>/', detalhes_consulta, name='detalhes'),
    path('cadastrar-consulta/', views.cadastrar_consulta, name='cadastrar_consulta'),
]
