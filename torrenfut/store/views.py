from django.http import HttpResponse, Http404
from django.template import loader
from .models import Camiseta, CamisetaTamanho


def store(request):
    camisetas = Camiseta.objects.all()
    template = loader.get_template('home.html')
    context = {
        'camisetas': camisetas,
    }
    return HttpResponse(template.render(context, request))


def produto(request, time, estilo, temporada):
    try:
        # Usando get() para buscar uma única camiseta
        camiseta = Camiseta.objects.get(time=time, estilo=estilo, temporada=temporada)
        tamanhos = CamisetaTamanho.objects.filter(camiseta=camiseta)
    except Camiseta.DoesNotExist:
        raise Http404("Camiseta não encontrada.")
    
    template = loader.get_template('produto.html')
    context = {
        'camiseta': camiseta, 
        'tamanhos': tamanhos,

    }
    return HttpResponse(template.render(context, request))
