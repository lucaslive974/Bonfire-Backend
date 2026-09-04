import pytest


@pytest.mark.usefixtures("app", "client", "database")
class TestOpenApiDocumentation:
    def test_openapi_json_endpoint(self, client):
        """Verify that the /apidoc/openapi.json endpoint returns a valid OpenAPI specification."""
        response = client.get("/apidoc/openapi.json")
        assert response.status_code == 200
        data = response.get_json()

        assert "openapi" in data
        assert data["info"]["title"] == "Bonfire Backend API"
        assert "paths" in data

        paths = data["paths"]
        # Verify that versioned routes are documented
        assert "/v1/consorcio" in paths
        assert "/v1/veiculos" in paths
        assert "/v1/linha" in paths
        assert "/v1/infracao" in paths
        assert "/v1/infracao/csv" in paths
        assert "/v1/infracao/xls" in paths
        assert "/v1/infracao/check" in paths
        assert "/v1/recurso/primeiraInstancia/resultado" in paths
        assert "/v1/recurso/segundaInstancia/resultado" in paths

    def test_swagger_ui_endpoint(self, client):
        """Verify that the Swagger UI interface loads with 200 OK."""
        response = client.get("/apidoc/swagger/", follow_redirects=True)
        assert response.status_code == 200
        assert (
            b"swagger" in response.data.lower() or b"openapi" in response.data.lower()
        )
