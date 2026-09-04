from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from classes.Veiculo import Veiculo
from exceptions.CustomExceptions import ErrUpdateData
from repositories.veiculo_repository import VeiculoRepository
from services.veiculo_service import VeiculoService


def test_veiculo_model_without_dat_baix():
    veic = Veiculo(
        NUM_VEIC=1111,
        IDN_PLAC_VEIC="OPC123",
        VEIC_ATIV_EMPR=True,
        DAT_BAIX=None,
    )
    data = veic.to_dict()
    assert data == {
        "NUM_VEIC": 1111,
        "IDN_PLAC_VEIC": "OPC123",
        "VEIC_ATIV_EMPR": True,
        "DAT_BAIX": None,
    }


def test_veiculo_model_with_dat_baix():
    dt = datetime(2026, 8, 28, 10, 0, 0)
    veic = Veiculo(
        NUM_VEIC=2222,
        IDN_PLAC_VEIC="XYZ987",
        VEIC_ATIV_EMPR=False,
        DAT_BAIX=dt,
    )
    data = veic.to_dict()
    assert data == {
        "NUM_VEIC": 2222,
        "IDN_PLAC_VEIC": "XYZ987",
        "VEIC_ATIV_EMPR": False,
        "DAT_BAIX": "2026-08-28T10:00:00",
    }


def test_veiculo_repository_insert_bulk():
    mock_db = MagicMock()
    # Mock to ensure the exists check returns empty (no vehicles found)
    mock_db.query.return_value.filter.return_value.all.return_value = []
    repo = VeiculoRepository(mock_db)

    payload = [
        Veiculo(NUM_VEIC=1111, IDN_PLAC_VEIC="OPC123", VEIC_ATIV_EMPR=True),
        Veiculo(
            NUM_VEIC=2222,
            IDN_PLAC_VEIC="XYZ987",
            VEIC_ATIV_EMPR=False,
            DAT_BAIX="2026-08-28T10:00:00",
        ),
    ]

    count = repo.insert_bulk(payload)
    assert count == 2
    assert mock_db.add.call_count == 2


def test_veiculo_repository_update_bulk_deactivate():
    mock_db = MagicMock()
    repo = VeiculoRepository(mock_db)

    existing_veiculo = Veiculo(
        NUM_VEIC=1111,
        IDN_PLAC_VEIC="OPC123",
        VEIC_ATIV_EMPR=True,
        DAT_BAIX=None,
    )
    mock_model = repo._to_model(existing_veiculo)
    mock_db.query.return_value.filter.return_value.first.return_value = mock_model

    payload = [Veiculo(NUM_VEIC=1111, VEIC_ATIV_EMPR=False)]

    count = repo.update_bulk(payload)
    assert count == 1
    assert mock_model.VEIC_ATIV_EMPR is False
    assert mock_model.DAT_BAIX is not None
    assert isinstance(mock_model.DAT_BAIX, datetime)


def test_veiculo_repository_update_bulk_already_deactivated_raises_error():
    mock_db = MagicMock()
    repo = VeiculoRepository(mock_db)

    existing_veiculo = Veiculo(
        NUM_VEIC=1111,
        IDN_PLAC_VEIC="OPC123",
        VEIC_ATIV_EMPR=False,
        DAT_BAIX=datetime(2026, 1, 1),
    )
    mock_model = repo._to_model(existing_veiculo)
    mock_db.query.return_value.filter.return_value.first.return_value = mock_model

    payload = [Veiculo(NUM_VEIC=1111, VEIC_ATIV_EMPR=False)]

    with pytest.raises(ErrUpdateData) as exc_info:
        repo.update_bulk(payload)
    assert exc_info.value.status == 400
    assert "já se encontra baixado" in exc_info.value.message


def test_veiculo_repository_update_bulk_reactivate():
    mock_db = MagicMock()
    repo = VeiculoRepository(mock_db)

    existing_veiculo = Veiculo(
        NUM_VEIC=1111,
        IDN_PLAC_VEIC="OPC123",
        VEIC_ATIV_EMPR=False,
        DAT_BAIX=datetime(2026, 1, 1),
    )
    mock_model = repo._to_model(existing_veiculo)
    mock_db.query.return_value.filter.return_value.first.return_value = mock_model

    payload = [Veiculo(NUM_VEIC=1111, VEIC_ATIV_EMPR=True)]

    count = repo.update_bulk(payload)
    assert count == 1
    assert mock_model.VEIC_ATIV_EMPR is True
    assert mock_model.DAT_BAIX is None


def test_service_get_veiculos():
    mock_db_manager = MagicMock()
    mock_session = mock_db_manager.session.return_value.__enter__.return_value
    mock_repo = mock_session.get_veiculo_repository.return_value

    mock_veic = Veiculo(
        NUM_VEIC=1111,
        IDN_PLAC_VEIC="OPC123",
        VEIC_ATIV_EMPR=False,
        DAT_BAIX=datetime(2026, 8, 28, 12, 0, 0),
    )
    mock_repo.get_all.return_value = [mock_veic]

    service = VeiculoService(mock_db_manager)
    res = service.get_veiculos()
    assert len(res) == 1
    assert res[0].vehicle_number == 1111
    assert res[0].to_dict()["DAT_BAIX"] == "2026-08-28T12:00:00"


@pytest.mark.usefixtures("app", "client", "database")
class TestVeiculos:
    @patch("services.veiculo_service.VeiculoService.get_veiculos")
    def test_get_route(self, mock_get, client, database):
        """Test that GET /veiculos returns 200 and the correct list."""
        mock_get.return_value = [
            {
                "NUM_VEIC": 1111,
                "IDN_PLAC_VEIC": "OPC123",
                "VEIC_ATIV_EMPR": False,
                "DAT_BAIX": None,
            }
        ]

        response = client.get("/veiculos")

        assert response.status_code == 200
        data = response.get_json()
        assert "veiculos" in data
        assert len(data["veiculos"]) == 1
        assert data["veiculos"][0]["NUM_VEIC"] == 1111
        assert data["veiculos"][0]["DAT_BAIX"] is None

    @patch("services.veiculo_service.VeiculoService.get_veiculos")
    def test_get_route_with_data_baixa(self, mock_get, client, database):
        """Test that GET /veiculos returns 200 with DAT_BAIX populated."""
        mock_get.return_value = [
            {
                "NUM_VEIC": 2222,
                "IDN_PLAC_VEIC": "ABC1234",
                "VEIC_ATIV_EMPR": False,
                "DAT_BAIX": "2026-08-28T10:30:00",
            }
        ]

        response = client.get("/veiculos")

        assert response.status_code == 200
        data = response.get_json()
        assert "veiculos" in data
        assert len(data["veiculos"]) == 1
        assert data["veiculos"][0]["NUM_VEIC"] == 2222
        assert data["veiculos"][0]["DAT_BAIX"] == "2026-08-28T10:30:00"

    @patch("services.veiculo_service.VeiculoService.insert_veiculos")
    def test_insert_route(self, mock_insert, client, database):
        """Test POST /veiculos route."""
        mock_insert.return_value = 1

        payload = [
            {"NUM_VEIC": 1111, "IDN_PLAC_VEIC": "OPC123", "VEIC_ATIV_EMPR": True}
        ]

        response = client.post("/veiculos", json=payload)

        assert response.status_code == 201
        data = response.get_json()
        assert data["message"] == "Veículos inseridos com sucesso"
        assert data["counter"] == 1

    @patch("services.veiculo_service.VeiculoService.update_veiculos")
    def test_update_route(self, mock_update, client, database):
        """Test PATCH /veiculos route."""
        mock_update.return_value = 1

        payload = [
            {"NUM_VEIC": 1111, "IDN_PLAC_VEIC": "OPC123", "VEIC_ATIV_EMPR": False}
        ]

        response = client.patch("/veiculos", json=payload)

        assert response.status_code == 202
        data = response.get_json()
        assert data["message"] == "Veículos atualizados com sucesso"
        assert data["counter"] == 1

    @patch("services.veiculo_service.VeiculoService.delete_veiculos")
    def test_delete_route(self, mock_delete, client, database):
        """Test DELETE /veiculos/<NUM_VEIC> route."""
        mock_delete.return_value = 1

        response = client.delete("/veiculos/1111")

        assert response.status_code == 202
        data = response.get_json()
        assert data["message"] == "Veículos deletados com sucesso"
        assert data["counter"] == 1


def test_veiculo_repository_insert_bulk_already_exists():
    from exceptions.CustomExceptions import ErrInsertData

    mock_db = MagicMock()
    # Mock to ensure the exists check returns some vehicles
    mock_db.query.return_value.filter.return_value.all.return_value = [(1111,)]
    repo = VeiculoRepository(mock_db)

    payload = [Veiculo(NUM_VEIC=1111, IDN_PLAC_VEIC="OPC123", VEIC_ATIV_EMPR=True)]

    with pytest.raises(ErrInsertData) as exc_info:
        repo.insert_bulk(payload)

    assert exc_info.value.status == 409
    assert (
        "já existem e não podem ser sobrescritos: 1111"
        in exc_info.value.friendly_message
    )
