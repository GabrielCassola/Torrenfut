from django.http import HttpResponse, Http404
from django.template import loader
from .models import Camiseta, CamisetaTamanho, HistoricoEstoque
import json
from django.shortcuts import render
from django.contrib.admin.models import LogEntry, CHANGE
import re


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
    
    try:
        produto = CamisetaTamanho.objects.get(id=produto_id)
        historico = HistoricoEstoque.objects.filter(produto=produto).order_by('data_alteracao')
    except CamisetaTamanho.DoesNotExist:
        raise Http404("Camiseta não encontrada.")
    
    dados_grafico = [["Data", "Quantidade em Estoque"]]
    for entrada in historico:
        dados_grafico.append([entrada.data_alteracao.strftime('%Y-%m-%d %H:%M:%S'), entrada.quantidade])

    template = loader.get_template('grafico_estoque.html')

    context = {
        'produto': produto,
        'dados_grafico': json.dumps(dados_grafico)
    }
    return HttpResponse(template.render(context, request))