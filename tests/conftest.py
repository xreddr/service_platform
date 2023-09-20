import pytest
import sys
sys.path.append('/home/xreddr/repos/service_platform')
from src import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    print(app.config)
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()