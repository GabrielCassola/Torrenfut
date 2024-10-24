from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Carrinho, ItemCarrinho
from store.models import Camiseta, CamisetaTamanho
from django.contrib import messages

@login_required
def adicionar_ao_carrinho(request, camiseta_id):
    camiseta = get_object_or_404(Camiseta, id=camiseta_id)
    
    # Obter o tamanho do formulário
    tamanho_id = request.POST.get('tamanho_id')
    tamanho = get_object_or_404(CamisetaTamanho, id=tamanho_id)

    # Obter ou criar o carrinho do usuário
    carrinho, created = Carrinho.objects.get_or_create(usuario=request.user)

    # Verifica se o item já está no carrinho
    item_carrinho, created = ItemCarrinho.objects.get_or_create(
        carrinho=carrinho,
        camiseta=camiseta,
        tamanho=tamanho
    )
    
    if item_carrinho.quantidade < tamanho.quantidade_em_estoque:
        item_carrinho.quantidade += 1
        item_carrinho.save()

        # Reduzir momentaneamente o estoque
        tamanho.quantidade_em_estoque -= 1
        tamanho.save()

        #messages.success(request, f'{camiseta.time} foi adicionado ao carrinho.')
    else:
        messages.error(request, 'Estoque insuficiente para adicionar mais itens.')

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
