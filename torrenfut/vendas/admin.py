from django.contrib import admin
from .models import Compra

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'data_compra', 'total', 'usuario_id')  
    search_fields = ('usuario__username',)

    def usuario_id(self, obj):
        return obj.usuario.id  
    usuario_id.short_description = 'ID do Usuário'  