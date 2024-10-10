from django.contrib import admin
from .models import Fornecedor, TipoProduto, TaxaFornecedor, Taxa

class TaxaFornecedorInline(admin.TabularInline):
    model = TaxaFornecedor
    extra = 1  # Quantas linhas extras mostrar

class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'cnpj', 'tipo_produto', 'taxas_list')
    inlines = [TaxaFornecedorInline]

    def taxas_list(self, obj):
        return ", ".join([taxa.nome for taxa in obj.taxas.all()])
    taxas_list.short_description = 'Taxas do Fornecedor'

class TipoProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome',)

class TaxaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'percentual')

admin.site.register(Fornecedor, FornecedorAdmin)
admin.site.register(TipoProduto, TipoProdutoAdmin)
admin.site.register(Taxa, TaxaAdmin)
