from fastapi.testclient import TestClient
from .config import Config

from app.main import app

client = TestClient(app)


def test_read_root():
    """Testa se o endpoint raiz está respondendo corretamente."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Microsserviço de Subtração"
    assert data["host"] == Config.HOST
    assert data["versão"] == Config.VERSION
    


def test_operacao_subtracao_sucesso():
    """Testa a operação de subtração com valores válidos."""
    response = client.post("/sub", json={"a": 10, "b": 4})
    assert response.status_code == 200
    assert response.json() == {"result": 6, "op": "sub"}


def test_operacao_subtracao_invalida():
    """Testa a operação de subtração com tipos de dados inválidos (ex: string em vez de int)."""
    response = client.post("/sub", json={"a": "dez", "b": 4})
    assert response.status_code == 422
