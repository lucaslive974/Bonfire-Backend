import os
from unittest.mock import patch

import pytest

from app import BonfireApp

# Set dummy environment variables to prevent Config from raising ErrMissingRequiredEnv during test imports
for key, val in [
    ("DB_PASSWORD", "test_password"),
    ("KEYCLOAK_CLIENT_SECRET", "test_client_secret"),
    ("KEYCLOAK_REALM_NAME", "test_realm"),
]:
    os.environ.setdefault(key, val)


# Mock database connection check and Keycloak connection check during test imports
patcher_db = patch("repositories.manager.SQLAlchemyRepositoryManager.check_connection")
patcher_kc_conn = patch("core.auth.authenticator.KeyCloakAuthenticator.checkConnection")

patcher_db.start()
patcher_kc_conn.start()


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

        # Inject Fake Repositories and Services
        from services.factory import ServiceFactory
        from tests.fakes import FakeRepositoryManager

        fake_manager = FakeRepositoryManager()
        application.extensions["db_manager"] = fake_manager
        application.extensions["service_factory"] = ServiceFactory(fake_manager)

        yield application


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def database():
    """Mock database fixture to satisfy tests referencing it."""
    return None
