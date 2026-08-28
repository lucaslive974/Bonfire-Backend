import pytest
import json
from datetime import datetime
from unittest.mock import patch, MagicMock

from classes.Linha import Linha
from repositories.linha_repository import LinhaRepository
from exceptions.CustomExceptions import ErrUpdateData
from handlers import linha as handlers_linha


def test_linha_model_without_dat_baix():
    linha = Linha(
        COD_LINH="61",
        ID_OPERADORA=107,
        COMPARTILHADA=True,
        LINH_ATIV_EMPR=True,
        DAT_BAIX=None,
    )
    data = linha.to_dict()
    assert data == {
        'COD_LINH': "61",
        'ID_OPERADORA': 107,
        'COMPARTILHADA': True,
        'LINH_ATIV_EMPR': True,
        'DAT_BAIX': None,
    }


def test_linha_model_with_dat_baix():
    dt = datetime(2026, 8, 28, 10, 0, 0)
    linha = Linha(
        COD_LINH="62",
        ID_OPERADORA=108,
        COMPARTILHADA=False,
        LINH_ATIV_EMPR=False,
        DAT_BAIX=dt,
    )
    data = linha.to_dict()
    assert data == {
        'COD_LINH': "62",
        'ID_OPERADORA': 108,
        'COMPARTILHADA': False,
        'LINH_ATIV_EMPR': False,
        'DAT_BAIX': "2026-08-28T10:00:00",
    }


def test_linha_repository_insert_bulk():
    mock_db = MagicMock()
    repo = LinhaRepository(mock_db)

    payload = [
        {
            "COD_LINH": "61",
            "ID_OPERADORA": 107,
            "COMPARTILHADA": True,
            "LINH_ATIV_EMPR": True,
        },
        {
            "COD_LINH": "62",
            "ID_OPERADORA": 108,
            "COMPARTILHADA": False,
            "LINH_ATIV_EMPR": False,
            "DAT_BAIX": "2026-08-28T10:00:00",
        },
    ]

    count = repo.insert_bulk(payload)
    assert count == 2
    assert mock_db.merge.call_count == 2


def test_linha_repository_update_bulk_deactivate():
    mock_db = MagicMock()
    repo = LinhaRepository(mock_db)

    existing_linha = Linha(
        COD_LINH="61",
        ID_OPERADORA=107,
        COMPARTILHADA=True,
        LINH_ATIV_EMPR=True,
        DAT_BAIX=None,
    )
    mock_db.query.return_value.filter.return_value.first.return_value = existing_linha

    payload = [
        {"COD_LINH": "61", "LINH_ATIV_EMPR": False}
    ]

    count = repo.update_bulk(payload)
    assert count == 1
    assert existing_linha.LINH_ATIV_EMPR is False
    assert existing_linha.DAT_BAIX is not None
    assert isinstance(existing_linha.DAT_BAIX, datetime)


def test_linha_repository_update_bulk_already_deactivated_raises_error():
    mock_db = MagicMock()
    repo = LinhaRepository(mock_db)

    existing_linha = Linha(
        COD_LINH="61",
        ID_OPERADORA=107,
        COMPARTILHADA=True,
        LINH_ATIV_EMPR=False,
        DAT_BAIX=datetime(2026, 1, 1),
    )
    mock_db.query.return_value.filter.return_value.first.return_value = existing_linha

    payload = [
        {"COD_LINH": "61", "LINH_ATIV_EMPR": False}
    ]

    with pytest.raises(ErrUpdateData) as exc_info:
        repo.update_bulk(payload)
    assert exc_info.value.status == 400
    assert "já se encontra baixada" in exc_info.value.message


def test_linha_repository_update_bulk_reactivate():
    mock_db = MagicMock()
    repo = LinhaRepository(mock_db)

    existing_linha = Linha(
        COD_LINH="61",
        ID_OPERADORA=107,
        COMPARTILHADA=True,
        LINH_ATIV_EMPR=False,
        DAT_BAIX=datetime(2026, 1, 1),
    )
    mock_db.query.return_value.filter.return_value.first.return_value = existing_linha

    payload = [
        {"COD_LINH": "61", "LINH_ATIV_EMPR": True}
    ]

    count = repo.update_bulk(payload)
    assert count == 1
    assert existing_linha.LINH_ATIV_EMPR is True
    assert existing_linha.DAT_BAIX is None


@patch("handlers.linha.get_db")
@patch("handlers.linha.LinhaRepository")
def test_handler_get_linha(mock_repo_cls, mock_get_db):
    mock_db = MagicMock()
    mock_get_db.return_value.__enter__.return_value = mock_db
    mock_repo = MagicMock()
    mock_repo_cls.return_value = mock_repo

    mock_linha = Linha(
        COD_LINH="61",
        ID_OPERADORA=107,
        COMPARTILHADA=True,
        LINH_ATIV_EMPR=False,
        DAT_BAIX=datetime(2026, 8, 28, 12, 0, 0),
    )
    mock_repo.get_all.return_value = [mock_linha]

    res = handlers_linha.getLinha()
    data = json.loads(res)
    assert len(data) == 1
    assert data[0]["COD_LINH"] == "61"
    assert data[0]["DAT_BAIX"] == "2026-08-28T12:00:00"


@pytest.mark.usefixtures("app", "client", "database")
class TestLinha:
    @patch("handlers.linha.getLinha")
    def test_get_route(self, mock_get, client, database):
        """Testa se a rota GET /linha retorna a lista correta de linhas"""
        mock_get.return_value = '[{"COD_LINH": "61", "ID_OPERADORA": 107, "COMPARTILHADA": true, "LINH_ATIV_EMPR": true, "DAT_BAIX": null}]'

        response = client.get("/linha")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "linha" in data
        assert len(data["linha"]) == 1
        assert data["linha"][0]["COD_LINH"] == "61"
        assert data["linha"][0]["DAT_BAIX"] is None

    @patch("handlers.linha.getLinha")
    def test_get_route_with_data_baixa(self, mock_get, client, database):
        """Testa se a rota GET /linha retorna a lista com DAT_BAIX preenchido"""
        mock_get.return_value = '[{"COD_LINH": "62", "ID_OPERADORA": 108, "COMPARTILHADA": false, "LINH_ATIV_EMPR": false, "DAT_BAIX": "2026-08-28T11:00:00"}]'

        response = client.get("/linha")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "linha" in data
        assert len(data["linha"]) == 1
        assert data["linha"][0]["COD_LINH"] == "62"
        assert data["linha"][0]["DAT_BAIX"] == "2026-08-28T11:00:00"

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

    @patch("handlers.linha.deleteLinha")
    def test_delete_route(self, mock_delete, client, database):
        """Testa se a rota DELETE /linha/<COD_LINH> deleta linhas com sucesso"""
        mock_delete.return_value = 1

        response = client.delete("/linha/61")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["message"] == "linha deletada com sucesso"
        assert data["counter"] == 1

