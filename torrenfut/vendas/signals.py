
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Compra, ItemCompra

@receiver(post_save, sender=Compra)
def enviar_email_confirmacao_compra(sender, instance, created, **kwargs):
    if created:
            usuario_email = instance.usuario.email
            usuario = instance.usuario
            itens = ItemCompra.objects.filter(compra=instance)

            if not itens.exists():
                print("Nenhum item encontrado para esta compra.")
            else:
                print(f"Itens encontrados para a compra {instance.id}: {[str(item) for item in itens]}")

            mensagem = f"Olá {usuario.username},\n\n"
            mensagem += "Obrigado pela sua compra! Aqui estão os detalhes do seu pedido:\n\n"

            for item in itens:
                mensagem += f"- {item.camiseta.time} ({item.tamanho.tamanho}) x{item.quantidade} - R$ {item.subtotal():.2f}\n"

            mensagem += f"\nTotal: R$ {instance.total:.2f}\n\n"
            mensagem += "Agradecemos por escolher nossa loja!\n\nAtenciosamente,\nEquipe da Loja"

            send_mail(
                subject='Confirmação de compra',
                message=mensagem,
                from_email='bento.teste7009@gmail.com',
                recipient_list=[usuario_email],
                fail_silently=False,
            )
