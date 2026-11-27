from datetime import date, datetime
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

from .erros import ErroValidacao

NOME_MIN = 3
NOME_MAX = 50
VALOR_MAX = Decimal("10000000")
_CENTAVOS = Decimal("0.01")


def validar_nome(nome):
    if not isinstance(nome, str) or not nome.strip():
        raise ErroValidacao("Informe o nome da meta.")
    limpo = " ".join(nome.split())
    if len(limpo) < NOME_MIN:
        raise ErroValidacao(f"O nome precisa ter pelo menos {NOME_MIN} letras.")
    if len(limpo) > NOME_MAX:
        raise ErroValidacao(f"O nome pode ter no máximo {NOME_MAX} letras.")
    return limpo


def validar_valor(valor):
    if isinstance(valor, str):
        texto = valor.strip().replace(",", ".")
        if not texto:
            raise ErroValidacao("Informe um valor.")
        valor = texto
    try:
        numero = Decimal(str(valor))
    except InvalidOperation:
        raise ErroValidacao("Valor inválido. Use apenas números, como 150,50.")
    if not numero.is_finite():
        raise ErroValidacao("Valor inválido. Use apenas números, como 150,50.")
    if numero <= 0:
        raise ErroValidacao("O valor deve ser maior que zero.")
    if numero > VALOR_MAX:
        raise ErroValidacao("O valor máximo é R$ 10.000.000,00.")
    return numero.quantize(_CENTAVOS, rounding=ROUND_HALF_UP)


def validar_prazo(prazo, hoje):
    if isinstance(prazo, str):
        texto = prazo.strip()
        if not texto:
            raise ErroValidacao("Informe o prazo da meta.")
        try:
            prazo = date.fromisoformat(texto)
        except ValueError:
            raise ErroValidacao("Data inválida. Use o formato AAAA-MM-DD.")
    if isinstance(prazo, datetime):
        prazo = prazo.date()
    if not isinstance(prazo, date):
        raise ErroValidacao("Informe o prazo da meta.")
    if prazo <= hoje:
        raise ErroValidacao("O prazo deve ser uma data futura.")
    return prazo
