from datetime import date

from app import create_app


def pagina(resposta):
    return resposta.get_data(as_text=True)


def criar_viagem(client, alvo="1000"):
    return client.post(
        "/metas",
        data={"nome": "Viagem", "alvo": alvo, "prazo": "2026-12-31"},
        follow_redirects=True,
    )


def test_remover_apaga_a_meta_da_lista(client):
    criar_viagem(client)
    html = pagina(client.post("/metas/1/remover", follow_redirects=True))
    assert "Meta removida." in html and "Nenhuma meta" in html


def test_formulario_de_edicao_vem_preenchido(client):
    criar_viagem(client)
    assert 'value="Viagem"' in pagina(client.get("/metas/1/editar"))


def test_editar_meta_altera_o_nome(client):
    criar_viagem(client)
    html = pagina(client.post(
        "/metas/1/editar",
        data={"nome": "Viagem ao Japão", "alvo": "1000", "prazo": "2026-12-31"},
        follow_redirects=True))
    assert "Meta atualizada." in html and "Meta Viagem ao Japão" in html


def test_editar_com_dado_invalido_permanece_na_tela_com_erro(client):
    criar_viagem(client)
    resposta = client.post(
        "/metas/1/editar", data={"nome": "Viagem", "alvo": "x", "prazo": "2026-12-31"})
    assert resposta.status_code == 200 and "inválido" in pagina(resposta)


def test_editar_meta_inexistente_devolve_404(client):
    assert client.get("/metas/99/editar").status_code == 404


def test_depositar_em_meta_inexistente_devolve_404(client):
    assert client.post("/metas/99/deposito", data={"valor": "1"}).status_code == 404


def test_busca_por_nome_filtra_a_lista(client):
    criar_viagem(client)
    client.post("/metas", data={"nome": "Notebook", "alvo": "4000", "prazo": "2026-12-31"})
    html = pagina(client.get("/?q=note"))
    assert "Meta Notebook" in html and "Meta Viagem" not in html


def test_filtro_de_situacao_invalido_mostra_erro_e_lista_tudo(client):
    criar_viagem(client)
    resposta = client.get("/?status=xyz", follow_redirects=True)
    assert resposta.status_code == 200 and "Situação inválida" in pagina(resposta)


def test_endpoint_de_saude_responde_ok(client):
    assert client.get("/saude").get_json() == {"status": "ok"}


def test_dados_persistem_entre_instancias_da_aplicacao(tmp_path):
    config = {"TESTING": True, "ARQUIVO_DADOS": str(tmp_path / "d.json"), "HOJE": date(2026, 1, 1)}
    criar_viagem(create_app(config).test_client())
    assert "Meta Viagem" in pagina(create_app(config).test_client().get("/"))
