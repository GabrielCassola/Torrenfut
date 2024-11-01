from django.db import models
from django.contrib.auth.models import User
from store.models import Camiseta, CamisetaTamanho

class Carrinho(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)

    def total_itens(self):
        return sum(item.quantidade for item in self.itens.all())

    def total_preco(self):
        return sum(item.subtotal() for item in self.itens.all())

    def __str__(self):
        return f'Carrinho de {self.usuario.username}'

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, related_name='itens', on_delete=models.CASCADE)
    camiseta = models.ForeignKey(Camiseta, on_delete=models.CASCADE)
    tamanho = models.ForeignKey(CamisetaTamanho, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def subtotal(self):
        if self.quantidade is None or self.camiseta.valor_final is None:
            return 0
        return self.quantidade * self.camiseta.valor_final

    def __str__(self):
        return f'{self.camiseta.time} - {self.tamanho.tamanho}'

class ItemCompra(models.Model):
    compra = models.ForeignKey('Compra', related_name='itens_compra', on_delete=models.CASCADE)
    camiseta = models.ForeignKey(Camiseta, on_delete=models.CASCADE)
    tamanho = models.ForeignKey(CamisetaTamanho, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        if self.quantidade is None or self.preco_unitario is None:
            return 0
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f'{self.camiseta.time} - {self.tamanho.tamanho} ({self.quantidade} unidades)'

class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_compra = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def calcular_total(self):
        # Recalcula o total somando os subtotais dos itens de compra
        return sum(item.subtotal() for item in self.itens_compra.all())

    def save(self, *args, **kwargs):
        if not self.total:
            self.total = sum(item.subtotal() for item in self.itens_compra.all())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Compra {self.id} - {self.usuario.username} em {self.data_compra}"
