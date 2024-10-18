from django.db import models

class Cliente(models.Model):
    first_name = models.CharField('nome', max_length=50, default='-')
    last_name = models.CharField('sobrenome', max_length=50, null=True) 
    email = models.EmailField(null=True)

    class Meta:
        ordering = ('first_name',)
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name or ""}'.strip()

    def __str__(self):
        return self.full_name