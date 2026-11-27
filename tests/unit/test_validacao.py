from datetime import date, datetime
from decimal import Decimal

import pytest

from app.dominio.erros import ErroValidacao
from app.dominio.validacao import validar_nome, validar_prazo, validar_valor

HOJE = date(2026, 1, 1)


# ---------- nome ----------
def test_nome_valido_e_devolvido_sem_espacos_nas_pontas():
    assert validar_nome("  Viagem  ") == "Viagem"


def test_nome_com_espacos_repetidos_no_meio_e_normalizado():
    assert validar_nome("Viagem   para  Paris") == "Viagem para Paris"


def test_nome_vazio_e_rejeitado():
    with pytest.raises(ErroValidacao, match="Informe o nome"):
        validar_nome("")


def test_nome_so_com_espacos_e_rejeitado():
    with pytest.raises(ErroValidacao, match="Informe o nome"):
        validar_nome("     ")


def test_nome_que_nao_e_texto_e_rejeitado():
    with pytest.raises(ErroValidacao, match="Informe o nome"):
        validar_nome(None)


def test_nome_com_duas_letras_e_rejeitado_por_ser_curto():
    with pytest.raises(ErroValidacao, match="pelo menos 3"):
        validar_nome("ab")


def test_nome_com_exatamente_tres_letras_e_aceito():
    assert validar_nome("abc") == "abc"


def test_nome_com_cinquenta_letras_e_aceito():
    assert len(validar_nome("a" * 50)) == 50


def test_nome_com_cinquenta_e_uma_letras_e_rejeitado():
    with pytest.raises(ErroValidacao, match="no máximo 50"):
        validar_nome("a" * 51)


# ---------- valor ----------
def test_valor_inteiro_vira_decimal_com_centavos():
    assert validar_valor(100) == Decimal("100.00")


def test_valor_em_texto_com_virgula_e_aceito():
    assert validar_valor("10,5") == Decimal("10.50")


def test_valor_em_texto_com_ponto_e_aceito():
    assert validar_valor("10.5") == Decimal("10.50")


def test_valor_float_nao_sofre_erro_de_ponto_flutuante():
    assert validar_valor(19.9) == Decimal("19.90")


def test_valor_e_arredondado_para_cima_na_terceira_casa_quando_metade():
    assert validar_valor("10.005") == Decimal("10.01")


def test_valor_zero_e_rejeitado():
    with pytest.raises(ErroValidacao, match="maior que zero"):
        validar_valor(0)


def test_valor_negativo_e_rejeitado():
    with pytest.raises(ErroValidacao, match="maior que zero"):
        validar_valor("-5")


def test_valor_nao_numerico_e_rejeitado():
    with pytest.raises(ErroValidacao, match="inválido"):
        validar_valor("abc")


def test_valor_vazio_e_rejeitado():
    with pytest.raises(ErroValidacao, match="Informe um valor"):
        validar_valor("  ")


def test_valor_infinito_e_rejeitado():
    with pytest.raises(ErroValidacao, match="inválido"):
        validar_valor("inf")


def test_valor_acima_do_limite_e_rejeitado():
    with pytest.raises(ErroValidacao, match="valor máximo"):
        validar_valor("10000000.01")


def test_valor_exatamente_no_limite_e_aceito():
    assert validar_valor("10000000") == Decimal("10000000.00")


# ---------- prazo ----------
def test_prazo_futuro_como_data_e_aceito():
    assert validar_prazo(date(2026, 6, 30), HOJE) == date(2026, 6, 30)


def test_prazo_em_texto_iso_e_convertido_para_data():
    assert validar_prazo("2026-06-30", HOJE) == date(2026, 6, 30)


def test_prazo_com_datetime_e_convertido_para_data():
    assert validar_prazo(datetime(2026, 6, 1, 10, 30), HOJE) == date(2026, 6, 1)


def test_prazo_igual_a_hoje_e_rejeitado():
    with pytest.raises(ErroValidacao, match="futura"):
        validar_prazo(HOJE, HOJE)


def test_prazo_no_passado_e_rejeitado():
    with pytest.raises(ErroValidacao, match="futura"):
        validar_prazo("2025-12-31", HOJE)


def test_prazo_com_formato_brasileiro_e_rejeitado_como_invalido():
    with pytest.raises(ErroValidacao, match="inválida"):
        validar_prazo("31/12/2026", HOJE)


def test_prazo_vazio_e_rejeitado():
    with pytest.raises(ErroValidacao, match="Informe o prazo"):
        validar_prazo("", HOJE)


def test_prazo_nulo_e_rejeitado():
    with pytest.raises(ErroValidacao, match="Informe o prazo"):
        validar_prazo(None, HOJE)
