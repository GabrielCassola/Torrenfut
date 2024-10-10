from django.contrib import admin
from .models import Camiseta, CamisetaTamanho
from fornecedores.models import Fornecedor, Taxa

class CamisetaTamanhoInline(admin.TabularInline):
    model = CamisetaTamanho
    extra = 1  # Quantas linhas extras mostrar

class CamisetasAdmin(admin.ModelAdmin):
    list_display = ("time", "temporada", "estilo", "estoque_total", "valor_final")
    inlines = [CamisetaTamanhoInline]

# Register your models here.
admin.site.register(Camiseta, CamisetasAdmin)
