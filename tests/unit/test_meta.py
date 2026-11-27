from datetime import date, timedelta
from decimal import Decimal

import pytest

from app.dominio.erros import ErroValidacao, SaldoInsuficiente
from app.dominio.meta import criar_meta, depositar, editar_meta, retirar

HOJE = date(2026, 1, 1)
PRAZO = date(2026, 12, 31)


# ---------- criação ----------
def test_meta_nova_comeca_com_saldo_zero():
    meta = criar_meta("Viagem", 1000, PRAZO, HOJE)
    assert meta.saldo == Decimal("0.00")


def test_meta_nova_guarda_nome_normalizado():
    meta = criar_meta("  Viagem  ", 1000, PRAZO, HOJE)
    assert meta.nome == "Viagem"


def test_meta_nova_converte_alvo_em_texto_para_decimal():
    meta = criar_meta("Viagem", "1500,50", PRAZO, HOJE)
    assert meta.alvo == Decimal("1500.50")


def test_meta_nova_nao_esta_concluida():
    assert not criar_meta("Viagem", 1000, PRAZO, HOJE).concluida


def test_meta_nova_ainda_nao_tem_id():
    assert criar_meta("Viagem", 1000, PRAZO, HOJE).id is None


def test_criar_meta_com_nome_invalido_falha():
    with pytest.raises(ErroValidacao):
        criar_meta("", 1000, PRAZO, HOJE)


def test_criar_meta_com_alvo_zero_falha():
    with pytest.raises(ErroValidacao, match="maior que zero"):
        criar_meta("Viagem", 0, PRAZO, HOJE)


def test_criar_meta_com_prazo_passado_falha():
    with pytest.raises(ErroValidacao, match="futura"):
        criar_meta("Viagem", 1000, HOJE - timedelta(days=1), HOJE)


# ---------- edição ----------
def test_editar_nome_mantem_os_demais_campos(nova_meta):
    meta = nova_meta(alvo=1000, saldo=200)
    editada = editar_meta(meta, nome="Viagem à praia", hoje=HOJE)
    assert (editada.nome, editada.alvo, editada.prazo, editada.saldo) == (
        "Viagem à praia", meta.alvo, meta.prazo, meta.saldo)


def test_editar_alvo_atualiza_somente_o_alvo(nova_meta):
    editada = editar_meta(nova_meta(), alvo="2000", hoje=HOJE)
    assert editada.alvo == Decimal("2000.00")


def test_editar_prazo_atualiza_somente_o_prazo(nova_meta):
    editada = editar_meta(nova_meta(), prazo="2026-11-30", hoje=HOJE)
    assert editada.prazo == date(2026, 11, 30)


def test_editar_sem_argumentos_devolve_meta_equivalente(nova_meta):
    meta = nova_meta()
    assert editar_meta(meta, hoje=HOJE) == meta


def test_editar_nao_altera_o_saldo(nova_meta):
    meta = nova_meta(saldo=300)
    assert editar_meta(meta, alvo=5000, hoje=HOJE).saldo == Decimal("300.00")


def test_editar_com_valor_invalido_falha(nova_meta):
    with pytest.raises(ErroValidacao):
        editar_meta(nova_meta(), alvo="abc", hoje=HOJE)


def test_editar_com_prazo_passado_falha(nova_meta):
    with pytest.raises(ErroValidacao, match="futura"):
        editar_meta(nova_meta(), prazo="2025-01-01", hoje=HOJE)


# ---------- depósitos ----------
def test_deposito_aumenta_o_saldo(nova_meta):
    assert depositar(nova_meta(), 250).saldo == Decimal("250.00")


def test_depositos_sucessivos_se_acumulam(nova_meta):
    meta = depositar(depositar(nova_meta(), 100), "50,25")
    assert meta.saldo == Decimal("150.25")


def test_deposito_nao_altera_a_meta_original(nova_meta):
    meta = nova_meta()
    depositar(meta, 100)
    assert meta.saldo == Decimal("0.00")


def test_deposito_zero_e_rejeitado(nova_meta):
    with pytest.raises(ErroValidacao):
        depositar(nova_meta(), 0)


def test_deposito_negativo_e_rejeitado(nova_meta):
    with pytest.raises(ErroValidacao):
        depositar(nova_meta(), -10)


def test_meta_conclui_ao_atingir_exatamente_o_alvo(nova_meta):
    assert depositar(nova_meta(alvo=500), 500).concluida


def test_meta_conclui_quando_o_saldo_ultrapassa_o_alvo(nova_meta):
    assert depositar(nova_meta(alvo=500), 800).concluida


def test_meta_nao_conclui_um_centavo_antes_do_alvo(nova_meta):
    assert not depositar(nova_meta(alvo=500), "499.99").concluida


# ---------- retiradas ----------
def test_retirada_diminui_o_saldo(nova_meta):
    assert retirar(nova_meta(saldo=500), 200).saldo == Decimal("300.00")


def test_retirada_de_todo_o_saldo_zera_a_meta(nova_meta):
    assert retirar(nova_meta(saldo=500), 500).saldo == Decimal("0.00")


def test_retirada_maior_que_o_saldo_e_rejeitada(nova_meta):
    with pytest.raises(SaldoInsuficiente, match="Saldo insuficiente"):
        retirar(nova_meta(saldo=100), 100.01)


def test_retirada_em_meta_sem_saldo_e_rejeitada(nova_meta):
    with pytest.raises(SaldoInsuficiente):
        retirar(nova_meta(), 1)


def test_retirada_de_valor_zero_e_rejeitada(nova_meta):
    with pytest.raises(ErroValidacao, match="maior que zero"):
        retirar(nova_meta(saldo=100), 0)


def test_retirada_reabre_meta_que_estava_concluida(nova_meta):
    concluida = nova_meta(alvo=500, saldo=500)
    assert not retirar(concluida, 1).concluida
