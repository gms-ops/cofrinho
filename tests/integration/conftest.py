from datetime import date

import pytest

from app import create_app


@pytest.fixture
def app():
    return create_app({"TESTING": True, "ARQUIVO_DADOS": None, "HOJE": date(2026, 1, 1)})


@pytest.fixture
def client(app):
    return app.test_client()
