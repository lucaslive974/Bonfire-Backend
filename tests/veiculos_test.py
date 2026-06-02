import pytest
import json
from unittest.mock import patch


@pytest.mark.usefixtures("app", "client", "database")
class TestVeiculos:
    @patch("handlers.veiculos.getVeiculos")
    def test_get_route(self, mock_get, client, database):
        """Testa se a rota GET /veiculos retorna 200 e a lista correta"""
        mock_get.return_value = (
            '[{"NUM_VEIC": 1111, "IDN_PLAC_VEIC": "OPC123", "VEIC_ATIV_EMPR": false}]'
        )

        response = client.get("/veiculos")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "veiculos" in data
        assert len(data["veiculos"]) == 1
        assert data["veiculos"][0]["NUM_VEIC"] == 1111

    @patch("handlers.veiculos.insertVeiculos")
    def test_insert_route(self, mock_insert, client, database):
        """Testa a rota POST /veiculos"""
        mock_insert.return_value = 1

        payload = [
            {"NUM_VEIC": 1111, "IDN_PLAC_VEIC": "OPC123", "VEIC_ATIV_EMPR": True}
        ]

        response = client.post("/veiculos", json=payload)

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["message"] == "Veículos inseridos com sucesso"
        assert data["counter"] == 1

    @patch("handlers.veiculos.updateVeiculos")
    def test_update_route(self, mock_update, client, database):
        """Testa a rota PATCH /veiculos"""
        mock_update.return_value = 1

        payload = [
            {"NUM_VEIC": 1111, "IDN_PLAC_VEIC": "OPC123", "VEIC_ATIV_EMPR": False}
        ]

        response = client.patch("/veiculos", json=payload)

        assert response.status_code == 202
        data = json.loads(response.data)
        assert data["message"] == "Veículos atualizados com sucesso"
        assert data["counter"] == 1

