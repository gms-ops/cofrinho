from dataclasses import dataclass, replace
from datetime import date
from decimal import Decimal
from typing import Optional

from .erros import SaldoInsuficiente
from .validacao import validar_nome, validar_prazo, validar_valor

ZERO = Decimal("0.00")


@dataclass(frozen=True)
class Meta:
    nome: str
    alvo: Decimal
    prazo: date
    saldo: Decimal = ZERO
    id: Optional[int] = None

    @property
    def concluida(self):
        return self.saldo >= self.alvo


def criar_meta(nome, alvo, prazo, hoje=None):
    hoje = hoje or date.today()
    return Meta(
        nome=validar_nome(nome),
        alvo=validar_valor(alvo),
        prazo=validar_prazo(prazo, hoje),
    )


def editar_meta(meta, nome=None, alvo=None, prazo=None, hoje=None):
    hoje = hoje or date.today()
    mudancas = {}
    if nome is not None:
        mudancas["nome"] = validar_nome(nome)
    if alvo is not None:
        mudancas["alvo"] = validar_valor(alvo)
    if prazo is not None:
        mudancas["prazo"] = validar_prazo(prazo, hoje)
    return replace(meta, **mudancas)


def depositar(meta, valor):
    return replace(meta, saldo=meta.saldo + validar_valor(valor))


def retirar(meta, valor):
    valor = validar_valor(valor)
    if valor > meta.saldo:
        raise SaldoInsuficiente("Saldo insuficiente para retirar este valor.")
    return replace(meta, saldo=meta.saldo - valor)
