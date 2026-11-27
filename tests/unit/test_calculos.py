from datetime import timedelta
from decimal import Decimal

from app.dominio.calculos import (calcular_faltante, calcular_mensalidade,
                                  calcular_progresso, esta_atrasada,
                                  meses_restantes)

from tests.conftest import HOJE


def test_progresso_e_zero_sem_depositos(nova_meta):
    assert calcular_progresso(nova_meta()) == 0


def test_progresso_e_50_quando_metade_foi_poupada(nova_meta):
    assert calcular_progresso(nova_meta(alvo=1000, saldo=500)) == 50


def test_progresso_e_limitado_a_100_quando_saldo_excede_o_alvo(nova_meta):
    assert calcular_progresso(nova_meta(alvo=100, saldo=150)) == 100


def test_progresso_tem_uma_casa_decimal(nova_meta):
    assert calcular_progresso(nova_meta(alvo=3, saldo=1)) == 33.3


def test_faltante_e_alvo_menos_saldo(nova_meta):
    assert calcular_faltante(nova_meta(alvo=1000, saldo=350)) == Decimal("650.00")


def test_faltante_nunca_e_negativo(nova_meta):
    assert calcular_faltante(nova_meta(alvo=100, saldo=150)) == Decimal("0.00")


def test_meses_restantes_para_noventa_dias_sao_tres(nova_meta):
    assert meses_restantes(nova_meta(dias=90), HOJE) == 3


def test_meses_restantes_arredonda_para_cima(nova_meta):
    assert meses_restantes(nova_meta(dias=91), HOJE) == 4


def test_meses_restantes_tem_minimo_de_um_para_prazo_amanha(nova_meta):
    assert meses_restantes(nova_meta(dias=1), HOJE) == 1


def test_meses_restantes_tem_minimo_de_um_quando_prazo_ja_venceu(nova_meta):
    meta = nova_meta(dias=10)
    assert meses_restantes(meta, HOJE + timedelta(days=30)) == 1


def test_mensalidade_divide_o_faltante_pelos_meses(nova_meta):
    assert calcular_mensalidade(nova_meta(alvo=900, dias=90), HOJE) == Decimal("300.00")


def test_mensalidade_considera_o_que_ja_foi_poupado(nova_meta):
    meta = nova_meta(alvo=900, dias=90, saldo=300)
    assert calcular_mensalidade(meta, HOJE) == Decimal("200.00")


def test_mensalidade_arredonda_centavos_para_cima(nova_meta):
    assert calcular_mensalidade(nova_meta(alvo=100, dias=90), HOJE) == Decimal("33.34")


def test_mensalidade_e_zero_quando_meta_ja_foi_alcancada(nova_meta):
    meta = nova_meta(alvo=100, saldo=100)
    assert calcular_mensalidade(meta, HOJE) == Decimal("0.00")


def test_meta_esta_atrasada_quando_prazo_passou_sem_concluir(nova_meta):
    meta = nova_meta(dias=10)
    assert esta_atrasada(meta, HOJE + timedelta(days=11))


def test_meta_concluida_nunca_esta_atrasada(nova_meta):
    meta = nova_meta(alvo=100, saldo=100, dias=10)
    assert not esta_atrasada(meta, HOJE + timedelta(days=11))


def test_meta_nao_esta_atrasada_no_proprio_dia_do_prazo(nova_meta):
    meta = nova_meta(dias=10)
    assert not esta_atrasada(meta, HOJE + timedelta(days=10))
