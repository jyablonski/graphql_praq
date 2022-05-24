from fastapi.testclient import TestClient
import pytest

from tests.app import create_app


@pytest.fixture
def test_client():
    app = create_app()
    return TestClient(app)
