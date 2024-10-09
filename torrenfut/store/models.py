from django.db import models

class Camiseta(models.Model):
    time = models.CharField(max_length=100)
    temporada = models.CharField(max_length=50)
    estilo = models.CharField(max_length=50)
    cor_principal = models.CharField(max_length=50)
    patrocinador = models.CharField(max_length=100, blank=True, null=True) 
    marca = models.CharField(max_length=100, blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='camisetas/', blank=True, null=True)
    @property
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