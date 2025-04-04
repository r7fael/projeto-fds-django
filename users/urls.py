from django.urls import include, path
from . import views

app_name = 'users'

urlpatterns = [
    path('cadastrar/', views.cadastrar_usuario, name='cadastrar'),
    path('login/', views.login_usuario, name='login'),
    path('application/', include('application.urls')),
]
