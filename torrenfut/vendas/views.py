from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Carrinho, ItemCarrinho, Compra, ItemCompra
from store.models import Camiseta, CamisetaTamanho
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse
from django.db.models import Sum, F


@login_required
def adicionar_ao_carrinho(request, camiseta_id):
    camiseta = get_object_or_404(Camiseta, id=camiseta_id)
    referer = request.META.get('HTTP_REFERER', '/')
    
    # Obter o tamanho do formulário
    tamanho_id = request.POST.get('tamanho_id')
    tamanho = get_object_or_404(CamisetaTamanho, id=tamanho_id)

    # Obter a quantidade do formulário
    quantidade = int(request.POST.get('quantidade', 1))  # Pega a quantidade do input, padrão 1

    # Verifica se a quantidade solicitada está disponível no estoque
    if quantidade > tamanho.quantidade_em_estoque:
        messages.error(request, f'Estoque insuficiente. Apenas {tamanho.quantidade_em_estoque} unidades disponíveis.')
        return redirect('ver_camiseta', camiseta_id=camiseta_id)

    # Obter ou criar o carrinho do usuário
    carrinho, created = Carrinho.objects.get_or_create(usuario=request.user)

    # Verifica se o item já está no carrinho
    item_carrinho, created = ItemCarrinho.objects.get_or_create(
        carrinho=carrinho,
        camiseta=camiseta,
        tamanho=tamanho
    )

    if created:
        # Se o item foi criado, a quantidade inicial deve ser a solicitada
        item_carrinho.quantidade = quantidade
    else:
        # Se o item já estava no carrinho, somar a quantidade solicitada à atual, verificando o estoque
        nova_quantidade = item_carrinho.quantidade + quantidade
        if nova_quantidade <= tamanho.quantidade_em_estoque:
            item_carrinho.quantidade = nova_quantidade
        else:
            messages.error(request, f'Estoque insuficiente. Você já possui {item_carrinho.quantidade} no carrinho.')
            return redirect(referer)

    item_carrinho.save()

    # Atualizar o estoque
    tamanho.quantidade_em_estoque -= quantidade
    tamanho.save()
    
    return redirect(referer)


# Ver o carrinho
@login_required
def ver_carrinho(request):
    carrinho = get_object_or_404(Carrinho, usuario=request.user)
    context = {'carrinho': carrinho}
    return render(request, 'carrinho.html', context)

# Confirmar compra
@login_required
def confirmar_compra(request):
    # Obtém o carrinho do usuário
    carrinho = get_object_or_404(Carrinho, usuario=request.user)
    if carrinho.itens.count() == 0:
        messages.error(request, "Seu carrinho está vazio.")
        return redirect('ver_carrinho')

    # Calcular o total da compra
    total = sum(item.camiseta.valor_final * item.quantidade for item in carrinho.itens.all())

    # Criar a compra
    compra = Compra(usuario=request.user, total=total)
    compra.save()  # Isso garante que a compra tenha um ID

    # Adicionar cada item do carrinho à compra
    for item in carrinho.itens.all():
        ItemCompra.objects.create(
            compra=compra,  # Aqui a compra já tem um ID
            camiseta=item.camiseta,
            tamanho=item.tamanho,
            quantidade=item.quantidade,
            preco_unitario=item.camiseta.valor_final
        )
        # Atualizar o estoque e deletar o item do carrinho
        item.tamanho.quantidade_em_estoque -= item.quantidade
        item.tamanho.save()
        item.delete()  # Remover o item do carrinho

    enviar_email_confirmacao_compra(compra, request.user)
    messages.success(request, 'Compra realizada com sucesso!')
    return redirect('perfil')

def enviar_email_confirmacao_compra(compra, usuario):
    usuario_email = usuario.email
    itens_compra = compra.itens_compra.all()  # Pega todos os itens da compra atual

    mensagem = f"Olá {usuario.first_name},\n\n"
    mensagem += "Obrigado pela sua compra! Aqui estão os detalhes do seu pedido:\n\n"

    for item in itens_compra:
        mensagem += f"- {item.camiseta.time} {item.camiseta.estilo} {item.camiseta.temporada} ({item.tamanho.tamanho}) x{item.quantidade} - R$ {item.subtotal():.2f}\n"

    mensagem += f"Total: R$ {compra.total:.2f}\n\n"
    mensagem += "Agradecemos por escolher nossa loja!\n\nAtenciosamente,\nEquipe Torrenfut"

    send_mail(
        subject='Confirmação de compra',
        message=mensagem,
        from_email='bento.teste7009@gmail.com',
        recipient_list=[usuario_email],
        fail_silently=False,
    )



@login_required
def remover_item(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id, carrinho__usuario=request.user)
    
    # Restaurar o estoque do tamanho removido
    item.tamanho.quantidade_em_estoque += item.quantidade
    item.tamanho.save()
    
    item.delete()
   # messages.success(request, 'Item removido com sucesso do carrinho.')
    
    return redirect('ver_carrinho')

def relatorio_vendas(modeladmin, request, queryset): # Action no admin exige 3 argumentos, mesmo que não sejam usados

     # Obter os itens de compra apenas das compras selecionadas
    itens = ItemCompra.objects.filter(compra__in=queryset)
    compras = Compra.objects.prefetch_related('itens_compra').filter(id__in=queryset)

    # Calcular o total de cada produto vendido e o total arrecadado
    totais_por_produto = itens.values('camiseta__time', 'tamanho__tamanho').annotate(
    total_quantidade=Sum('quantidade'),
    total_arrecadado=Sum(F('quantidade') * F('preco_unitario'))
    )

    total_geral = sum(item.subtotal() for item in itens)

    # Carregar o template e passar apenas os itens filtrados
    template = loader.get_template('relatorio_vendas.html')
    context = {
        'compras': compras,
        'itens': itens,  # Somente itens das compras selecionadas
        'totais_por_produto': totais_por_produto, # Total vendido por produto
        'total_geral': total_geral  # Total arrecado
    }
    return HttpResponse(template.render(context, request))