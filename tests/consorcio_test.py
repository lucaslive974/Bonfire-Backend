from unittest.mock import MagicMock, patch

import pytest

from classes.Operadora import Operadora
from repositories.consorcio_repository import ConsorcioRepository
from services.consorcio_service import ConsorcioService


def test_consorcio_repository_get_by_ids():
    mock_db = MagicMock()
    repo = ConsorcioRepository(mock_db)

    existing_op = Operadora(
        ID=107, NOME="MILENIO TRANSPORTES", CONCESSIONARIA="CONSORCIO PAMPULHA"
    )
    mock_model = repo._to_model(existing_op)
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_model]

    result = repo.get_by_ids([107])
    assert len(result) == 1
    assert result[0].id == 107
    assert result[0].name == "MILENIO TRANSPORTES"
    assert result[0].concessionaire == "CONSORCIO PAMPULHA"


def test_consorcio_repository_update_bulk():
    mock_db = MagicMock()
    repo = ConsorcioRepository(mock_db)

    payload = [
        Operadora(ID=107, NOME="MILENIO", CONCESSIONARIA="PAMPULHA"),
        Operadora(ID=108, NOME="TORRES", CONCESSIONARIA="BHTRANS"),
    ]

    count = repo.update_bulk(payload)
    assert count == 2
    assert mock_db.merge.call_count == 2


def test_consorcio_service_update_consorcios():
    mock_db_manager = MagicMock()
    mock_session = mock_db_manager.session.return_value.__enter__.return_value
    mock_repo = mock_session.get_consorcio_repository.return_value

    existing_op = Operadora(ID=107, NOME="MILENIO", CONCESSIONARIA="PAMPULHA")
    mock_repo.get_by_ids.return_value = [existing_op]
    mock_repo.update_bulk.side_effect = lambda ops: len(ops)

    service = ConsorcioService(mock_db_manager)
    payload = [Operadora(ID=107, NOME="MILENIO ALTERADO")]

    count = service.update_consorcios(payload)
    assert count == 1
    mock_repo.get_by_ids.assert_called_once_with([107])
    mock_repo.update_bulk.assert_called_once()
    updated_op = mock_repo.update_bulk.call_args[0][0][0]
    assert updated_op.name == "MILENIO ALTERADO"
    assert updated_op.concessionaire == "PAMPULHA"


def test_consorcio_service_update_consorcios_empty():
    mock_db_manager = MagicMock()
    service = ConsorcioService(mock_db_manager)
    assert service.update_consorcios([]) == 0
    assert service.update_consorcios([Operadora(ID=None)]) == 0


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
