import pytest

from app.dominio.erros import ErroValidacao
from app.dominio.validacao import validar_valor


def test_valor_que_arredonda_para_zero_e_rejeitado():
    with pytest.raises(ErroValidacao, match="maior que zero"):
        validar_valor("0.001")


def test_menor_valor_aceito_e_um_centavo():
    assert str(validar_valor("0.01")) == "0.01"


def test_valor_que_arredonda_para_um_centavo_e_aceito():
    assert str(validar_valor("0.005")) == "0.01"
