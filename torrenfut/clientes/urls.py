from django.urls import path
from . import views, forms 

urlpatterns = [
    path('cadastro/', views.cliente_cadastro, name='cliente_cadastro'),
]

