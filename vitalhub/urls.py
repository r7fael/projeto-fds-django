from django.contrib import admin
from django.urls import path, include
from application import views as application_views

urlpatterns = [
    path('', application_views.home, name='home'),
    path('application/', include('application.urls', namespace='application')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('consultas/', include('consultas.urls', namespace='consultas')),
    path('pacientes/', include('pacientes.urls', namespace='pacientes')),
    path('medicamentos/', include('medicamentos.urls', namespace='medicamentos')),
    path('notificacoes/', include('notificacoes.urls', namespace='notificacoes')),
    
]
