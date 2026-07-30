from fastapi.testclient import TestClient
from test_main import app

client = TestClient(app)

def test_home():
    response=client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message":"helloworld"}

def test_add():
    response=client.get('/add?a=11&b=11')
    assert response.status_code == 200
    assert response.json() == {"result":22}