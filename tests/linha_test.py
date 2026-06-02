import pytest
import json
from unittest.mock import patch


@pytest.mark.usefixtures("app", "client", "database")
class TestLinha:
    @patch("handlers.linha.getLinha")
    def test_get_route(self, mock_get, client, database):
        """Testa se a rota GET /linha retorna a lista correta de linhas"""
        mock_get.return_value = '[{"COD_LINH": "61", "ID_OPERADORA": 107, "COMPARTILHADA": true, "LINH_ATIV_EMPR": true}]'

        response = client.get("/linha")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "linha" in data
        assert len(data["linha"]) == 1
        assert data["linha"][0]["COD_LINH"] == "61"

    @patch("handlers.linha.insertLinha")
    def test_insert_route(self, mock_insert, client, database):
        """Testa se a rota POST /linha insere linhas com sucesso"""
        mock_insert.return_value = 1

        payload = [
            {
                "COD_LINH": "61",
                "ID_OPERADORA": 107,
                "COMPARTILHADA": True,
                "LINH_ATIV_EMPR": True,
            }
        ]

        response = client.post("/linha", json=payload)
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["message"] == "linhas inseridas com sucesso"
        assert data["counter"] == 1

    @patch("handlers.linha.updateLinha")
    def test_update_route(self, mock_update, client, database):
        """Testa se a rota PATCH /linha atualiza linhas com sucesso"""
        mock_update.return_value = 1

        payload = [
            {
                "COD_LINH": "61",
                "ID_OPERADORA": 107,
                "COMPARTILHADA": False,
                "LINH_ATIV_EMPR": True,
            }
        ]

        response = client.patch("/linha", json=payload)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["message"] == "linha atualizada com sucesso"
        assert data["counter"] == 1

