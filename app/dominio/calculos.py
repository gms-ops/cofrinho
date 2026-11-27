import math
from decimal import ROUND_CEILING, Decimal

_CENTAVOS = Decimal("0.01")
_DIAS_POR_MES = 30


def calcular_progresso(meta):
    """Percentual poupado (0 a 100), com uma casa decimal."""
    percentual = meta.saldo / meta.alvo * 100
    return float(round(min(percentual, Decimal(100)), 1))


def calcular_faltante(meta):
    return max(meta.alvo - meta.saldo, Decimal("0.00"))


def meses_restantes(meta, hoje):
    """Meses até o prazo, arredondando para cima; no mínimo 1."""
    dias = (meta.prazo - hoje).days
    return max(1, math.ceil(dias / _DIAS_POR_MES))


def calcular_mensalidade(meta, hoje):
    """Quanto poupar por mês para atingir a meta no prazo."""
    if meta.concluida:
        return Decimal("0.00")
    mensal = calcular_faltante(meta) / meses_restantes(meta, hoje)
    return mensal.quantize(_CENTAVOS, rounding=ROUND_CEILING)


def esta_atrasada(meta, hoje):
    return not meta.concluida and meta.prazo < hoje
