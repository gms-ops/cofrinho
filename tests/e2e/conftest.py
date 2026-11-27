import threading

import pytest
from werkzeug.serving import make_server

from app import create_app


@pytest.fixture
def url_base(tmp_path):
    """Sobe uma instância isolada da aplicação (dados em arquivo temporário)."""
    app = create_app({"TESTING": True, "ARQUIVO_DADOS": str(tmp_path / "dados.json")})
    servidor = make_server("127.0.0.1", 0, app)
    thread = threading.Thread(target=servidor.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{servidor.server_port}"
    servidor.shutdown()
    thread.join()
