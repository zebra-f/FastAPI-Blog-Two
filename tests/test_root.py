from app.main import client


def test_root():
    res = client.get("/")
    assert res.json().get("Documentation") == {
                'Swagger UI': 'http://127.0.0.1:8000/docs', 
                'ReDoc': 'http://127.0.0.1:8000/redoc'
                }
    assert res.status_code == 200