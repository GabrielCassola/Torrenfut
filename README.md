# Torrenfut | E-Commerce de artigos esportivos
# *Trabalho da matéria de implementação de sistemas de informação*  

## Tecnologias Utilizadas:
- Python 3.12.3
- Django 5.1.2

## Instalação
1. **Clone o repositório:**

   ```bash 
   git clone https://github.com/GabrielCassola/Torrenfut.git
   ```

2. **Crie e ative um ambiente virtual:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate     # Windows
   ```   
3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```
   **Executar os testes unitários**

   ```bash
    pytest torrent/
      ```
   **Executar cobertura de teste**

   ```bash
    pytest torrenfut/ --cov=torrenfut
      ```
   **Executar cobertura de testes**

   ```bash
    pytest torrenfut/ --cov=torrenfut --cov-fail-under=taxa-minima
      ```

4. **Inicie o servidor:**

   ```bash
   python manage.py runserver
   ```

   O servidor estará disponível em http://127.0.0.1:8000/store.
