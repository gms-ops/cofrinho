from datetime import date
from decimal import Decimal

from app.dominio.formatacao import formatar_data, formatar_moeda, formatar_percentual


def test_moeda_simples_tem_duas_casas():
    assert formatar_moeda(Decimal("10")) == "R$ 10,00"


def test_moeda_usa_ponto_nos_milhares_e_virgula_nos_centavos():
    assert formatar_moeda(Decimal("1234.5")) == "R$ 1.234,50"


def test_moeda_com_milhoes():
    assert formatar_moeda(Decimal("1234567.89")) == "R$ 1.234.567,89"


def test_moeda_zero():
    assert formatar_moeda(Decimal("0")) == "R$ 0,00"


def test_moeda_negativa_coloca_sinal_antes_do_simbolo():
    assert formatar_moeda(Decimal("-5")) == "-R$ 5,00"


def test_moeda_aceita_inteiro():
    assert formatar_moeda(7) == "R$ 7,00"


def test_moeda_arredonda_meio_centavo_para_cima():
    assert formatar_moeda(Decimal("0.005")) == "R$ 0,01"


def test_data_usa_formato_dia_mes_ano():
    assert formatar_data(date(2026, 3, 5)) == "05/03/2026"


def test_percentual_inteiro_nao_mostra_casas_decimais():
    assert formatar_percentual(50.0) == "50%"


def test_percentual_fracionado_usa_virgula():
    assert formatar_percentual(33.3) == "33,3%"


def test_percentual_zero():
    assert formatar_percentual(0) == "0%"


def test_percentual_cem():
    assert formatar_percentual(100.0) == "100%"
