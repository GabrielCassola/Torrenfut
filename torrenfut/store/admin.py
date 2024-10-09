from django.contrib import admin
from .models import Camiseta, CamisetaTamanho

class CamisetaTamanhoInline(admin.TabularInline):
    model = CamisetaTamanho
    extra = 1  # Quantas linhas extras mostrar

class CamisetasAdmin(admin.ModelAdmin):
    list_display = ("time", "temporada", "estilo", "get_quantidade_total_estoque", "preco")
    inlines = [CamisetaTamanhoInline]

    def get_quantidade_total_estoque(self, obj):
        # Soma a quantidade de estoque de todos os tamanhos relacionados
        return sum(tamanho.quantidade_em_estoque for tamanho in obj.tamanhos.all())
    
    get_quantidade_total_estoque.short_description = 'Quantidade Total em Estoque'  # Nome que aparecerá na coluna

# Register your models here.
admin.site.register(Camiseta, CamisetasAdmin)
