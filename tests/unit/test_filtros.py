import pytest

from app.dominio.erros import ErroValidacao
from app.dominio.filtros import buscar_por_nome, filtrar_por_status, ordenar_metas


@pytest.fixture
def metas(nova_meta):
    viagem = nova_meta("Viagem", alvo=1000, dias=60, saldo=1000)   # concluída, 100%
    notebook = nova_meta("notebook", alvo=4000, dias=30, saldo=1000)  # 25%
    moto = nova_meta("Moto nova", alvo=10000, dias=200, saldo=5000)  # 50%
    return [viagem, notebook, moto]


def nomes(lista):
    return [m.nome for m in lista]


def test_filtrar_todas_devolve_todas_as_metas(metas):
    assert nomes(filtrar_por_status(metas, "todas")) == ["Viagem", "notebook", "Moto nova"]


def test_filtrar_andamento_exclui_as_concluidas(metas):
    assert nomes(filtrar_por_status(metas, "andamento")) == ["notebook", "Moto nova"]


def test_filtrar_concluidas_devolve_so_as_concluidas(metas):
    assert nomes(filtrar_por_status(metas, "concluidas")) == ["Viagem"]


def test_filtrar_com_situacao_desconhecida_falha(metas):
    with pytest.raises(ErroValidacao, match="Situação inválida"):
        filtrar_por_status(metas, "arquivadas")


def test_buscar_ignora_maiusculas_e_minusculas(metas):
    assert nomes(buscar_por_nome(metas, "NOTEBOOK")) == ["notebook"]


def test_buscar_aceita_trecho_do_nome(metas):
    assert nomes(buscar_por_nome(metas, "nova")) == ["Moto nova"]


def test_buscar_com_termo_vazio_devolve_todas(metas):
    assert len(buscar_por_nome(metas, "  ")) == 3


def test_buscar_sem_correspondencia_devolve_lista_vazia(metas):
    assert buscar_por_nome(metas, "carro") == []


def test_ordenar_por_nome_ignora_maiusculas(metas):
    assert nomes(ordenar_metas(metas, "nome")) == ["Moto nova", "notebook", "Viagem"]


def test_ordenar_por_prazo_coloca_o_mais_proximo_primeiro(metas):
    assert nomes(ordenar_metas(metas, "prazo")) == ["notebook", "Viagem", "Moto nova"]


def test_ordenar_por_progresso_coloca_o_maior_primeiro(metas):
    assert nomes(ordenar_metas(metas, "progresso")) == ["Viagem", "Moto nova", "notebook"]


def test_ordenar_com_criterio_desconhecido_falha(metas):
    with pytest.raises(ErroValidacao, match="Ordenação inválida"):
        ordenar_metas(metas, "cor")


def test_ordenar_nao_modifica_a_lista_original(metas):
    ordenar_metas(metas, "nome")
    assert nomes(metas) == ["Viagem", "notebook", "Moto nova"]
