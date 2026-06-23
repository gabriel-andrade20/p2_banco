from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def client():
    with patch("app.database.MongoClient") as mock_mongo:
        mock_collection = MagicMock()
        mock_collection.find.return_value = [
            {
                "id": "abc-123",
                "nome_cliente": "João",
                "nome_produto": "Teclado",
                "quantidade": 1,
                "status": "PENDENTE",
            }
        ]
        mock_mongo.return_value.__getitem__.return_value.__getitem__.return_value = mock_collection

        import importlib
        import app.database as db_module
        db_module.colecao_pedidos = mock_collection

        from app.main import app
        yield TestClient(app)


def test_criar_pedido(client):
    with patch("app.routes.pedidos.publicar_rabbitmq"), patch(
        "app.routes.pedidos.publicar_kafka"
    ):
        resposta = client.post(
            "/pedidos/",
            json={"nome_cliente": "Maria", "nome_produto": "Mouse", "quantidade": 2},
        )
        assert resposta.status_code == 201
        corpo = resposta.json()
        assert corpo["nome_cliente"] == "Maria"
        assert corpo["nome_produto"] == "Mouse"
        assert corpo["quantidade"] == 2
        assert corpo["status"] == "PENDENTE"
        assert "id" in corpo


def test_listar_pedidos(client):
    resposta = client.get("/pedidos/")
    assert resposta.status_code == 200
    assert isinstance(resposta.json(), list)
