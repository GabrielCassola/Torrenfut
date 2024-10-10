# models.py (app de fornecedores)
from django.db import models

class TipoProduto(models.Model):
    nome = models.CharField(max_length=50)
    def __str__(self):
        return self.nome 

class Fornecedor(models.Model):
    nome = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    telefone = models.CharField(max_length=20)
    cnpj = models.CharField(max_length=50)
    tipo_produto = models.ForeignKey(TipoProduto, on_delete=models.CASCADE)
    def __str__(self):
        return self.nome

class TaxaFornecedor(models.Model):
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, related_name='taxas')
    nome = models.CharField(max_length=100)
    percentual = models.DecimalField(max_digits=5, decimal_places=2)  # percentual da taxa

class Taxa(models.Model):
    tipos_produto = models.ManyToManyField(TipoProduto, related_name='taxas') 
    nome = models.CharField(max_length=100)
    percentual = models.DecimalField(max_digits=5, decimal_places=2)  # percentual da taxa geral