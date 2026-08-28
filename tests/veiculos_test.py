import pytest
import json
from datetime import datetime
from unittest.mock import patch, MagicMock

from classes.Veiculo import Veiculo
from repositories.veiculo_repository import VeiculoRepository
from exceptions.CustomExceptions import ErrUpdateData
from handlers import veiculos as handlers_veiculos


def test_veiculo_model_without_dat_baix():
    veic = Veiculo(
        NUM_VEIC=1111,
        IDN_PLAC_VEIC="OPC123",
        VEIC_ATIV_EMPR=True,
        DAT_BAIX=None,
    )
    data = veic.to_dict()
    assert data == {
        'NUM_VEIC': 1111,
        'IDN_PLAC_VEIC': "OPC123",
        'VEIC_ATIV_EMPR': True,
        'DAT_BAIX': None,
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
        'NUM_VEIC': 2222,
        'IDN_PLAC_VEIC': "XYZ987",
        'VEIC_ATIV_EMPR': False,
        'DAT_BAIX': "2026-08-28T10:00:00",
    }


def test_veiculo_repository_insert_bulk():
    mock_db = MagicMock()
    repo = VeiculoRepository(mock_db)

    payload = [
        {"NUM_VEIC": 1111, "IDN_PLAC_VEIC": "OPC123", "VEIC_ATIV_EMPR": True},
        {
            "NUM_VEIC": 2222,
            "IDN_PLAC_VEIC": "XYZ987",
            "VEIC_ATIV_EMPR": False,
            "DAT_BAIX": "2026-08-28T10:00:00",
        },
    ]

    count = repo.insert_bulk(payload)
    assert count == 2
    assert mock_db.merge.call_count == 2


def test_veiculo_repository_update_bulk_deactivate():
    mock_db = MagicMock()
    repo = VeiculoRepository(mock_db)

    existing_veiculo = Veiculo(
        NUM_VEIC=1111,
        IDN_PLAC_VEIC="OPC123",
        VEIC_ATIV_EMPR=True,
        DAT_BAIX=None,
    )
    mock_db.query.return_value.filter.return_value.first.return_value = existing_veiculo

    payload = [
        {"NUM_VEIC": 1111, "VEIC_ATIV_EMPR": False}
    ]

    count = repo.update_bulk(payload)
    assert count == 1
    assert existing_veiculo.VEIC_ATIV_EMPR is False
    assert existing_veiculo.DAT_BAIX is not None
    assert isinstance(existing_veiculo.DAT_BAIX, datetime)


def test_veiculo_repository_update_bulk_already_deactivated_raises_error():
    mock_db = MagicMock()
    repo = VeiculoRepository(mock_db)

    existing_veiculo = Veiculo(
        NUM_VEIC=1111,
        IDN_PLAC_VEIC="OPC123",
        VEIC_ATIV_EMPR=False,
        DAT_BAIX=datetime(2026, 1, 1),
    )
    mock_db.query.return_value.filter.return_value.first.return_value = existing_veiculo

    payload = [
        {"NUM_VEIC": 1111, "VEIC_ATIV_EMPR": False}
    ]

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
    mock_db.query.return_value.filter.return_value.first.return_value = existing_veiculo

    payload = [
        {"NUM_VEIC": 1111, "VEIC_ATIV_EMPR": True}
    ]

    count = repo.update_bulk(payload)
    assert count == 1
    assert existing_veiculo.VEIC_ATIV_EMPR is True
    assert existing_veiculo.DAT_BAIX is None


@patch("handlers.veiculos.get_db")
@patch("handlers.veiculos.VeiculoRepository")
def test_handler_get_veiculos(mock_repo_cls, mock_get_db):
    mock_db = MagicMock()
    mock_get_db.return_value.__enter__.return_value = mock_db
    mock_repo = MagicMock()
    mock_repo_cls.return_value = mock_repo

    mock_veic = Veiculo(
        NUM_VEIC=1111,
        IDN_PLAC_VEIC="OPC123",
        VEIC_ATIV_EMPR=False,
        DAT_BAIX=datetime(2026, 8, 28, 12, 0, 0),
    )
    mock_repo.get_all.return_value = [mock_veic]

    res = handlers_veiculos.getVeiculos()
    data = json.loads(res)
    assert len(data) == 1
    assert data[0]["NUM_VEIC"] == 1111
    assert data[0]["DAT_BAIX"] == "2026-08-28T12:00:00"


@pytest.mark.usefixtures("app", "client", "database")
class TestVeiculos:
    @patch("handlers.veiculos.getVeiculos")
    def test_get_route(self, mock_get, client, database):
        """Testa se a rota GET /veiculos retorna 200 e a lista correta"""
        mock_get.return_value = (
            '[{"NUM_VEIC": 1111, "IDN_PLAC_VEIC": "OPC123", "VEIC_ATIV_EMPR": false, "DAT_BAIX": null}]'
        )

        response = client.get("/veiculos")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "veiculos" in data
        assert len(data["veiculos"]) == 1
        assert data["veiculos"][0]["NUM_VEIC"] == 1111
        assert data["veiculos"][0]["DAT_BAIX"] is None

    @patch("handlers.veiculos.getVeiculos")
    def test_get_route_with_data_baixa(self, mock_get, client, database):
        """Testa se a rota GET /veiculos retorna 200 com DAT_BAIX preenchido"""
        mock_get.return_value = (
            '[{"NUM_VEIC": 2222, "IDN_PLAC_VEIC": "ABC1234", "VEIC_ATIV_EMPR": false, "DAT_BAIX": "2026-08-28T10:30:00"}]'
        )

        response = client.get("/veiculos")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "veiculos" in data
        assert len(data["veiculos"]) == 1
        assert data["veiculos"][0]["NUM_VEIC"] == 2222
        assert data["veiculos"][0]["DAT_BAIX"] == "2026-08-28T10:30:00"

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

    @patch("handlers.veiculos.deleteVeiculos")
    def test_delete_route(self, mock_delete, client, database):
        """Testa a rota DELETE /veiculos/<NUM_VEIC>"""
        mock_delete.return_value = 1

        response = client.delete("/veiculos/1111")

        assert response.status_code == 202
        data = json.loads(response.data)
        assert data["message"] == "Veículos deletados com sucesso"
        assert data["counter"] == 1

