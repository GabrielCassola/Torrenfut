from django.contrib import admin
from .models import Compra, ItemCompra
from .views import relatorio_vendas

class ItemCompraInline(admin.TabularInline):
    model = ItemCompra
    readonly_fields = ('camiseta', 'tamanho', 'quantidade', 'preco_unitario', 'subtotal')
    can_delete = False
    extra = 0

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'data_compra', 'total')
    search_fields = ('usuario__username',)
    inlines = [ItemCompraInline]
    readonly_fields = ('usuario', 'data_compra', 'total')
    actions = [relatorio_vendas]