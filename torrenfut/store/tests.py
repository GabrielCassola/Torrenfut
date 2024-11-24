def test_home_status_code(client):
    resposta = client.get('/store')
    assert resposta.status_code == 301