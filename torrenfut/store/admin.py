from django.contrib import admin
from .models import Camiseta, CamisetaTamanho

class CamisetaTamanhoInline(admin.TabularInline):
    model = CamisetaTamanho
    extra = 1  # Quantas linhas extras mostrar

class CamisetasAdmin(admin.ModelAdmin):
    list_display = ("time", "temporada", "estilo", "estoque_total", "preco")
    inlines = [CamisetaTamanhoInline]

# Register your models here.
admin.site.register(Camiseta, CamisetasAdmin)
