from django.urls import path
from . import views

urlpatterns = [
    path('adicionar/<int:camiseta_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/', views.ver_carrinho, name='ver_carrinho'),
    path('remover/<int:item_id>/', views.remover_item, name='remover_item'), 
    path('confirmar/', views.confirmar_compra, name='confirmar_compra'),
]
