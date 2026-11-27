def test_remover_meta_inexistente_devolve_404(client):
    assert client.post("/metas/99/remover").status_code == 404


def test_retirar_de_meta_inexistente_devolve_404(client):
    assert client.post("/metas/99/retirada", data={"valor": "1"}).status_code == 404


def test_pagina_404_tem_link_para_voltar(client):
    html = client.get("/metas/99/editar").get_data(as_text=True)
    assert "Voltar para suas metas" in html
