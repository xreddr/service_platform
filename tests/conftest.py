import pytest
import sys
sys.path.append('/home/xreddr/repos/service_platform')
print(sys.path)
from src import create_app

@pytest.fixture
def client():
    client = create_app()
    return client