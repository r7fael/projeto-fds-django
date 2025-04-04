from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('application.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('consultas/', include('consultas.urls', namespace='consultas')),
    path('pacientes/', include('pacientes.urls', namespace='pacientes')),
    path('medicamentos/', include('medicamentos.urls', namespace='medicamentos')),
]
