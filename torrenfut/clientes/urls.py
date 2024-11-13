from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cliente_registro, name='cadastro'),
    path('login/', views.cliente_login, name='login'),
    path('logout/', views.logout_cliente, name='logout'),  
    path('perfil/', views.perfil_cliente, name='perfil'),
    path('editar/', views.editar_perfil, name='editar_perfil'),
]
