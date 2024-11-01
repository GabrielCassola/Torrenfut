# models.py (app store)
from django.db import models
from fornecedores.models import Fornecedor, TipoProduto, Taxa
from django.utils import timezone

class Camiseta(models.Model):
    tipo_produto = models.ForeignKey(TipoProduto, default=1, on_delete=models.CASCADE)  # Supondo que o ID 1 exista em TipoProduto
    time = models.CharField(max_length=100)
    temporada = models.CharField(max_length=50)
    estilo = models.CharField(max_length=50)
    cor_principal = models.CharField(max_length=50)
    patrocinador = models.CharField(max_length=100, blank=True, null=True) 
    marca = models.CharField(max_length=100, blank=True, null=True)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='camisetas/', blank=True, null=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True)

    @property

    def valor_final(self):
        preco = self.preco_custo
        # Adicionar as taxas do fornecedor
        if self.fornecedor:
            for taxa in self.fornecedor.taxas.all():
                preco += preco * (taxa.percentual / 100)
        # Adicionar as taxas gerais que estão atreladas ao tipo de produto
        for taxa_geral in self.tipo_produto.taxas.all():  # Filtra taxas pelo tipo de produto
            preco += preco * (taxa_geral.percentual / 100)

        round(preco, 2)
        decimal = preco % 1

    # Aplicar a lógica de arredondamento
        if decimal < 0.30:
            preco = float(int(preco))  # Arredonda para 0,00
        elif decimal >= 0.30 and decimal < 0.50:
            preco = int(preco) + 0.50  # Arredonda para 0,50
        elif decimal >= 0.50:
            preco = int(preco) + 0.99  # Arredonda para 0,99
        return round(preco, 2)  # Retorna o valor final como float
    

    def estoque_total(self):
        return sum(tamanho.quantidade_em_estoque for tamanho in self.tamanhos.all())

class CamisetaTamanho(models.Model):
    TAMANHOS = [
        ('P', 'Pequeno'),
        ('M', 'Médio'),
        ('G', 'Grande'),
        ('GG', 'Extra Grande'),
    ]
    camiseta = models.ForeignKey(Camiseta, related_name='tamanhos', on_delete=models.CASCADE)
    tamanho = models.CharField(max_length=2, choices=TAMANHOS)
    quantidade_em_estoque = models.IntegerField()
    estoque_minimo = models.IntegerField(default=5) # Valor minimo para alerta de estoque

    def __str__(self):
        return self.tamanho

    def estoque_baixo(self):
        return self.quantidade_em_estoque <= self.estoque_minimo

class HistoricoEstoque(models.Model):
    camiseta = models.ForeignKey(Camiseta, related_name='historico_camisetas', on_delete=models.CASCADE)
    produto = models.ForeignKey(CamisetaTamanho, related_name ='historico_estoque', on_delete=models.CASCADE)
    estoque_anterior = models.IntegerField(default=0)  # Campo para a quantidade anterior
    estoque_novo = models.IntegerField(default=0)  # Campo para a nova quantidade
    email_usuario = models.EmailField(null=True)  # Campo para armazenar o e-mail do usuário
    tamanho = models.CharField(max_length=2, null=True)  # Campo para o tamanho do produto
    data_alteracao = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return f"{self.camiseta} e {self.produto} - {self.quantidade} em {self.data_alteracao}"