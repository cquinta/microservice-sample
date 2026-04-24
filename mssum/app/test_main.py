from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_read_root():
    """Testa se o endpoint raiz está respondendo corretamente."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Microsserviço de Soma"}

def test_operacao_subtracao_sucesso():
    """Testa a operação de subtração com valores válidos."""
    response = client.post("/sum", json={"a": 10, "b": 4})
    assert response.status_code == 200
    assert response.json() == {"result": 14, "op": "sum"}

def test_operacao_subtracao_invalida():
    """Testa a operação de soma com tipos de dados inválidos (ex: string em vez de int)."""
    response = client.post("/sum", json={"a": "dez", "b": 4})
    assert response.status_code == 422