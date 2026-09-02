import json
from io import BytesIO
from unittest.mock import patch

import pytest


@pytest.mark.usefixtures("app", "client", "database")
class TestInfracoes:
    @patch(
        "services.document_parser.factory.PyIngestionParserFactory.create_infracoes_csv_parser"
    )
    def test_post_csv_route(self, mock_create, client, database):
        """Testa se a rota POST /infracao/csv importa com sucesso"""
        from unittest.mock import MagicMock

        mock_extractor = MagicMock()

        def fake_extract(stream):
            return {"rows_processed": 5, "inserted": 5, "ignored": 0}

        mock_extractor.extract.side_effect = fake_extract
        mock_create.return_value = mock_extractor

        data = {
            "file": (
                BytesIO(
                    b"NUM_AI;HORA;DAT_OCOR_INFR;DAT_EMIS_NOTF;DAT_LIMT_RECU;VAL_INFR\n1234;12:00;01/01/2026;02/01/2026;03/01/2026;100.00"
                ),
                "test.csv",
            )
        }

        response = client.post(
            "/infracao/csv", data=data, content_type="multipart/form-data"
        )
        assert response.status_code == 200
        res_data = json.loads(response.data)
        assert res_data["message"] == "5 autos de infração importados"

    @patch(
        "services.document_parser.factory.PyIngestionParserFactory.create_infracoes_xls_parser"
    )
    def test_post_xls_route(self, mock_create, client, database):
        """Testa se a rota POST /infracao/xls insere com sucesso"""
        from unittest.mock import MagicMock

        mock_extractor = MagicMock()

        def fake_extract(stream):
            return {"rows_processed": 10, "inserted": 10, "ignored": 0}

        mock_extractor.extract.side_effect = fake_extract
        mock_create.return_value = mock_extractor

        data = {"file": (BytesIO(b"dummy excel content"), "test.xls")}

        response = client.post(
            "/infracao/xls", data=data, content_type="multipart/form-data"
        )
        assert response.status_code == 200
        res_data = json.loads(response.data)
        assert res_data["message"] == "10 autos inseridos com sucesso"

    @patch("routes.autoinfracao.AutoInfracaoService.get_infracoes")
    def test_get_infracoes_route(self, mock_get, client, database):
        """Testa se a rota GET /infracao busca corretamente"""
        mock_get.return_value = [{"NUM_AI": "1234-A", "VAL_INFR": 150.0}]

        response = client.get("/infracao?ai=1234-A")
        assert response.status_code == 200
        res_data = json.loads(response.data)
        assert "autos" in res_data
        assert len(res_data["autos"]) == 1
        assert res_data["autos"][0]["NUM_AI"] == "1234-A"

    @patch("routes.autoinfracao.AutoInfracaoService.check_infracoes")
    def test_check_infracoes_route(self, mock_check, client, database):
        """Testa se a rota POST /infracao/check valida os registros"""
        mock_check.return_value = (8, 10, ["9999-X", "8888-Y"])

        data = {"file": (BytesIO(b"NUM_AI\n1234;5678"), "test.csv")}

        response = client.post(
            "/infracao/check", data=data, content_type="multipart/form-data"
        )
        assert response.status_code == 200
        res_data = json.loads(response.data)
        assert "db_rows" in res_data
        assert "file_rows" in res_data
        assert "Not Present" in res_data
