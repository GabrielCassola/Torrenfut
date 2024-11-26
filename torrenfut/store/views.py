from django.http import HttpResponse, Http404
from django.template import loader
from .models import Camiseta, CamisetaTamanho, HistoricoEstoque, Time, Liga, Marca
import json
from django.shortcuts import render, get_object_or_404
from collections import defaultdict
from .models import Camiseta, CamisetaTamanho, TipoProduto

def obter_opcoes_filtro():
    # Obter opções únicas para filtro
    cores_disponiveis = Camiseta.objects.values_list('cor_principal', flat=True).distinct().order_by('cor_principal')
    marcas_disponiveis = Marca.objects.all().order_by('nome')
    times_disponiveis = Time.objects.all().order_by('nome')
    temporadas_disponiveis = Camiseta.objects.values_list('temporada', flat=True).distinct()
    tipos_produto_disponiveis = TipoProduto.objects.all()
    ligas_disponiveis = Liga.objects.all().order_by('nome')

    
    return {
        'cores_disponiveis': cores_disponiveis,
        'marcas_disponiveis': marcas_disponiveis,
        'times_disponiveis': times_disponiveis,
        'temporadas_disponiveis': temporadas_disponiveis,
        'tipos_produto_disponiveis': tipos_produto_disponiveis,
        'ligas_disponiveis': ligas_disponiveis,

    }


def store(request):
    camisetas = Camiseta.objects.all()
    template = loader.get_template('home.html')
    opcoes_filtro = obter_opcoes_filtro()
    context = {
        'camisetas': camisetas,
        **opcoes_filtro,
    }
    return HttpResponse(template.render(context, request))


def produto(request, time_nome, estilo, temporada):
    try:
        # Buscar o time pelo nome, que agora é uma chave estrangeira
        time = get_object_or_404(Time, nome=time_nome)
        
        # Usando get() para buscar a camiseta que corresponde ao time, estilo e temporada
        camiseta = Camiseta.objects.get(time=time, estilo=estilo, temporada=temporada)
        tamanhos = CamisetaTamanho.objects.filter(camiseta=camiseta)
    except Camiseta.DoesNotExist:
        raise Http404("Camiseta não encontrada.")
    
    # Carregar o template
    template = loader.get_template('produto.html')
    
    # Obter as opções de filtro
    opcoes_filtro = obter_opcoes_filtro()
    
    # Contexto com a camiseta, tamanhos e as opções de filtro
    context = {
        'camiseta': camiseta, 
        'tamanhos': tamanhos,
        **opcoes_filtro,
    }
    
    # Retornar a resposta com o contexto
    return HttpResponse(template.render(context, request))

def grafico_estoque(request, produto_id):

    # Obtém a camiseta específica usando o produto_id
    camiseta = get_object_or_404(Camiseta, id=produto_id)

     # Obtendo valores
    time = camiseta.time
    cor_principal = camiseta.cor_principal
    marca = camiseta.marca
    temporada = camiseta.temporada
    estilo = camiseta.estilo

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
        'dados_grafico': dados_formatados,
        'time': time,
        'estilo': estilo,
        'cor_principal': cor_principal,
        'marca': marca,
        'temporada': temporada,
    }
    return render(request, 'grafico_estoque.html', context)


def filtrar_camisetas(request):
    # Obter filtros da requisição
    filtros_aplicados = {
        'cor': request.GET.get('cor'),
        'marca': request.GET.get('marca'),
        'time': request.GET.get('time'),
        'temporada': request.GET.get('temporada'),
        'tipo_produto': request.GET.get('tipo_produto'),
        'liga': request.GET.get('liga'),
    }

    # Remover filtros que não estão preenchidos
    filtros_aplicados = {chave: valor for chave, valor in filtros_aplicados.items() if valor}

    # Buscar todas as camisetas e aplicar filtros
    camisetas = Camiseta.objects.all()
    if 'cor' in filtros_aplicados:
        camisetas = camisetas.filter(cor_principal=filtros_aplicados['cor'])
    if 'marca' in filtros_aplicados:
        camisetas = camisetas.filter(marca=filtros_aplicados['marca'])
    if 'time' in filtros_aplicados:
        camisetas = camisetas.filter(time=filtros_aplicados['time'])
    if 'temporada' in filtros_aplicados:
        camisetas = camisetas.filter(temporada=filtros_aplicados['temporada'])
    if 'tipo_produto' in filtros_aplicados:
        camisetas = camisetas.filter(tipo_produto__id=filtros_aplicados['tipo_produto'])
    if 'liga' in filtros_aplicados:
        camisetas = camisetas.filter(time__liga=filtros_aplicados['liga'])

    # Obter opções únicas para filtro
    cores_disponiveis = Camiseta.objects.values_list('cor_principal', flat=True).distinct()
    marcas_disponiveis = Marca.objects.all()
    times_disponiveis = Time.objects.all()
    temporadas_disponiveis = Camiseta.objects.values_list('temporada', flat=True).distinct()
    tipos_produto_disponiveis = TipoProduto.objects.all()
    ligas_disponiveis = Liga.objects.all()
    print(temporadas_disponiveis)

    # Renderizar o template
    return render(request, 'home.html', {
        'camisetas': camisetas,
        'cores_disponiveis': cores_disponiveis,
        'marcas_disponiveis': marcas_disponiveis,
        'times_disponiveis': times_disponiveis,
        'temporadas_disponiveis': temporadas_disponiveis,
        'tipos_produto_disponiveis': tipos_produto_disponiveis,
        'ligas_disponiveis': ligas_disponiveis,
        'filtros_aplicados': filtros_aplicados,  # Enviar os filtros ativos
    })


def sobre(request):
    return render(request, 'sobre.html')  # Carrega a página 'sobre.html'

def quem_somos(request):
    return render(request, 'quem_somos.html')  # Carrega a página 'quem_somos.html'
