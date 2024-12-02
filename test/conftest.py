import pytest
from  main import app


@pytest.fixture
def client():
    """Fixture to provide a Flask test client."""
    app.config['TESTING'] = True
    client = app.test_client()
    yield client
