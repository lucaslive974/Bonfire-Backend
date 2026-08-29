import os

# Set dummy environment variables to prevent Config from raising ErrMissingRequiredEnv during test imports
for key, val in [
    ("DB_PASSWORD", "test_password"),
    ("KEYCLOAK_CLIENT_SECRET", "test_client_secret"),
    ("KEYCLOAK_REALM_NAME", "test_realm"),
]:
    os.environ.setdefault(key, val)

import pytest
from unittest.mock import patch

# Mock database connection check and Keycloak connection check during test imports
patcher_db = patch("repositories.database.check_database_connection")
patcher_kc_conn = patch("core.auth.authenticator.KeyCloakAuthenticator.checkConnection")

patcher_db.start()
patcher_kc_conn.start()

from app import BonfireApp


@pytest.fixture(scope="session")
def app():
    # Patch checkAuth method of BonfireApp to return None (bypass auth)
    with patch.object(BonfireApp, "checkAuth", return_value=None):
        application = BonfireApp("test_bonfire")
        application.config.update(
            {
                "TESTING": True,
            }
        )
        yield application


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def database():
    """Mock database fixture to satisfy tests referencing it."""
    return None
