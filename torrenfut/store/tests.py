import pytest
from django.db import IntegrityError
from .models import Camiseta, TipoProduto, Fornecedor
from .views import produto
from django.urls import reverse
from django.test import TestCase
from django.core.files import File
from io import BytesIO
from PIL import Image

def test_home_status_code(client): #Teste 1
    resposta = client.get('/store')
    assert resposta.status_code == 301 # Não sei porque é 301

# Teste com Models
@pytest.mark.django_db
def test_camiseta_creation(): # Teste 2
    # Criando um TipoProduto para o campo ForeignKey
    tipo_produto = TipoProduto.objects.create(nome="Camiseta Oficial")
    
    # Criando um Fornecedor para o campo ForeignKey
    fornecedor = Fornecedor.objects.create(
    nome="Fornecedor A",
    email="fornecedor@example.com",
    telefone="123456789",
    cnpj="00.000.000/0000-00",
    tipo_produto=tipo_produto
)
    
    # Criando uma camiseta
    camiseta = Camiseta.objects.create(
        tipo_produto=tipo_produto,
        time="Time A",
        liga="Liga A",
        temporada="2024",
        estilo="Estilo A",
        cor_principal="Azul",
        patrocinador="Patrocinador A",
        marca="Marca A",
        preco_custo=100.00,
        fornecedor=fornecedor
    )
    
    # Validando que o objeto camiseta foi criado e salvo corretamente
    assert camiseta.time == "Time A"
    assert camiseta.liga == "Liga A"
    assert camiseta.temporada == "2024"
    assert camiseta.estilo == "Estilo A"
    assert camiseta.cor_principal == "Azul"
    assert camiseta.patrocinador == "Patrocinador A"
    assert camiseta.marca == "Marca A"
    assert camiseta.preco_custo == 100.00
    assert camiseta.fornecedor == fornecedor

# Teste com uma view
class ProdutoViewTest(TestCase):
    
    
    @staticmethod
    def create_fake_image():
        # Cria uma imagem fictícia em memória
        image = Image.new('RGB', (100, 100), color='blue')
        img_io = BytesIO()
        image.save(img_io, 'JPEG')
        img_io.seek(0)
        return File(img_io, name='fake_image.jpg')

    @classmethod
    def setUpTestData(cls):
        # Criando os dados necessários para o teste
        tipo_produto = TipoProduto.objects.create(nome="Camisetas Esportivas")

        fornecedor = Fornecedor.objects.create(nome="Fornecedor A", email="fornecedor@exemplo.com", telefone="123456789", cnpj="00.000.000/0000-00", tipo_produto=tipo_produto)

        # Usando uma imagvem ficticia
        fake_image = cls.create_fake_image()


        cls.camiseta = Camiseta.objects.create(
            tipo_produto=tipo_produto,
            time="flamengo",
            liga="Brasileirão",
            temporada="2024",
            estilo="away",
            cor_principal="preto",
            patrocinador="Patrocinador X",
            marca="Marca Y",
            preco_custo=150.00,
            imagem = fake_image,
            fornecedor=fornecedor
        )

    def test_produto_view_success(self): # Teste 3
        # Criando a URL com os parâmetros
        url = reverse('produto', args=[self.camiseta.time, self.camiseta.estilo, self.camiseta.temporada])
        
        # Simulando a requisição GET para a URL
        response = self.client.get(url)
        
        # Verificando se a resposta tem o código de status 200
        self.assertEqual(response.status_code, 200)
        
        # Verificando se o nome da camiseta está no contexto da resposta
        self.assertContains(response, self.camiseta.time)
        self.assertContains(response, self.camiseta.estilo)
        
        # Verificando se os dados da camiseta estão sendo renderizados corretamente
        self.assertTemplateUsed(response, 'produto.html')

    def test_produto_view_not_found(self): # Teste 4
        # Testando um caso onde a camiseta não é encontrada
        url = reverse('produto', args=['inexistente', 'estiloX', '2025'])
        
        # Simulando a requisição GET para a URL
        response = self.client.get(url)
        
        # Verificando se o código de status é 404 (não encontrado)
        self.assertEqual(response.status_code, 404)