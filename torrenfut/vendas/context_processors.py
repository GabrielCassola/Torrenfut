from .models import Carrinho

def carrinho_quantidade(request):
    if request.user.is_authenticated:
        carrinho = Carrinho.objects.filter(usuario=request.user).first()
        quantidade = sum(item.quantidade for item in carrinho.itens.all()) if carrinho else 0
    else:
        quantidade = 0
    return {'carrinho_quantidade': quantidade}
