from datetime import date, timedelta

import pytest

from app.dominio.meta import criar_meta, depositar

HOJE = date(2026, 1, 1)


@pytest.fixture
def hoje():
    return HOJE


@pytest.fixture
def nova_meta():
    """Fábrica de metas: prazo em `dias` a partir de HOJE e saldo inicial opcional."""

    def _fabricar(nome="Viagem", alvo=1000, dias=90, saldo=0):
        meta = criar_meta(nome, alvo, HOJE + timedelta(days=dias), HOJE)
        return depositar(meta, saldo) if saldo else meta

    return _fabricar
