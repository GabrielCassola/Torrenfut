from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import CamisetaTamanho, HistoricoEstoque
from .middleware import get_current_user



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

# Este sinal é executado antes da instância ser salva, então podemos capturar o valor atual
@receiver(pre_save, sender=CamisetaTamanho)
def capturar_quantidade_anterior(sender, instance, **kwargs):
    if instance.pk:  # Verifica se a instância já existe no banco de dados
        # Obtém a instância do banco de dados antes da atualização
        original_instance = CamisetaTamanho.objects.get(pk=instance.pk)
        # Armazena a quantidade anterior na instância
        instance.estoque_anterior = original_instance.quantidade_em_estoque


# Cria um sinal para a funcao HistoricoEstoque saber que o estoque foi modificado
@receiver(post_save, sender=CamisetaTamanho)
def atualizar_historico_estoque(sender, instance, created, **kwargs):
    if not created:  # Apenas para atualizações

        user = get_current_user()  # Obtém o usuário atual
        email_usuario = user.email if user.is_authenticated else 'email@exemplo.com'  # Default ou tratamento

        # Criar um registro no histórico
        HistoricoEstoque.objects.create(
            camiseta=instance.camiseta,
            produto=instance,
            estoque_anterior=instance.estoque_anterior,
            estoque_novo=instance.quantidade_em_estoque,
            email_usuario=email_usuario,
            tamanho=instance.tamanho,
        )