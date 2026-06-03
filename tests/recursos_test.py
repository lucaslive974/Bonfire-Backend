import pytest
from typing import Any
from io import BytesIO
from unittest.mock import patch, MagicMock
from datetime import date

from classes.Recurso import RecursoPrimeiraInstancia, RecursoSegundaInstancia
from exceptions.CustomExceptions import ErrNullInsert
from handlers import recursos as handlers_recursos


def test_recurso_primeira_instancia_model():
    model = RecursoPrimeiraInstancia(
        ID=1,
        NUM_AI="123456-A",
        NUM_ATA=5,
        NUM_RECURSO="123/2026",
        NOM_CONC="Consórcio BH Leste",
        RESULTADO=True,
        DAT_PUBL=date(2026, 5, 15)
    )
    data = model.to_dict()
    assert data == {
        'ID': 1,
        'NUM_AI': "123456-A",
        'NUM_ATA': 5,
        'NUM_RECURSO': "123/2026",
        'NOM_CONC': "Consórcio BH Leste",
        'RESULTADO': True,
        'DAT_PUBL': "2026-05-15"
    }


def test_recurso_segunda_instancia_model():
    model = RecursoSegundaInstancia(
        ID=2,
        NUM_AI="654321-B",
        NUM_RECURSO="321/2026",
        NOM_CONC="Consórcio Leste",
        RESULTADO=False,
        DAT_PUBL=date(2026, 6, 20)
    )
    data = model.to_dict()
    assert data == {
        'ID': 2,
        'NUM_AI': "654321-B",
        'NUM_RECURSO': "321/2026",
        'NOM_CONC': "Consórcio Leste",
        'RESULTADO': False,
        'DAT_PUBL': "2026-06-20"
    }


@patch("handlers.recursos.get_db")
@patch("handlers.recursos.RecursoRepository")
def test_handler_get_primeira_instancia(mock_repo_cls: MagicMock, mock_get_db: MagicMock):
    mock_db = MagicMock()
    mock_get_db.return_value.__enter__.return_value = mock_db
    mock_repo = MagicMock()
    mock_repo_cls.return_value = mock_repo
    mock_repo.get_primeira_instancia.return_value = [{"recurso": "123"}]

    res = handlers_recursos.getPrimeiraInstancia("2026-05-15", 5)
    assert res == [{"recurso": "123"}]
    mock_repo_cls.assert_called_once_with(mock_db)
    mock_repo.get_primeira_instancia.assert_called_once_with("2026-05-15", 5)


@patch("handlers.recursos.get_db")
@patch("handlers.recursos.RecursoRepository")
def test_handler_get_segunda_instancia(mock_repo_cls: MagicMock, mock_get_db: MagicMock):
    mock_db = MagicMock()
    mock_get_db.return_value.__enter__.return_value = mock_db
    mock_repo = MagicMock()
    mock_repo_cls.return_value = mock_repo
    mock_repo.get_segunda_instancia.return_value = [{"recurso": "321"}]

    res = handlers_recursos.getSegundaInstancia("2026-06-20")
    assert res == [{"recurso": "321"}]
    mock_repo_cls.assert_called_once_with(mock_db)
    mock_repo.get_segunda_instancia.assert_called_once_with("2026-06-20")


@patch("handlers.recursos.get_db")
@patch("handlers.recursos.RecursoRepository")
def test_handler_insert_primeira_instancia(mock_repo_cls: MagicMock, mock_get_db: MagicMock):
    mock_db = MagicMock()
    mock_get_db.return_value.__enter__.return_value = mock_db
    mock_repo = MagicMock()
    mock_repo_cls.return_value = mock_repo
    mock_repo.insert_primeira_instancia.return_value = 10

    payload = [{"NUM_RECURSO": "123"}]
    res = handlers_recursos.insertPrimeiraInstancia(payload)
    assert res == 10
    mock_repo_cls.assert_called_once_with(mock_db)
    mock_repo.insert_primeira_instancia.assert_called_once_with(payload)


def test_handler_insert_primeira_instancia_null():
    with pytest.raises(ErrNullInsert):
        handlers_recursos.insertPrimeiraInstancia(None)


@patch("handlers.recursos.get_db")
@patch("handlers.recursos.RecursoRepository")
def test_handler_insert_segunda_instancia(mock_repo_cls: MagicMock, mock_get_db: MagicMock):
    mock_db = MagicMock()
    mock_get_db.return_value.__enter__.return_value = mock_db
    mock_repo = MagicMock()
    mock_repo_cls.return_value = mock_repo
    mock_repo.insert_segunda_instancia.return_value = 20

    payload = [{"NUM_RECURSO": "321"}]
    res = handlers_recursos.insertSegundaInstancia(payload)
    assert res == 20
    mock_repo_cls.assert_called_once_with(mock_db)
    mock_repo.insert_segunda_instancia.assert_called_once_with(payload)


def test_handler_insert_segunda_instancia_null():
    with pytest.raises(ErrNullInsert):
        handlers_recursos.insertSegundaInstancia(None)


@pytest.mark.usefixtures("app", "client", "database")
class TestRecursoRoutes:
    @patch("handlers.recursos.getPrimeiraInstancia")
    def test_get_primeira_instancia_route(self, mock_get: MagicMock, client: Any, database: Any):
        mock_get.return_value = [{"NUM_RECURSO": "123"}]
        response = client.get("/recurso/primeiraInstancia?date=2026-05-15&ata=5")
        assert response.status_code == 200
        data = response.get_json()
        assert data == {"recurses": [{"NUM_RECURSO": "123"}]}
        mock_get.assert_called_once_with("2026-05-15", "5")

    @patch("handlers.recursos.getSegundaInstancia")
    def test_get_segunda_instancia_route(self, mock_get: MagicMock, client: Any, database: Any):
        mock_get.return_value = [{"NUM_RECURSO": "321"}]
        response = client.get("/recurso/segundaInstancia?date=2026-06-20")
        assert response.status_code == 200
        data = response.get_json()
        assert data == {"recurses": [{"NUM_RECURSO": "321"}]}
        mock_get.assert_called_once_with("2026-06-20")

    @patch("routes.recursos.recursos.insertPrimeiraInstancia")
    @patch("routes.recursos.recursos.parseDocx")
    def test_post_primeira_instancia_route(self, mock_parse: MagicMock, mock_insert: MagicMock, client: Any, database: Any):
        mock_parse.return_value = [{"NUM_RECURSO": "123"}]
        mock_insert.return_value = 5

        data = {"file": (BytesIO(b"docx content"), "test.docx")}
        response = client.post("/recurso/primeiraInstancia/resultado", data=data, content_type="multipart/form-data")
        assert response.status_code == 200
        res_data = response.get_json()
        assert res_data == {
            "message": "itens Extraídos e armazenados com sucesso!",
            "counter": 5
        }

    def test_post_primeira_instancia_route_no_file(self, client: Any, database: Any):
        response = client.post("/recurso/primeiraInstancia/resultado", data={}, content_type="multipart/form-data")
        assert response.status_code == 400
        res_data = response.get_json()
        assert res_data["error"] == "Incomplete Data"

    @patch("routes.recursos.recursos.insertSegundaInstancia")
    @patch("routes.recursos.recursos.parseDocx")
    def test_post_segunda_instancia_route(self, mock_parse: MagicMock, mock_insert: MagicMock, client: Any, database: Any):
        mock_parse.return_value = [{"NUM_RECURSO": "321"}]
        mock_insert.return_value = 10

        data = {"file": (BytesIO(b"docx content"), "test.docx")}
        response = client.post("/recurso/segundaInstancia/resultado", data=data, content_type="multipart/form-data")
        assert response.status_code == 200
        res_data = response.get_json()
        assert res_data == {
            "message": "itens Extraídos e armazenados com sucesso!",
            "counter": 10
        }

    def test_post_segunda_instancia_route_no_file(self, client: Any, database: Any):
        response = client.post("/recurso/segundaInstancia/resultado", data={}, content_type="multipart/form-data")
        assert response.status_code == 400
        res_data = response.get_json()
        assert res_data["error"] == "Incomplete Data"
