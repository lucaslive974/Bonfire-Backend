from datetime import date
from io import BytesIO
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from classes.Recurso import RecursoPrimeiraInstancia, RecursoSegundaInstancia
from exceptions.CustomExceptions import ErrNullInsert
from services.recurso_service import RecursoService


def test_recurso_primeira_instancia_model():
    model = RecursoPrimeiraInstancia(
        NUM_AI="123456-A",
        NUM_ATA=5,
        NUM_RECURSO="123/2026",
        NOM_CONC="Consórcio BH Leste",
        RESULTADO=True,
        DAT_PUBL=date(2026, 5, 15),
    )
    data = model.to_dict()
    assert data == {
        "NUM_AI": "123456-A",
        "NUM_ATA": 5,
        "NUM_RECURSO": "123/2026",
        "NOM_CONC": "Consórcio BH Leste",
        "RESULTADO": True,
        "DAT_PUBL": "2026-05-15",
    }


def test_recurso_segunda_instancia_model():
    model = RecursoSegundaInstancia(
        NUM_AI="654321-B",
        NUM_RECURSO="321/2026",
        NOM_CONC="Consórcio Leste",
        RESULTADO=False,
        DAT_PUBL=date(2026, 6, 20),
    )
    data = model.to_dict()
    assert data == {
        "NUM_AI": "654321-B",
        "NUM_RECURSO": "321/2026",
        "NOM_CONC": "Consórcio Leste",
        "RESULTADO": False,
        "DAT_PUBL": "2026-06-20",
    }


def test_service_get_primeira_instancia():
    mock_db_manager = MagicMock()
    mock_session = mock_db_manager.session.return_value.__enter__.return_value
    mock_repo = mock_session.get_recurso_repository.return_value
    mock_repo.get_primeira_instancia.return_value = [{"recurso": "123"}]

    service = RecursoService(mock_db_manager)
    res = service.get_primeira_instancia("2026-05-15", 5)
    assert res == [{"recurso": "123"}]
    mock_repo.get_primeira_instancia.assert_called_once_with("2026-05-15", 5)


def test_service_get_segunda_instancia():
    mock_db_manager = MagicMock()
    mock_session = mock_db_manager.session.return_value.__enter__.return_value
    mock_repo = mock_session.get_recurso_repository.return_value
    mock_repo.get_segunda_instancia.return_value = [{"recurso": "321"}]

    service = RecursoService(mock_db_manager)
    res = service.get_segunda_instancia("2026-06-20")
    assert res == [{"recurso": "321"}]
    mock_repo.get_segunda_instancia.assert_called_once_with("2026-06-20")


def test_service_insert_primeira_instancia():
    mock_db_manager = MagicMock()
    mock_session = mock_db_manager.session.return_value.__enter__.return_value
    mock_repo = mock_session.get_recurso_repository.return_value
    mock_repo.insert_primeira_instancia.return_value = 10

    payload = [{"NUM_RECURSO": "123"}]
    service = RecursoService(mock_db_manager)
    res = service.insert_primeira_instancia(payload)
    assert res == 10
    mock_repo.insert_primeira_instancia.assert_called_once_with(payload)


def test_service_insert_primeira_instancia_null():
    mock_db_manager = MagicMock()
    service = RecursoService(mock_db_manager)
    with pytest.raises(ErrNullInsert):
        service.insert_primeira_instancia(None)


def test_service_insert_segunda_instancia():
    mock_db_manager = MagicMock()
    mock_session = mock_db_manager.session.return_value.__enter__.return_value
    mock_repo = mock_session.get_recurso_repository.return_value
    mock_repo.insert_segunda_instancia.return_value = 20

    payload = [{"NUM_RECURSO": "321"}]
    service = RecursoService(mock_db_manager)
    res = service.insert_segunda_instancia(payload)
    assert res == 20
    mock_repo.insert_segunda_instancia.assert_called_once_with(payload)


def test_service_insert_segunda_instancia_null():
    mock_db_manager = MagicMock()
    service = RecursoService(mock_db_manager)
    with pytest.raises(ErrNullInsert):
        service.insert_segunda_instancia(None)


@pytest.mark.usefixtures("app", "client", "database")
class TestRecursoRoutes:
    @patch("services.recurso_service.RecursoService.get_primeira_instancia")
    def test_get_primeira_instancia_route(
        self, mock_get: MagicMock, client: Any, database: Any
    ):
        mock_get.return_value = [{"NUM_RECURSO": "123"}]
        response = client.get("/recurso/primeiraInstancia?date=2026-05-15&ata=5")
        assert response.status_code == 200
        data = response.get_json()
        assert data == {"recurses": [{"NUM_RECURSO": "123"}]}
        mock_get.assert_called_once_with("2026-05-15", "5")

    @patch("services.recurso_service.RecursoService.get_segunda_instancia")
    def test_get_segunda_instancia_route(
        self, mock_get: MagicMock, client: Any, database: Any
    ):
        mock_get.return_value = [{"NUM_RECURSO": "321"}]
        response = client.get("/recurso/segundaInstancia?date=2026-06-20")
        assert response.status_code == 200
        data = response.get_json()
        assert data == {"recurses": [{"NUM_RECURSO": "321"}]}
        mock_get.assert_called_once_with("2026-06-20")

    @patch("services.parsers.factory.ParserFactory.create_primeira_instancia_parser")
    def test_post_primeira_instancia_route(
        self, mock_create: MagicMock, client: Any, database: Any
    ):
        mock_extractor = MagicMock()

        def fake_extract(stream):
            return {"rows_processed": 5, "inserted": 5, "ignored": 0}

        mock_extractor.extract.side_effect = fake_extract
        mock_create.return_value = mock_extractor

        data = {"file": (BytesIO(b"docx content"), "test.docx")}
        response = client.post(
            "/recurso/primeiraInstancia/resultado",
            data=data,
            content_type="multipart/form-data",
        )
        assert response.status_code == 200
        res_data = response.get_json()
        assert res_data == {
            "message": "itens Extraídos e armazenados com sucesso!",
            "counter": 5,
        }

    def test_post_primeira_instancia_route_no_file(self, client: Any, database: Any):
        response = client.post(
            "/recurso/primeiraInstancia/resultado",
            data={},
            content_type="multipart/form-data",
        )
        assert response.status_code == 400
        res_data = response.get_json()
        assert res_data["error"] == "Incomplete Data"

    @patch("services.parsers.factory.ParserFactory.create_segunda_instancia_parser")
    def test_post_segunda_instancia_route(
        self, mock_create: MagicMock, client: Any, database: Any
    ):
        mock_extractor = MagicMock()

        def fake_extract(stream):
            return {"rows_processed": 10, "inserted": 10, "ignored": 0}

        mock_extractor.extract.side_effect = fake_extract
        mock_create.return_value = mock_extractor

        data = {"file": (BytesIO(b"docx content"), "test.docx")}
        response = client.post(
            "/recurso/segundaInstancia/resultado",
            data=data,
            content_type="multipart/form-data",
        )
        assert response.status_code == 200
        res_data = response.get_json()
        assert res_data == {
            "message": "itens Extraídos e armazenados com sucesso!",
            "counter": 10,
        }

    def test_post_segunda_instancia_route_no_file(self, client: Any, database: Any):
        response = client.post(
            "/recurso/segundaInstancia/resultado",
            data={},
            content_type="multipart/form-data",
        )
        assert response.status_code == 400
        res_data = response.get_json()
        assert res_data["error"] == "Incomplete Data"
