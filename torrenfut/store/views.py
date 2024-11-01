from django.http import HttpResponse, Http404
from django.template import loader
from .models import Camiseta, CamisetaTamanho, HistoricoEstoque
import json
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.models import LogEntry, CHANGE
import re
from collections import defaultdict

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

def grafico_estoque(request, produto_id):

    # Obtém a camiseta específica usando o produto_id
    camiseta = get_object_or_404(Camiseta, id=produto_id)

    # Obtém todos os dados do histórico de estoque
    historico = HistoricoEstoque.objects.all().filter(camiseta=camiseta).order_by('data_alteracao')

    # Organizar os dados por tamanho
    dados_grafico = defaultdict(list)
    for entrada in historico:
        dados_grafico[entrada.produto.tamanho].append([
            entrada.data_alteracao.strftime('%Y-%m-%d'),
            entrada.estoque_novo,
        ])

    # Converter para formato JSON adequado para Google Charts
    dados_formatados = json.dumps({
        tamanho: [["Data", "Estoque Novo"]] + entradas
        for tamanho, entradas in dados_grafico.items()
    })

    context = {
        'dados_grafico': dados_formatados
    }
    return render(request, 'grafico_estoque.html', context)