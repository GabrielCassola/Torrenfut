import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.contrib.admin.models import LogEntry, CHANGE
import re
from django.utils.html import format_html

# Função auxiliar para extrair a mudança de estoque
def extrair_valor_estoque(mensagem):
    match = re.search(r'Alterado Quantidade em estoque para (\d+)', mensagem)
    if match:
        return int(match.group(1))
    return None

# Função para gerar o gráfico
def gerar_grafico(produto):
    # Pegue as entradas do log relacionadas ao produto
    logs = LogEntry.objects.filter(
        object_id=produto.id,
        object_repr=str(produto),
        action_flag=CHANGE
    ).order_by('action_time')

    datas = []
    estoques = []

    # Extraia o estoque a partir do log
    for log in logs:
        mensagem = log.change_message
        estoque = extrair_valor_estoque(mensagem)
        if estoque is not None:
            datas.append(log.action_time)
            estoques.append(estoque)

    # Gerar o gráfico se houver dados
    if datas and estoques:
        fig, ax = plt.subplots()
        ax.plot(datas, estoques, marker='o')
        ax.set_title('Nível de Estoque ao Longo do Tempo')
        ax.set_xlabel('Data')
        ax.set_ylabel('Quantidade em Estoque')

        # Converter o gráfico para um formato visualizável no Django Admin
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        imagem_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close(fig)
        
        # Retornar a imagem para ser renderizada no template do admin
        return format_html(f'<img src="data:image/png;base64,{imagem_base64}" />')
    else:
        return "Nenhuma alteração de estoque registrada."



