from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import CamisetaTamanho, HistoricoEstoque

@receiver(post_save, sender=CamisetaTamanho) # O email é enviado a cada vez que um produto é atualizado
def verificar_estoque(sender, instance, **kwargs):
    camiseta = instance.camiseta
    if instance.estoque_baixo():
        # Enviar alerta de baixo estoque por e-mail
        send_mail(
            subject = 'Alerta de baixo estoque',
            message = (
            f'O estoque do produto {camiseta.time} ({camiseta.marca}) está abaixo do mínimo.\n'
            f'Cor Principal: {camiseta.cor_principal}\n'
            f'Patrocinador: {camiseta.patrocinador}\n'
            f'Tamanho: {instance.tamanho}\n'
            f'Quantidade atual em estoque: {instance.quantidade_em_estoque}\n'
            f'Fornecedor: {camiseta.fornecedor.nome if camiseta.fornecedor else "Não disponível"}\n'
        ),
            from_email = 'bento.teste7009@gmail.com',  # Remetente
            recipient_list=destinatarios,  # Lista de destinatários
            fail_silently=False,
        )

destinatarios =[
    'pedro.smith@unesp.br',
    'pirs.pedrinhoo@gmail.com'
]

# Cria um sinal para a funcao HistoricoEstoque saber que o estoque foi modificado
@receiver(post_save, sender=CamisetaTamanho)
def atualizar_historico_estoque(sender, instance, **kwargs):
    HistoricoEstoque.objects.create(
        produto=instance,
        quantidade=instance.quantidade_em_estoque
    )