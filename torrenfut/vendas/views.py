from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Carrinho, ItemCarrinho
from store.models import Camiseta, CamisetaTamanho
from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def adicionar_ao_carrinho(request, camiseta_id):
    camiseta = get_object_or_404(Camiseta, id=camiseta_id)
    
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
            return redirect('ver_carrinho')

    item_carrinho.save()

    # Atualizar o estoque
    tamanho.quantidade_em_estoque -= quantidade
    tamanho.save()

    #messages.success(request, f'{quantidade} unidade(s) de {camiseta.time} foram adicionadas ao carrinho.')
    return redirect('ver_carrinho')


# Ver o carrinho
@login_required
def ver_carrinho(request):
    carrinho = get_object_or_404(Carrinho, usuario=request.user)
    context = {'carrinho': carrinho}
    return render(request, 'carrinho.html', context)

# Confirmar compra
@login_required
def confirmar_compra(request):
    carrinho = get_object_or_404(Carrinho, usuario=request.user)

    for item in carrinho.itens.all():
        # Confirmar a remoção do estoque
        item.tamanho.quantidade_em_estoque -= item.quantidade
        item.tamanho.save()

    carrinho.delete()  # Limpar o carrinho após a compra

    messages.success(request, 'Compra confirmada com sucesso!')
    return redirect('perfil')

@login_required
def remover_item(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id, carrinho__usuario=request.user)
    
    # Restaurar o estoque do tamanho removido
    item.tamanho.quantidade_em_estoque += item.quantidade
    item.tamanho.save()
    
    item.delete()
    messages.success(request, 'Item removido com sucesso do carrinho.')
    
    return redirect('ver_carrinho')