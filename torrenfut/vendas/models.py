from django.db import models
from django.contrib.auth.models import User
from store.models import Camiseta, CamisetaTamanho  # Camiseta importada do outro app

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
        return self.quantidade * self.camiseta.valor_final

    def __str__(self):
        return f'{self.camiseta.time} - {self.tamanho.tamanho}'
