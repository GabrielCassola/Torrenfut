from django.contrib import admin
from .views import exportar_estoque_csv
from .models import Camiseta, CamisetaTamanho, Time, Liga, Marca
from django.utils.html import format_html
from django.urls import reverse

class CamisetaTamanhoInline(admin.TabularInline):
    model = CamisetaTamanho
    extra = 0  # Quantas linhas extras mostrar

# Nome para a ação no admin
exportar_estoque_csv.short_description = "Exportar Estoque para CSV"


class CamisetasAdmin(admin.ModelAdmin):
    list_display = ("time", "temporada", "estilo", "estoque_total", "valor_final", "link_grafico_estoque")
    list_filter = ("time", "temporada")
    inlines = [CamisetaTamanhoInline]
    actions = [exportar_estoque_csv]

    def link_grafico_estoque(self, obj):
        url = reverse('grafico_estoque', args=[obj.id])
        return format_html('<a href="{}">Gráfico Estoque</a>', url)

    link_grafico_estoque.short_description = 'Gráfico de Estoque'
    
# Register your models here.
admin.site.register(Camiseta, CamisetasAdmin)
admin.site.register(Time)
admin.site.register(Liga)
admin.site.register(Marca)


