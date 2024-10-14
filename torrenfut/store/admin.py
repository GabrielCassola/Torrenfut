from django.contrib import admin
from .models import Camiseta, CamisetaTamanho

class CamisetaTamanhoInline(admin.TabularInline):
    model = CamisetaTamanho
    extra = 1  # Quantas linhas extras mostrar

    # Mostrar no Django que o estoque esta abaixo de 5
    def estoque_baixo_alerta(self, obj):
        if obj.estoque_baixo():
            return '⚠️ Baixo Estoque'
        return 'OK'
    estoque_baixo_alerta.short_description = 'Alerta de Estoque'

class CamisetasAdmin(admin.ModelAdmin):
    list_display = ("time", "temporada", "estilo", "estoque_total", "valor_final")
    inlines = [CamisetaTamanhoInline]



# Register your models here.
admin.site.register(Camiseta, CamisetasAdmin)
