from django.contrib import admin
from .models import Camiseta

class CamisetasAdmin(admin.ModelAdmin):
  list_display = ("time", "temporada", "estilo","quantidade_em_estoque", "preco")

# Register your models here.
admin.site.register(Camiseta, CamisetasAdmin)