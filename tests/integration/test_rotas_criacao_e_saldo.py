def pagina(resposta):
    return resposta.get_data(as_text=True)


def criar_viagem(client, alvo="1000"):
    return client.post(
        "/metas",
        data={"nome": "Viagem", "alvo": alvo, "prazo": "2026-12-31"},
        follow_redirects=True,
    )


def test_pagina_inicial_sem_metas_convida_a_criar_a_primeira(client):
    assert "Nenhuma meta" in pagina(client.get("/"))


def test_criar_meta_mostra_confirmacao_e_a_meta_na_lista(client):
    html = pagina(criar_viagem(client))
    assert "Meta criada." in html and "Meta Viagem" in html


def test_criar_meta_sem_nome_mostra_erro_e_nao_cria(client):
    resposta = client.post(
        "/metas", data={"nome": "", "alvo": "10", "prazo": "2026-12-31"}, follow_redirects=True)
    assert "Informe o nome da meta." in pagina(resposta)
    assert "Nenhuma meta" in pagina(resposta)


def test_deposito_atualiza_o_progresso(client):
    criar_viagem(client)
    html = pagina(client.post("/metas/1/deposito", data={"valor": "500"}, follow_redirects=True))
    assert 'aria-valuenow="50"' in html and "R$ 500,00 de R$ 1.000,00" in html


def test_deposito_invalido_mostra_erro(client):
    criar_viagem(client)
    html = pagina(client.post("/metas/1/deposito", data={"valor": "-1"}, follow_redirects=True))
    assert "maior que zero" in html


def test_deposito_que_completa_a_meta_mostra_parabens(client):
    criar_viagem(client, alvo="100")
    html = pagina(client.post("/metas/1/deposito", data={"valor": "100"}, follow_redirects=True))
    assert "Parabéns" in html and "Meta alcançada" in html


def test_retirada_maior_que_o_saldo_mostra_erro(client):
    criar_viagem(client)
    html = pagina(client.post("/metas/1/retirada", data={"valor": "10"}, follow_redirects=True))
    assert "Saldo insuficiente" in html


def test_retirada_valida_reduz_o_saldo(client):
    criar_viagem(client)
    client.post("/metas/1/deposito", data={"valor": "300"})
    html = pagina(client.post("/metas/1/retirada", data={"valor": "100"}, follow_redirects=True))
    assert "R$ 200,00 de R$ 1.000,00" in html
