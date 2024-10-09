from django.db import models

class Camiseta(models.Model):
    time = models.CharField(max_length=100)
    temporada = models.CharField(max_length=50)
    estilo = models.CharField(max_length=50)
    cor_principal = models.CharField(max_length=50)
    patrocinador = models.CharField(max_length=100, blank=True, null=True) 
    marca = models.CharField(max_length=100, blank=True, null=True)
    tamanho = models.CharField(max_length=10)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_em_estoque = models.IntegerField()
    imagem = models.ImageField(upload_to='camisetas/', blank=True, null=True)
