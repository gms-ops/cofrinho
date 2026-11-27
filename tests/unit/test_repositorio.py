from dataclasses import replace

import pytest

from app.dominio.erros import MetaNaoEncontrada
from app.dominio.meta import depositar
from app.repositorio import RepositorioMetas


@pytest.fixture
def repo():
    return RepositorioMetas()


def test_adicionar_atribui_ids_sequenciais(repo, nova_meta):
    primeira = repo.adicionar(nova_meta("Viagem"))
    segunda = repo.adicionar(nova_meta("Notebook"))
    assert (primeira.id, segunda.id) == (1, 2)


def test_obter_devolve_a_meta_adicionada(repo, nova_meta):
    salva = repo.adicionar(nova_meta("Viagem"))
    assert repo.obter(salva.id) == salva


def test_obter_id_inexistente_falha(repo):
    with pytest.raises(MetaNaoEncontrada):
        repo.obter(99)


def test_listar_repositorio_vazio_devolve_lista_vazia(repo):
    assert repo.listar() == []


def test_listar_devolve_metas_em_ordem_de_criacao(repo, nova_meta):
    repo.adicionar(nova_meta("Viagem"))
    repo.adicionar(nova_meta("Notebook"))
    assert [m.nome for m in repo.listar()] == ["Viagem", "Notebook"]


def test_atualizar_substitui_a_meta_guardada(repo, nova_meta):
    salva = repo.adicionar(nova_meta("Viagem"))
    repo.atualizar(depositar(salva, 100))
    assert repo.obter(salva.id).saldo == 100


def test_atualizar_meta_inexistente_falha(repo, nova_meta):
    with pytest.raises(MetaNaoEncontrada):
        repo.atualizar(replace(nova_meta(), id=42))


def test_remover_apaga_a_meta(repo, nova_meta):
    salva = repo.adicionar(nova_meta())
    repo.remover(salva.id)
    assert repo.listar() == []


def test_remover_meta_inexistente_falha(repo):
    with pytest.raises(MetaNaoEncontrada):
        repo.remover(1)


def test_ids_removidos_nao_sao_reaproveitados(repo, nova_meta):
    repo.adicionar(nova_meta("Viagem"))
    segunda = repo.adicionar(nova_meta("Notebook"))
    repo.remover(segunda.id)
    assert repo.adicionar(nova_meta("Moto nova")).id == 3


def test_dados_sobrevivem_a_um_novo_repositorio_no_mesmo_arquivo(tmp_path, nova_meta):
    arquivo = tmp_path / "dados.json"
    original = RepositorioMetas(arquivo)
    salva = original.adicionar(nova_meta("Viagem", saldo=250))
    reaberto = RepositorioMetas(arquivo)
    assert reaberto.listar() == [salva]


def test_contador_de_ids_tambem_e_persistido(tmp_path, nova_meta):
    arquivo = tmp_path / "dados.json"
    original = RepositorioMetas(arquivo)
    original.adicionar(nova_meta("Viagem"))
    reaberto = RepositorioMetas(arquivo)
    assert reaberto.adicionar(nova_meta("Notebook")).id == 2
