from unittest.mock import patch

import pytest


@pytest.mark.usefixtures("app", "client", "database")
class TestConsorcio:
    @patch("services.consorcio_service.ConsorcioService.get_consorcios")
    def test_get_route(self, mock_get, client, database):
        """Test that GET /consorcio route returns the correct list of consórcios."""
        mock_get.return_value = [
            {
                "ID": 107,
                "NOME": "MILENIO TRANSPORTES",
                "CONCESSIONARIA": "CONSORCIO PAMPULHA",
            }
        ]

        response = client.get("/consorcio")
        assert response.status_code == 200
        data = response.get_json()
        assert "consorcios" in data
        assert len(data["consorcios"]) == 1
        assert data["consorcios"][0]["ID"] == 107

    @patch("services.consorcio_service.ConsorcioService.get_consorcios")
    def test_get_v1_route(self, mock_get, client, database):
        """Test that GET /v1/consorcio route returns the correct list of consórcios."""
        mock_get.return_value = [
            {
                "ID": 107,
                "NOME": "MILENIO TRANSPORTES",
                "CONCESSIONARIA": "CONSORCIO PAMPULHA",
            }
        ]

        response = client.get("/v1/consorcio")
        assert response.status_code == 200
        data = response.get_json()
        assert "consorcios" in data
        assert len(data["consorcios"]) == 1
        assert data["consorcios"][0]["ID"] == 107

    @patch("services.consorcio_service.ConsorcioService.insert_consorcios")
    def test_insert_route(self, mock_insert, client, database):
        """Test that POST /consorcio route inserts consórcios successfully."""
        mock_insert.return_value = 1

        payload = [
            {
                "ID": 107,
                "NOME": "MILENIO TRANSPORTES",
                "CONCESSIONARIA": "CONSORCIO PAMPULHA",
            }
        ]

        response = client.post("/consorcio", json=payload)
        assert response.status_code == 201
        data = response.get_json()
        assert data["message"] == "Consórcios inseridos com sucesso"
        assert data["counter"] == 1

    @patch("services.consorcio_service.ConsorcioService.update_consorcios")
    def test_patch_route(self, mock_update, client, database):
        """Test that PATCH /consorcio route updates consórcios successfully."""
        mock_update.return_value = 1

        payload = [
            {
                "ID": 107,
                "NOME": "MILENIO TRANSPORTES ALTERADO",
                "CONCESSIONARIA": "CONSORCIO PAMPULHA",
            }
        ]

        response = client.patch("/consorcio", json=payload)
        assert response.status_code == 200
        data = response.get_json()
        assert data["message"] == "Consórcios atualizados com sucesso"
        assert data["counter"] == 1

    @patch("services.consorcio_service.ConsorcioService.update_consorcios")
    def test_put_route(self, mock_update, client, database):
        """Test that PUT /consorcio route updates consórcios successfully."""
        mock_update.return_value = 1

        payload = [
            {
                "ID": 107,
                "NOME": "MILENIO TRANSPORTES ALTERADO",
                "CONCESSIONARIA": "CONSORCIO PAMPULHA",
            }
        ]

        response = client.put("/consorcio", json=payload)
        assert response.status_code == 200
        data = response.get_json()
        assert data["message"] == "Consórcios atualizados com sucesso"
        assert data["counter"] == 1

    @patch("services.consorcio_service.ConsorcioService.delete_consorcio")
    def test_delete_route(self, mock_delete, client, database):
        """Test that DELETE /consorcio/<id> route deletes a consórcio successfully."""
        mock_delete.return_value = 1

        response = client.delete("/consorcio/107")
        assert response.status_code == 200
        data = response.get_json()
        assert data["message"] == "Consórcio deletado com sucesso"
        assert data["counter"] == 1

    def test_insert_route_validation_error(self, client, database):
        """Test that Pydantic/SpecTree validation returns 422 on invalid payload."""
        # Payload missing required NOME field
        invalid_payload = [
            {
                "ID": 107,
                "CONCESSIONARIA": "CONSORCIO PAMPULHA",
            }
        ]
        response = client.post("/consorcio", json=invalid_payload)
        assert response.status_code == 422
        data = response.get_json()
        assert data["error"] == "ValidationError"
        assert "NOME" in data["message"]
